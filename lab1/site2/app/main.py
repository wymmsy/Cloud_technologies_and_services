from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.routing import Route

async def info(request):
    url = str(request.url)
    client_host = request.client.host
    client_port = request.client.port
    headers_html = '<br>'.join(f"{k}: {v}" for k, v in request.headers.items())

    html = f"""
    <html>
        <head><title>Request Info</title>
	<link rel="stylesheet" href="/static/style.css">
	</head>
        <body>
            <h2>Информация о запросе</h2>
            <p><b>URL:</b> {url}</p>
            <p><b>Клиент:</b> {client_host}:{client_port}</p>
            <p><b>Заголовки:</b><br>{headers_html}</p>
        </body>
    </html>
    """

    return HTMLResponse(html)

app = Starlette(debug=True, routes=[
    Route("/", info)
])
app.mount("/static", StaticFiles(directory="static"), name="static")
