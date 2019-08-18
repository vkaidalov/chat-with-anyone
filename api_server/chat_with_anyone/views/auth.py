from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields


class SigninRequestSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class SignupRequestSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class AuthResponseSchema(Schema):
    token = fields.Str()


@docs(tags=['auth'], summary='User signin')
@request_schema(SigninRequestSchema(strict=True))
@response_schema(AuthResponseSchema(), 200)
async def signin(request):
    data = await request.json()
    print('signin', data)

    return web.json_response({'token': '123'})


@docs(tags=['auth'], summary='User signup')
@request_schema(SignupRequestSchema(strict=True))
@response_schema(AuthResponseSchema(), 200)
async def signup(request):
    data = await request.json()
    print('signup', data)

    return web.json_response({'token': '123'})
