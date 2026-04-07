from openai import OpenAI
import requests
import time

key = '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'

client = OpenAI(api_key=key)

result = client.images.generate(
    model="dall-e-3",
    prompt="A person riding a cat while they eat a taco",
    size="1024x1024"
)

image_url = result.data[0].url

print(result)
print('****')
print(result.data[0].revised_prompt)
print('****')
print(image_url)

img_data = requests.get(image_url).content
filename = f"{int(time.time())}.png"

with open(filename, "wb") as handler:
    handler.write(img_data)