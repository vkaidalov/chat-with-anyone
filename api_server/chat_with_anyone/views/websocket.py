import logging
from datetime import datetime, timedelta

import aiohttp
from aiohttp import web

from ..models.user import User

log = logging.getLogger(__name__)


async def websocket_handler(request):
    user = await User.query.where(
        User.token == request.match_info.get('token')
    ).gino.first()

    if not user:
        return web.json_response(
            {"message": "Provided token is invalid."}, status=403
        )
    time_now = datetime.utcnow()
    expires_at = user.token_created_at + timedelta(
        **request.app['config']['token_expires']
    )

    if time_now > expires_at:
        return web.json_response(
            {"message": "Token is expired."}, status=403
        )

    if not user:
        return web.json_response(
            {"message": "Invalid token."},
            status=401
        )

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'][user.id] = ws

    while True:
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.TEXT:
            log.info('%s sent a message: %s.', user.username, msg.data)
        else:
            break

    del request.app['websockets'][user.id]
    log.info('%s disconnected.', user.username)

    return ws
