from aiohttp import web

from chat_with_anyone.models.user import User


async def get_user_detail(request):
    name = request.match_info.get('name', '')
    user = await User.query.where(User.username == name).gino.first()
    if not user:
        return web.Response(text="User Not Found!")
    return web.Response(text=f"Hello, {user.username}. Your id is {user.id}.")
