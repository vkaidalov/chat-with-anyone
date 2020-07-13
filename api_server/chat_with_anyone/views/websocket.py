from datetime import datetime, timedelta

import aiohttp
from aiohttp import web

from ..models.user import User


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

    while True:
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.TEXT:
            print('hi doggie')

        break

    # async for msg in ws:
    #     if msg.type == aiohttp.WSMsgType.TEXT:
    #         if msg.data == 'close':
    #             await ws.close()
    #         else:
    #             await ws.send_str(msg.data + '/answer')
    #     elif msg.type == aiohttp.WSMsgType.ERROR:
    #         print('ws connection closed with exception %s' %
    #               ws.exception())

    print('websocket connection closed')

    return ws
