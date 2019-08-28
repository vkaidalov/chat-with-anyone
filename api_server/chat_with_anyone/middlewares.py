from aiohttp import web
from aiohttp_apispec import validation_middleware

from .models.user import User


@web.middleware
async def authorization(request, handler):
    token = request.headers.get("Authorization")
    if not token:
        request["user"] = None
    else:
        user = await User.query.where(User.token == token).gino.first()
        if not user:
            return web.json_response(
                {"message": "Provided token is invalid."}, status=403
            )
        request["user"] = user

    return await handler(request)


def setup_middlewares(app):
    app.middlewares.extend([validation_middleware, authorization])
