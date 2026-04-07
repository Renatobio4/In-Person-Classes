from ollama import embeddings

chunk = 'Hello world'

result = embeddings(
    model='mxbai-embed-large', 
    prompt=chunk
    )

print(result['embedding'])