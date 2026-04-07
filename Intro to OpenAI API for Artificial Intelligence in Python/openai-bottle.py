from openai import OpenAI
from bottle import run, route, post, request

injection = 'Answer in Fewer Than 20 Words.'

def ai(query):
    key = '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'

    client = OpenAI(api_key=key)

    response = client.responses.create(
        model="gpt-5-nano",
        input=query
    )
    return response.output_text

@route('/', method=['GET','POST'])
def index():
    query = request.forms.get('query')

    if query:
        query_full = f'{injection} -- {query}'
        response = ai(query_full)
    else:
        query = 'Please Ask a Question'
        response = '***'

    page = f'''
            <h1>Web App</h1>
            <form action="/" method="post">
                How Can I help: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {response}
            '''
    return page

run(host='127.0.0.1', port=8080)