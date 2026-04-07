from pathlib import Path
from openai import OpenAI
import os

key = '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'

client = OpenAI(api_key=key)

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="onyx", #verse, echo, fable, onyx
    speed = 1, # .25 - 4
    input="hello steve",
    instructions="Speak like eeyore",
) as response:
    response.stream_to_file(speech_file_path)

os.system('afplay speech.mp3')