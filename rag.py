import os
import ollama
import chromadb

from ollama import Client
from pypdf import PdfReader


# =========================================================
# Configuration
# =========================================================

DOCUMENT_FOLDER = "documents"
CHROMA_FOLDER = "chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"
#LLM_MODEL = "llama3.2"
LLM_MODEL = "gemma4:cloud"
# Distance threshold
# Lower distance = more similar
RAG_DISTANCE_THRESHOLD = 1.2


# =========================================================
# ChromaDB
# =========================================================

# client = chromadb.PersistentClient(
#     path=CHROMA_FOLDER
# )

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="documents"
)

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}"
    }
)

# collection = client.get_or_create_collection(
#     name="documents"
# )


# =========================================================
# Read PDF
# =========================================================

def read_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================================
# Split text into chunks
# =========================================================

def split_text(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


# =========================================================
# Create Embedding
# =========================================================

def create_embedding(text):

    # response = ollama.embed(
    #     model=EMBEDDING_MODEL,
    #     input=text
    # )

    response = client.embed(
            model=EMBEDDING_MODEL,
            input=text
        )
    return response["embeddings"][0]


# =========================================================
# Ingest PDF Documents
# =========================================================

def ingest_documents():

    if not os.path.exists(DOCUMENT_FOLDER):

        raise Exception(
            f"Document folder not found: {DOCUMENT_FOLDER}"
        )

    pdf_found = False

    for filename in os.listdir(DOCUMENT_FOLDER):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_found = True

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        print("--------------------------------")
        print("Reading:", filename)
        print("--------------------------------")

        # Read PDF
        text = read_pdf(file_path)

        if not text.strip():

            print(
                f"No text found in {filename}"
            )

            continue

        # Split PDF text
        chunks = split_text(text)

        print(
            "Total chunks:",
            len(chunks)
        )

        # Create embeddings
        for index, chunk in enumerate(chunks):

            print(
                f"Creating embedding {index + 1}/{len(chunks)}"
            )

            embedding = create_embedding(chunk)

            collection.upsert(

                ids=[
                    f"{filename}-{index}"
                ],

                documents=[
                    chunk
                ],

                embeddings=[
                    embedding
                ],

                metadatas=[
                    {
                        "source": filename,
                        "chunk": index
                    }
                ]
            )

    if not pdf_found:

        print(
            "No PDF files found in documents folder."
        )

    else:

        print("--------------------------------")
        print("Documents indexed successfully.")
        print("--------------------------------")


# =========================================================
# Search Documents
# =========================================================

def search_documents(
    question,
    number_of_results=3
):

    # Create embedding for question
    question_embedding = create_embedding(
        question
    )

    # Search ChromaDB
    results = collection.query(

        query_embeddings=[
            question_embedding
        ],

        n_results=number_of_results,

        include=[
            "documents",
            "distances",
            "metadatas"
        ]
    )

    return results


# =========================================================
# Normal LLM Answer
# =========================================================

def ask_llm(question):

    # response = ollama.generate(

    #     model=LLM_MODEL,

    #     prompt=question
    # )
    response = client.generate(
   
           model=LLM_MODEL,
   
           prompt=question
       )
    return response["response"]


# =========================================================
# RAG + Normal LLM
# =========================================================

def ask_rag(question):

    # -----------------------------------------------------
    # Check whether ChromaDB contains documents
    # -----------------------------------------------------

    total_documents = collection.count()

    if total_documents == 0:

        print(
            "No documents found in ChromaDB."
        )

        # Normal LLM
        answer = ask_llm(question)

        return {
            "answer": answer,
            "context": "",
            "source": "llama3.2"
        }


    # -----------------------------------------------------
    # Search PDF
    # -----------------------------------------------------

    results = search_documents(
        question,
        number_of_results=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    # -----------------------------------------------------
    # No search result
    # -----------------------------------------------------

    if not documents:

        answer = ask_llm(question)

        return {
            "answer": answer,
            "context": "",
            "source": "llama3.2"
        }


    # -----------------------------------------------------
    # Best matching document
    # -----------------------------------------------------

    best_distance = distances[0]

    print("--------------------------------")
    print("Question:", question)
    print("Best distance:", best_distance)
    print("--------------------------------")


    # -----------------------------------------------------
    # Question is NOT related to PDF
    # -----------------------------------------------------

    if best_distance > RAG_DISTANCE_THRESHOLD:

        print(
            "Question is not related to PDF."
        )

        # Ask normal LLM
        answer = ask_llm(question)

        return {
            "answer": answer,
            "context": "",
            "source": "llama3.2"
        }


    # -----------------------------------------------------
    # Question IS related to PDF
    # -----------------------------------------------------

    print(
        "Question is related to PDF."
    )


    # Combine retrieved chunks
    context_parts = []

    for index, document in enumerate(documents):

        source = ""

        if index < len(metadatas):

            source = metadatas[index].get(
                "source",
                ""
            )

        context_parts.append(

            f"Source: {source}\n"
            f"{document}"
        )


    context = "\n\n".join(
        context_parts
    )


    # -----------------------------------------------------
    # RAG Prompt
    # -----------------------------------------------------

    prompt = f"""
You are an AI assistant.

Answer the user's question using the document
context provided below.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

RULES:

1. Use the document context when answering.
2. Do not make up information.
3. If the answer is clearly available in the context,
   answer the question directly.
4. If the answer is not available in the document,
   say:
   "I could not find this information in the document."

ANSWER:
"""


    # -----------------------------------------------------
    # Send context + question to Llama
    # -----------------------------------------------------

    response = client.generate(

        model=LLM_MODEL,

        prompt=prompt
    )


    return {

        "answer": response["response"],

        "context": context,

        "source": "RAG"
    }