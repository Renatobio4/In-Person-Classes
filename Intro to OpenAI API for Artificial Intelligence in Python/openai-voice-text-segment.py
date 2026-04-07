from openai import OpenAI

key = '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'

client = OpenAI(api_key=key)

audio_file = open("openai-test-audio.m4a", "rb")

transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["segment"]
)
print(transcript)
print('****')

for segment in transcript.segments:
    start = segment.start
    end = segment.end
    text = segment.text
    print(f"{start:.2f}s - {end:.2f}s: {text}")
