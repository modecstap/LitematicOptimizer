import aiohttp.web as web
from handlers import setup_routes

def start():
    app = web.Application()
    setup_routes(app)

    web.run_app(app, host='localhost', port=8080)