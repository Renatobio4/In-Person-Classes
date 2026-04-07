from bs4 import BeautifulSoup
import feedparser
import requests
from ollama import embeddings
import pysqlite3 as sqlite3
import sqlite_vec
import struct
from typing import List

site_list = ['https://feeds.arstechnica.com/arstechnica/index',
         'https://techcrunch.com/feed/',
         'https://gizmodo.com/feed']

class db():
    database = 'vector.db'
    def create_feed():
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS feed(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DEFAULT CURRENT_TIMESTAMP,
                site TEXT,
                title TEXT,
                url TEXT
            );
            """
        cursor.execute(sql,)
        conn.commit()
        conn.close()
        pass

    def create_post():
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS post(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DEFAULT CURRENT_TIMESTAMP,
                site TEXT,
                url TEXT,
                post TEXT
            );
            """
        cursor.execute(sql,)
        conn.commit()
        conn.close()
        pass

    def create_chunk():
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS chunk(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DEFAULT CURRENT_TIMESTAMP,
                url TEXT,
                chunk TEXT
            );
            """
        cursor.execute(sql,)
        conn.commit()
        conn.close()
        pass

    def create_embed():
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS embed(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DEFAULT CURRENT_TIMESTAMP,
                chunk_id INTEGER,
                chunk TEXT,
                embed TEXT
            );
            """
        cursor.execute(sql,)
        conn.commit()
        conn.close()
        pass

    def create_embed_vec():
        conn = sqlite3.connect(db.database)
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS embed_vec
            USING vec0(
                chunk_id INTEGER,
                embedding float[1024]
            );
        """)
        conn.commit()
        conn.close()

    def feed_find(title):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'select * from feed where title like ?'
        result = cursor.execute(sql,(f'%{title}%',))
        result = result.fetchall()
        conn.close()
        return result

    def feed_post(title):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'select * from post where title like ?'
        result = cursor.execute(sql,(title,))
        result = result.fetchone()
        conn.close()
        return result

    def feed_new(site,title,url):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'insert into feed(site,title,url) values(?,?,?)'
        cursor.execute(sql,(site,title,url))
        conn.commit()
        conn.close() 

    def post_new(site,url,post):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'insert into post(site,url,post) values(?,?,?)'
        cursor.execute(sql,(site,url,post))
        conn.commit()
        conn.close() 

    def post_find(url):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'select * from post where url like ?'
        result = cursor.execute(sql,(f'%{url}%',))
        result = result.fetchall()
        conn.close()
        return result

    def new_chunk(url,chunk):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'insert into chunk(url,chunk) values(?,?)'
        cursor.execute(sql,(url,chunk))
        conn.commit()
        conn.close() 

    def find_chunk(url):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'select * from chunk where url like ?'
        result = cursor.execute(sql,(f'%{url}%',))
        result = result.fetchall()
        conn.close()
        return result

    def insert_embed(chunk_id,text,chunk_embed):
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        sql = 'insert into embed(chunk_id,chunk,embed) values(?,?,?)'
        cursor.execute(sql,(chunk_id,text,chunk_embed))
        conn.commit()
        conn.close() 

    def find_embed(chunk_id):
        conn = sqlite3.connect(db.database)
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        cursor = conn.cursor()
        sql = 'select * from embed_vec where chunk_id = ?'
        result = cursor.execute(sql,(chunk_id,))
        result = result.fetchall()
        conn.close()
        return result

def scrape_feed(site_list):
    for site in site_list:
        try:
            d = feedparser.parse(site)
            for value in d.entries:
                title = value.title
                url = value.links[0].href
                if not db.feed_find(title):
                    db.feed_new(site,title,url)
            print(f'Processed: {title}')
        except:
            print(f'ERROR: {site}')

def scrape_post(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    paragraphs = soup.find_all("p")
    page_clean =''
    for line in paragraphs:
        page_clean+= line.get_text()
    return page_clean

def create_embed(chunk):
    result = embeddings(
        model='mxbai-embed-large', 
        prompt=chunk
        )

    return result['embedding']

def serialize(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)

db.create_feed()
db.create_post()
db.create_chunk()
db.create_embed()
db.create_embed_vec()

# Create Feed of All Sites to be Scraped
scrape_feed(site_list)

# Process Feed and INSERT site,title and url into POST table if url is not in table
feed_all = db.feed_find(' ')
for post in feed_all:
    site = post[2]
    title = post[3]
    url = post[4]
    print(url)
    if not db.post_find(url):
        post=scrape_post(url)
        db.post_new(site,url,post)
    print(f'POST:{post}')

# Turn posts in POST table into chunks and INSERT url and chunk into CHUNK table
post_all = db.post_find('/')
for post in post_all:
    url = post[3]
    if not db.find_chunk(url): # Manually create chunks
        text = post[4]
        list_word = text.split(' ')
        max = len(list_word)
        start = 0
        increment = 100
        stop = increment
        current = 0
        while stop < max:
            chunk = list_word[start:stop]
            chunk = ' '.join(chunk)
            db.new_chunk(url,chunk)
            start = stop - 20
            stop = stop + increment
            print(chunk)

# Find if embed has been created for chunk and if not create it and INSERT into database
chunk_all = db.find_chunk('')
for chunk in chunk_all:
    chunk_id = chunk[0]
    text = chunk[3]
    if not db.find_embed(chunk_id):
        chunk_embed = create_embed(text)
        vector_bytes = serialize(chunk_embed)

        conn = sqlite3.connect("vector.db")
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        conn.execute(
            "INSERT INTO embed_vec(chunk_id, embedding) VALUES (?,?)",
            (chunk_id, vector_bytes)
        )
        conn.commit()
        conn.close()

print('Finished')