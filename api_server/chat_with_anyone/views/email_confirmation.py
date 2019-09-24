from aiohttp import web
from aiohttp_apispec import docs

from ..models.user import User


@docs(tags=['Auth'], summary='Email confirmation.')
async def email_token_confirmation(request):
    user = await User.query.where(
        User.token == request.match_info.get('token')
    ).gino.first()

    if not user:
        return web.json_response(
            {"message": "Invalid token."},
            status=401
        )

    await user.update(is_active=True).apply()

    return web.json_response(
        {'message': 'WELCOME'},
        status=200
    )
