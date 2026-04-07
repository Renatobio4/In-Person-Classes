from openai import OpenAI
import time

key = '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'

client = OpenAI(api_key=key)

def ai(query):
    model = ['gpt-5','gpt-5-nano','gpt-3.5-turbo']

    for version in model:
        speed = time.time()
        response = client.responses.create(
            model=version,
            input=query
        )
        speed = time.time() - speed
        print(version)
        print(f'{speed} seconds')
        print(response.output_text)
        print('---------')

while True:
    query = input('Your Query: ')
    print(query)
    ai(query)
    print('****')
