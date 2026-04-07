from langchain_text_splitters import RecursiveCharacterTextSplitter

with open('story.txt', 'r') as file:
    story = file.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(story)

print(chunks)

for x in chunks:
    print('***')
    print(x)