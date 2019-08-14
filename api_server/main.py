from aiohttp import web

from chat_with_anyone.db import db
from chat_with_anyone.models.user import User
from settings import get_config

config = get_config()

app = web.Application(middlewares=[db])
db.init_app(app, config=config["postgres"])


async def handle(request):
    name = request.match_info.get('name', '')
    user = await User.query.where(User.username == name).gino.first()
    if not user:
        return web.Response(text="User Not Found!")
    return web.Response(text=f"Hello, {user.username}. Your id is {user.id}.")


app.add_routes([web.get('/users/{name}', handle)])

if __name__ == "__main__":
    web.run_app(app)
