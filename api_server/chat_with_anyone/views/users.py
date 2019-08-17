import json

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields

from ..models.user import User


class UserRequestSchema(Schema):
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class MeDetails(web.View):
    @docs(tags=['user'], summary='Fetch my profile details')
    @response_schema(UserResponseSchema(), 200)
    async def get(self):
        return web.json_response({})

    @docs(tags=['user'], summary='Edit my profile details')
    @request_schema(UserRequestSchema(strict=True))
    @response_schema(UserResponseSchema(), 200)
    async def patch(self):
        data = await self.request.json()
        print('me.patch', data)
        return web.json_response({})

    @docs(tags=['user'], summary='Delete my profile')
    async def delete(self):
        return web.json_response(status=204)


class UserDetails(web.View):
    @docs(tags=['user'], summary='Fetch profile details by id')
    @response_schema(UserResponseSchema(), 200)
    async def get(self):
        user_id = self.request.match_info.get('user_id')
        user = await User.get(int(user_id))

        if user is None:
            raise web.HTTPNotFound(
                body=json.dumps({'message': 'Invalid id'}),
                content_type='application/json'
            )

        return web.json_response(
            UserResponseSchema().dump(user.to_dict()).data)
