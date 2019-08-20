from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import UniqueViolationError
from marshmallow import Schema, fields
from secrets import token_urlsafe

from ..models.user import User


class SigninRequestSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class SignupRequestSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()


class AuthResponseSchema(Schema):
    token = fields.Str()


@docs(tags=['auth'], summary='User sign-in')
@request_schema(SigninRequestSchema(strict=True))
@response_schema(AuthResponseSchema(), 200)
async def sign_in(request):
    """
    Signs user in if username exists and password is valid.
    :param request: content of the page to take json.
    :return: response in json representation.
    """
    data = await request.json()
    user = await User.query.where(User.email == data['email']).gino.first()

    if user and user.password == data['password']:
        await user.update(token=token_urlsafe(30)).apply()
        return web.json_response({'token': user.token})
    else:
        return web.json_response(status=403)


@docs(tags=['auth'], summary='User signup')
@request_schema(SignupRequestSchema(strict=True))
@response_schema(AuthResponseSchema(), 201)
async def signup(request):
    """
    Signs user up if email is unique.
    :param request: content of the page to take json.
    :return: response in json representation.
    """
    data = await request.json()
    try:
        await User.create(username=data['username'], email=data['email'], password=data['password'],
                          token=token_urlsafe(30))
    except UniqueViolationError as e:
        return web.json_response({'message': e.as_dict()['detail']})

    return web.json_response(status=201)
