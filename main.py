from pydantic import BaseModel

from backup_rag import ingest_documents, ask_rag,test_ollama,test_embedding
import ollama
from fastapi import FastAPI
from models import Product
#from database import engine
#from sqlalchemy import text


app = FastAPI()

class Question(BaseModel):
    question: str

# @app.get("/db-test")
# def db_test():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT GETDATE()"))
#         return {
#             "database_time": str(result.fetchone()[0])
#         }

# --------------------------------
# Load PDF into Vector Database
# --------------------------------
@app.get("/ollama-test")
def ollama_test():

    try:

        answer = test_ollama()

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    
@app.post("/rag/ingest")
def ingest():

    try:
        test_embedding()
    #    ingest_documents()

        return {
            "message": "Documents successfully indexed"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    # --------------------------------
# Ask RAG
# --------------------------------

@app.get("/rag/{question}")
def rag(question: str):

    try:

        result = ask_rag(question)

        return {
            "question": question,
            "answer": result["answer"],
            "context": result["context"],
            "source": result["source"]
        }

    except Exception as e:

        return {
            "error": str(e)
        } 
# @app.get("/product")
# def getAllProduct():
#     try:
#         query = text("SELECT * FROM Products")
#         with engine.connect() as connection:
#             result = connection.execute(query)
#             product = [dict(row._mapping) for row in result]  
#             if not product:
#                 return {"message": "No products found"} 
#             else:
#                 return {"message": "Products retrieved successfully", "products": product }                   

#     except Exception as e:
#         return {"error": str(e)}


# @app.get("/product/{id}")
# def getProductById(id: int):
#     try:
#         query = text("SELECT * FROM Products WHERE id = :id")
#         with engine.connect() as connection:
#             result = connection.execute(query, {"id": id})
#             product = result.fetchone()
#             if product:
#                 return {"message": "Product retrieved successfully", "product": dict(product)}
#             else:   
#                 return {"error": "Product not found"}
#     except Exception as e:
#         return {"error": str(e)}
     

# @app.post("/product")
# def createProduct(new_product: Product):
#     query = text("""
#         INSERT INTO Products (Name, Price, Quantity)
#         VALUES (:name, :price, :quantity)
#     """)
#     with engine.connect() as connection:
#         connection.execute(query, {
#             "name": new_product.name,
#             "price": new_product.price,
#             "quantity": new_product.quantity
#         })
#         connection.commit()
    
#     return {"message": "Product created successfully", "product": new_product}  

# @app.put("/product/{id}")
# def updateProduct(id: int, updated_product: Product):
#     query = text("""
#         UPDATE Products Set name = :name, price = :price, quantity = :quantity
#         WHERE id = :id  
#     """)
#     with engine.connect() as connection:
#         result = connection.execute(query, {
#             "id": id,
#             "name": updated_product.name,
#             "price": updated_product.price,
#             "quantity": updated_product.quantity
#         })
#         connection.commit()
#     if result.rowcount == 0:
#         return {"error": "Product not found"}
#     else:
#         return {"message": "Product updated successfully", "product": updated_product}  
    

# @app.delete("/product/{id}")
# def deleteProduct(id: int):
#     query = text("""
#         DELETE FROM Products WHERE id = :id 
#     """)
#     with engine.connect() as connection:
#         result = connection.execute(query, {"id": id})
#         connection.commit()

#     if result.rowcount == 0:
#         return {"error": "Product not found"}
#     else:
#         return {"message": "Product deleted successfully"}
    


@app.get("/ollama/{message}")
def ollama(message: str):
    import ollama 
    try:
        respone = ollama.generate(
            model="llama3.2",
            prompt=message
        )
     
        return {"response": respone["response"]}  
    except Exception as e:
        return {"error": str(e)}