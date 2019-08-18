from aiohttp_apispec import validation_middleware


def setup_middlewares(app):
    app.middlewares.append(validation_middleware)
