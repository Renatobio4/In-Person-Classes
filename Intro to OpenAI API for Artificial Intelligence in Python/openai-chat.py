from openai import OpenAI

key = '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'

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence joke about Louis Rossmann"
)
# print(response)
# print('****')
print(response.output_text)
# print(response.output[1].content[0].text)
print('****')
print(response.usage.total_tokens)