from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

from chat_with_anyone.db import db
from chat_with_anyone.middlewares import setup_middlewares
from chat_with_anyone.routes import setup_routes
from settings import get_config

config = get_config()

app = web.Application(middlewares=[db])
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

if __name__ == "__main__":
    web.run_app(app)
