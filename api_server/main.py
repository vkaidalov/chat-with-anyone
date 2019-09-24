from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
import aiohttp_cors

from chat_with_anyone.db import db
from chat_with_anyone.middlewares import setup_middlewares
from chat_with_anyone.routes import setup_routes
from settings import get_config

config = get_config()

app = web.Application(middlewares=[db])
app['config'] = config
db.init_app(app, config=config["postgres"])
setup_middlewares(app)
setup_routes(app)

setup_aiohttp_apispec(
    app,
    title="Chat With Anyone API",
    version="0.1.0",
    url="/api/docs/swagger.json",
    swagger_path="/api/docs"
)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
    )
})

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == "__main__":
    web.run_app(app)
