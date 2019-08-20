import json

from aiohttp import web
from aiohttp_apispec import (
    docs, request_schema, response_schema, marshal_with
)
from asyncpg import ForeignKeyViolationError
from marshmallow import Schema, fields
from sqlalchemy import and_

from ..models.user import User
from ..models.contact import Contact


class UserRequestSchema(Schema):
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class ContactRequestSchema(Schema):
    contact_id = fields.Int()


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


class ContactList(web.View):
    @docs(
        tags=['Contacts'],
        summary='Create a new contact.',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @request_schema(ContactRequestSchema(strict=True))
    async def post(self):
        token = self.request.headers.get("Authorization")
        if not token:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )

        user = await User.query.where(User.token == token).gino.first()
        if not user:
            return web.json_response(
                {"message": "Provided token is invalid."}, status=403
            )

        request_user_id = int(self.request.match_info.get('user_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Posting to other's contact list is forbidden."},
                status=403
            )

        try:
            await Contact.create(
                owner_id=user.id,
                contact_id=self.request["data"]["contact_id"]
            )
        except ForeignKeyViolationError:
            return web.json_response(
                {"message": "Specified 'contact_id' is invalid."}, status=400
            )

        return web.json_response(status=201)

    @docs(
        tags=['Contacts'],
        summary="Get a list of a user's contacts.",
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @marshal_with(UserResponseSchema(many=True))
    async def get(self):
        token = self.request.headers.get("Authorization")
        if not token:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )

        user = await User.query.where(User.token == token).gino.first()
        if not user:
            return web.json_response(
                {"message": "Provided token is invalid."}, status=403
            )

        request_user_id = int(self.request.match_info.get('user_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Getting other's contact list is forbidden."},
                status=403
            )

        user_class_alias = User.alias()

        query = User.outerjoin(
            Contact, onclause=(User.id == Contact.owner_id)
        ).outerjoin(
            user_class_alias, onclause=(user_class_alias.id == Contact.contact_id)
        ).select().where(User.id == request_user_id)

        users = await query.gino.load(
            User.distinct(User.id).load(add_contact=user_class_alias)).all()

        return web.json_response(
            UserResponseSchema().dump(
                [contact.to_dict() for contact in users[0].contacts],
                many=True
            ).data)


class ContactDetail(web.View):
    @docs(
        tags=['Contacts'],
        summary='Delete the specified contact.',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    async def delete(self):
        token = self.request.headers.get("Authorization")
        if not token:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )

        user = await User.query.where(User.token == token).gino.first()
        if not user:
            return web.json_response(
                {"message": "Provided token is invalid."}, status=403
            )

        request_user_id = int(self.request.match_info.get('user_id'))
        request_contact_id = int(self.request.match_info.get('contact_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Deleting from other's contact list is forbidden."},
                status=403
            )

        await Contact.delete.where(
            and_(
                Contact.owner_id == request_user_id,
                Contact.contact_id == request_contact_id
            )
        ).gino.status()

        return web.json_response(status=204)
