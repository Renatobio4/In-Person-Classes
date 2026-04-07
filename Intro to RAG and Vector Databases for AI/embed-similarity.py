from ollama import embeddings
import numpy as np

chunk = 'Hello World'
chunk_list = ['Hello World', 'World Hello', 'hello people of the world', 'the world is flat', 'Can I have a Big Mac']

# chunk = 'What is the time?'
# chunk_list = ['got the time?', 'you have the time?', 'do you know what time it is?', 'anyone know the time', 'Can I have a Big Mac']

def create_embed(chunk):
    result = embeddings(
        model='mxbai-embed-large', 
        prompt=chunk
        )

    return result['embedding']

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    return dot_product / (norm_vec1 * norm_vec2)

embedding1 = create_embed(chunk)

print(chunk)
for value in chunk_list:
    embedding2 = create_embed(value)
    similarity = cosine_similarity(embedding1, embedding2)
    print(f'{value}:', similarity)