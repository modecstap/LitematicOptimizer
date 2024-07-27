from aiohttp import web

from .handlers import get_optimized_litematic


class AiohttpApplication:
    def __init__(self):
        self.app = web.Application()
        self._setup_routes()

        web.run_app(self.app, host='localhost', port=8080)

    def _setup_routes(self):
        self.app.router.add_post("/optimize_litematic", get_optimized_litematic)
