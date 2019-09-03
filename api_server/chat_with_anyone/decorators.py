from aiohttp import web
import inspect


def token_and_active_required(function_to_decorate):
    async def wrapper(req, *args, **kwargs):
        if 'self' in inspect.getfullargspec(function_to_decorate).args[0]:
            request = req.request
        else:
            request = req
        if request["user"]:
            if not request["user"].is_active:
                return web.json_response(
                    {"message": "User is not active."}, status=403
                    )
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
                )
        return await function_to_decorate(req, *args, **kwargs)
    return wrapper
