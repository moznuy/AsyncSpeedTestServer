from aiohttp import web
from aiohttp.web_request import Request
import time


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handle_upload(request: Request):
    try:
        reader = await request.multipart()
    except KeyError:
        return web.Response(text='Content-Type not provided', status=400)

    field = await reader.next()
    if field.name != 'file':
        return web.Response(text='field "file" is not provided', status=400)
    size = 0
    start = time.time_ns()
    while True:
        chunk = await field.read_chunk()  # 8192 bytes by default.
        if not chunk:
            break
        size += len(chunk)
    elapsed = time.time_ns() - start
    resp = f'{size}\n{elapsed}'
    print(size * 10 ** 9 / (elapsed *1024*1024))
    return web.Response(text=resp)


app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.post('/upload', handle_upload),
])


if __name__ == '__main__':
    web.run_app(app)


"""
 gunicorn main:app --bind localhost:8080 --worker-class aiohttp.GunicornUVLoopWebWorker
"""
