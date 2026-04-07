from langchain_text_splitters import RecursiveCharacterTextSplitter
from ollama import embeddings
import numpy as np

def chunk_file():
    with open('story.txt', 'r') as file:
        story = file.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(story)
    return chunks

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

def process(chunk_list, embedding):
    for value in chunk_list:
        embedding2 = create_embed(value)
        similarity = cosine_similarity(embedding1, embedding2)
        if similarity >= .50: #change for minimum threshold
            print(f'{similarity}\n{value}\n')

chunk_list = chunk_file()

while True:
    query = input('Question: ')
    embedding1 = create_embed(query)
    process(chunk_list, embedding1)
