from openai import OpenAI
from bottle import run, route, post, request
import requests
import time

injection = 'Add some pasta'

def ai(query):
    key = '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'
    client = OpenAI(api_key=key)

    result = client.images.generate(
        model="dall-e-3",
        prompt=query,
        size="1024x1024"
    )

    image_url = result.data[0].url
    revised_prompt = result.data[0].revised_prompt

    return image_url, revised_prompt

def gallery():
    with open('gallery_simple.csv', 'a+') as file:
        file.seek(0)
        pictures = file.readlines()
    gallery=''
    for image in pictures:
        item = image.split('|')
        gallery += f'''
                    <div style="display:inline-block; width:200px; height:auto; vertical-align:top;">
                        <img style="width:100%; height:auto;" src="{item[0]}">
                        <p>{item[1]}<p>
                    </div>
                    '''
    return gallery

@route('/', method=['GET','POST'])
def index():
    query = request.forms.get('query')

    if query:
        query_full = f'{injection} -- {query}'
        response = ai(query_full)
        with open('gallery_simple.csv', 'a') as file:
            file.write(f'{response[0]}|{response[1]}\n')
    else:
       response = '***'
 
    pic_gallery = gallery()

    page = f'''
            <h1>Web App</h1>
            <form action="/" method="post">
                Create an Image: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {response}<br>
            {pic_gallery}
            '''
    return page

run(host='127.0.0.1', port=8080)