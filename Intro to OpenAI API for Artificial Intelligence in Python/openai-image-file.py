import base64
from openai import OpenAI

key = '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'

client = OpenAI(api_key=key)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "roxy.png"

# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what kind of dog is this - answer in one word?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)