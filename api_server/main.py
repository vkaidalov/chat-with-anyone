from aiohttp import web

from chat_with_anyone.db import db
from chat_with_anyone.routes import setup_routes
from settings import get_config

config = get_config()

app = web.Application(middlewares=[db])
db.init_app(app, config=config["postgres"])
setup_routes(app)

if __name__ == "__main__":
    web.run_app(app)
