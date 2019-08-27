from secrets import token_urlsafe

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import UniqueViolationError
from marshmallow import Schema, fields, validate
from passlib.hash import bcrypt

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
    user_id = fields.Int()


@docs(tags=['Auth'], summary='Signup.')
@request_schema(SignupRequestSchema(strict=True))
async def sign_up(request):
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
            password=bcrypt.hash(data['password']),
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


@docs(tags=['Auth'], summary='Sign-in and receive a token and user_id.')
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

    if not (user and user.is_active and bcrypt.verify(data['password'],
                                                      user.password)):
        return web.json_response(
            {'message': 'Invalid credentials.'}, status=400
        )

    await user.update(token=token_urlsafe(30)).apply()
    return web.json_response({'token': user.token, 'user_id': user.id})


@docs(
    tags=['Auth'],
    summary='Sign-out.',
    parameters=[{
        'in': 'header',
        'name': 'Authorization',
        'schema': {'type': 'string'},
        'required': 'true'
    }])
async def sign_out(request):
    # for middleware in future ===>
    token = request.headers.get("Authorization")
    if not token:
        return web.json_response(
            {"message": "Authorization token is required."}, status=401
        )

    user = await User.query.where(User.token == token).gino.first()
    if not user:
        return web.json_response(
            {"message": "Provided token is invalid."}, status=403
        )
    # <=== for middleware in future
    request_user_id = int(request.match_info.get('user_id'))
    if user.id == request_user_id:
        await user.update(token=token_urlsafe(30)).apply()
        return web.json_response(status=200)
    else:
        return web.json_response(
            {'message': 'Invalid credentials'}, status=400
        )
