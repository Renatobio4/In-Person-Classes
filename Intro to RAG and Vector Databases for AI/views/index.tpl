<head>
    <meta charset="utf-8">
</head>

<h1>AI RAG App</h1>

<form action="/" method=post>
    Query: <input type="text" name="query">
    <br>
    <input type="submit">
    <br>
</form>

<p><strong>Query:</strong> {{query}}</p>
<p><strong>Response:</strong> {{response}}</p>
<hr>
<p><strong>RAG:</strong></p>

% if rag:
    % for record in rag:
        <p>{{record[3]}}<br>
        {{record[2]}}<br>
        {{record[1]}}</p>
    % end
% end
