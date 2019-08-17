from aiohttp import web
from aiohttp_apispec import (docs,
                             request_schema,
                             response_schema)
from marshmallow import Schema, fields

from chat_with_anyone.models.user import User


class TestIndexRequestSchema(Schema):
    id = fields.Int()
    name = fields.Str(description='name')
    bool_field = fields.Bool()


class TestIndexResponseSchema(Schema):
    msg = fields.Str()
    data = fields.Dict()


@docs(tags=['mytag'],
      summary='Test method summary',
      description='Test method description')
@request_schema(TestIndexRequestSchema(strict=True))
@response_schema(TestIndexResponseSchema(), 200)
async def index(_request):
    """
    Just an example, should be deleted later.
    """
    return web.json_response({'msg': 'done',
                              'data': {}})


class UserDetailSchema(Schema):
    id = fields.Int()
    username = fields.Str()


@docs(summary="User detail",
      description="Get a user's details")
@response_schema(UserDetailSchema(), 200)
async def get_user_detail(request):
    name = request.match_info.get('name', '')
    user = await User.query.where(User.username == name).gino.first()
    if not user:
        return web.json_response(status=404)

    return web.json_response(UserDetailSchema().dump(user.to_dict()).data)
