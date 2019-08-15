from aiohttp import web

from .views.user import get_user_detail, index


def setup_routes(app):
    app.add_routes([
        web.post("/api/v1/index", index),
        web.get("/api/v1/users/{name}", get_user_detail)
    ])
