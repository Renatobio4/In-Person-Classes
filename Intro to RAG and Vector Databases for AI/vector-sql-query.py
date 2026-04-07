from ollama import embeddings, chat, ChatResponse
import pysqlite3 as sqlite3
import sqlite_vec
import struct
from typing import List

class db():    
    def find_rag(query_embedding):
        db = sqlite3.connect("vector.db")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        sql = '''
            SELECT
                chunk.id,
                chunk.url,
                chunk.chunk,
                embed_vec.distance
            FROM embed_vec
            JOIN chunk ON chunk.id = embed_vec.chunk_id
            WHERE embedding MATCH ?
                AND k = 5
            ORDER BY distance;
            '''
        response = db.execute(sql,([serialize(query_embedding)])).fetchall()
        return response
    
def create_embed(chunk):
    result = embeddings(
        model='mxbai-embed-large', 
        prompt=chunk
        )
    return result['embedding']

def serialize(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)

def ai(query, rag):
    query = f''' 
            Answer this question: {query}\n
            Only answer the question with no additional explanation.\n
            Based on This Information from a RAG Vector Database: {rag}
            '''
    response: ChatResponse = chat(model='gpt-oss', messages=[
    {
      'role': 'user',
      'content': query,
    },
    ])
    return response.message.content

while True:
    query = input('Question:  ')
    query_embedding = create_embed(query)
    rag = db.find_rag(query_embedding)
    response = ai(query, rag)
    print(query)
    print(response)