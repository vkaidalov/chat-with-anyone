from aiohttp import web

from .views.user import get_user_detail


def setup_routes(app):
    app.add_routes([
        web.get("/users/{name}", get_user_detail)
    ])
