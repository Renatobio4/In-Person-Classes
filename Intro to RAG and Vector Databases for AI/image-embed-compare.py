import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image

image1 = 'image.png'
gallery = ['image.png','image2.png','image3.png','image4.png','image5.png','image6.png','image7.png','image8.png']

def create_embed(picture):
    model = SentenceTransformer('clip-ViT-B-32')
    img = Image.open(picture)
    embedding = model.encode(img)

    return embedding

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    return dot_product / (norm_vec1 * norm_vec2)

embedding1 = create_embed(image1)

with open('image-log.txt', 'w') as file:
    file.write(f'{image1}\n****\n')

for value in gallery:
    embedding2 = create_embed(value)
    similarity = cosine_similarity(embedding1, embedding2)
    print(f'{value}:', similarity)
    with open('image-log.txt', 'a') as file:
        file.write(f'{value}\t{similarity}\n')
    
