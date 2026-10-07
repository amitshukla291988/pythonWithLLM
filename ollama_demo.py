import ollama 

respone = ollama.generate(
    model="llama3.2",
    prompt="hi"
)

print(respone["response"])