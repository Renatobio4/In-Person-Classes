from openai import OpenAI

key = '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'

client = OpenAI(api_key=key)

audio_file = open("openai-test-audio.m4a", "rb")
transcript = client.audio.transcriptions.create(
  model="gpt-4o-transcribe",
  file=audio_file
)

print(transcript)
print('****')
print(transcript.text)