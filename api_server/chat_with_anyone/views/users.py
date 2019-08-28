from aiohttp import web
from aiohttp_apispec import (
    docs, request_schema, response_schema, marshal_with
)
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from marshmallow import Schema, fields, validate
from sqlalchemy import and_

from ..models.user import User
from ..models.contact import Contact


class UserRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(max=40)
    )
    first_name = fields.Str(
        validate=validate.Length(max=30)
    )
    last_name = fields.Str(
        validate=validate.Length(max=150)
    )


class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str(
        validate=validate.Length(max=40), required=True
    )
    first_name = fields.Str(
        validate=validate.Length(max=30)
    )
    last_name = fields.Str(
        validate=validate.Length(max=150)
    )


class ContactRequestSchema(Schema):
    contact_id = fields.Int()


class UserDetail(web.View):
    @docs(
        tags=['User'],
        summary='Fetch profile details by id',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @response_schema(UserResponseSchema())
    async def get(self):
        if not self.request["user"]:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )

        request_user_id = self.request.match_info.get('user_id')
        request_user = await User.get(int(request_user_id))

        if request_user is None:
            return web.json_response(
                {'message': 'User not found.'}, status=404
            )

        return web.json_response(
            UserResponseSchema().dump(request_user.to_dict()).data
        )

    @docs(
        tags=['User'],
        summary='Edit my profile details',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @request_schema(UserRequestSchema(strict=True))
    async def patch(self):
        if self.request["user"]:
            user = self.request["user"]
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )
        request_user_id = int(self.request.match_info.get('user_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Patching other's profile is forbidden."}, status=403
            )

        data = await self.request.json()
        try:
            await user.update(
                username=data.get('username', user.username),
                first_name=data.get('first_name', user.first_name),
                last_name=data.get('last_name', user.last_name)
            ).apply()
        except UniqueViolationError as e:
            return web.json_response(
                {'message': e.as_dict()['detail']},
                status=400
            )
        
        return web.json_response(status=204)

    @docs(
        tags=['User'],
        summary='Delete my profile',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }])
    async def delete(self):
        if self.request["user"]:
            user = self.request["user"]
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
            )
        request_user_id = int(self.request.match_info.get('user_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Deleting other's profile is forbidden."},
                status=403
            )
        
        await user.delete()
        
        return web.json_response(status=204)


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
        if self.request["user"]:
            user = self.request["user"]
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
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
        if self.request["user"]:
            user = self.request["user"]
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
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
        if self.request["user"]:
            user = self.request["user"]
        else:
            return web.json_response(
                {"message": "Authorization token is required."}, status=401
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
