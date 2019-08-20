from secrets import token_urlsafe

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import UniqueViolationError
from marshmallow import Schema, fields, validate

from ..models.user import User


class SigninRequestSchema(Schema):
    email = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    password = fields.Str(
        validate=validate.Length(max=255), required=True
    )


class SignupRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(max=40), required=True
    )
    email = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    first_name = fields.Str(
        validate=validate.Length(max=30)
    )
    last_name = fields.Str(
        validate=validate.Length(max=150)
    )


class AuthResponseSchema(Schema):
    token = fields.Str(
        required=True, validate=validate.Length(equal=40)
    )


@docs(tags=['Auth'], summary='Sign-in and receive a token.')
@request_schema(SigninRequestSchema(strict=True))
@response_schema(AuthResponseSchema(strict=True))
async def sign_in(request):
    """
    Signs user in if email exists and password is valid.
    :param request: content of the page to take json.
    :return: response in json representation.
    """
    data = await request.json()
    user = await User.query.where(User.email == data['email']).gino.first()

    if not user or user.password != data['password']:
        return web.json_response(
            {'message': 'Invalid credentials.'}, status=400
        )

    await user.update(token=token_urlsafe(30)).apply()
    return web.json_response({'token': user.token})


@docs(tags=['Auth'], summary='Signup.')
@request_schema(SignupRequestSchema(strict=True))
async def signup(request):
    """
    Signs user up if email is unique.
    :param request: content of the page to take json.
    :return: response in json representation.
    """
    data = await request.json()

    try:
        await User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            token=token_urlsafe(30)
        )
    except UniqueViolationError as e:
        return web.json_response(
            {'message': e.as_dict()['detail']},
            status=400
        )

    return web.json_response(status=201)
