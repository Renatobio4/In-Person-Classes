from sentence_transformers import SentenceTransformer
from PIL import Image

# Load the CLIP model
model = SentenceTransformer('clip-ViT-B-32')

# Load your image
img = Image.open("image.png")

# Generate the vector embedding
embedding = model.encode(img)

print(embedding)