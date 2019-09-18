from datetime import datetime

from aiohttp import web
from aiohttp_apispec import docs, marshal_with, request_schema, response_schema
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from marshmallow import Schema, fields, validate
from passlib.hash import bcrypt
from sqlalchemy import and_, desc

from api_server.chat_with_anyone.models.group_message import GroupMessage
from ..decorators import token_and_active_required
from ..models.contact import Contact
from ..models.group_membership import GroupMembership
from ..models.group_room import GroupRoom
from ..models.user import User


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


class UserListResponseSchema(Schema):
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


class PasswordChangeRequestSchema(Schema):
    old_password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    new_password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    new_password_repeat = fields.Str(
        validate=validate.Length(max=255), required=True
    )


class UserChatsResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    last_message_at = fields.DateTime()


class UserList(web.View):
    @docs(
        tags=['User'],
        summary="Return all users.",
        parameters=[
            {
                'in': 'header',
                'name': 'Authorization',
                'schema': {'type': 'string'},
                'required': 'true'
            },
            {
                'in': 'query',
                'name': 'username',
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'first_name',
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'last_name',
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'page',
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'page_size',
                'schema': {'type': 'integer'},
            }
        ]
    )
    @marshal_with(UserResponseSchema(many=True))
    @token_and_active_required
    async def get(self):
        query = self.request.query

        try:
            page = int(query.get('page', 1))
            page_size = int(query.get('page_size', 10))
        except ValueError:
            page = 1
            page_size = 10

        # one page pagination limit
        if page_size > 50:
            page_size = 50

        username = query.get('username')
        first_name = query.get('first_name')
        last_name = query.get('last_name')

        condition = []

        if username:
            condition.append(User.username.ilike(f'%{username}%'))
        if first_name:
            condition.append(User.first_name.ilike(f'%{first_name}%'))
        if last_name:
            condition.append(User.last_name.ilike(f'%{last_name}%'))

        users = await User.query.where(and_(*condition))\
            .limit(page_size).offset(page*page_size - page_size).gino.all()

        return web.json_response(
            UserListResponseSchema().dump(
                [user.to_dict() for user in users],
                many=True
            ).data)


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
    @token_and_active_required
    async def get(self):
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
    @token_and_active_required
    async def patch(self):
        user = self.request["user"]
        request_user_id = int(self.request.match_info.get('user_id'))
        if user.id != request_user_id:
            return web.json_response(
                {"message": "Patching other's profile is forbidden."},
                status=403
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
    @token_and_active_required
    async def delete(self):
        user = self.request["user"]
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
    @token_and_active_required
    async def post(self):
        user = self.request["user"]
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
        except UniqueViolationError:
            return web.json_response(
                {"message": "'contact_id' already exists"}, status=400
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
    @token_and_active_required
    async def get(self):
        user = self.request["user"]
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
            user_class_alias, onclause=(
                user_class_alias.id == Contact.contact_id)
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
    @token_and_active_required
    async def delete(self):
        user = self.request["user"]
        request_user_id = int(self.request.match_info.get('user_id'))
        request_contact_id = int(self.request.match_info.get('contact_id'))
        if user.id != request_user_id:
            message = "Deleting from other's contact list is forbidden"
            return web.json_response(
                {"message": message},
                status=403
            )

        request_contact = await Contact.query.where(
            and_(
                Contact.owner_id == request_user_id,
                Contact.contact_id == request_contact_id
            )
        ).gino.first()

        if request_contact is None:
            message = f'Contact with ID "{request_contact_id}" already deleted'
            return web.json_response(
                {'message': message},
                status=404
            )

        await Contact.delete.where(
            and_(
                Contact.owner_id == request_user_id,
                Contact.contact_id == request_contact_id
            )
        ).gino.status()

        return web.json_response(status=204)


class PasswordChange(web.View):
    @docs(
        tags=['PasswordChange'],
        summary='Change user`s password',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @request_schema(PasswordChangeRequestSchema(strict=True))
    @token_and_active_required
    async def patch(self):
        data = await self.request.json()
        user = self.request['user']

        request_user_id = int(self.request.match_info.get('user_id'))
        request_user = await User.get(int(request_user_id))

        if not request_user:
            return web.json_response(
                {"message": "User not found"},
                status=401
            )

        if user.id != request_user_id:
            return web.json_response(
                {
                    "message":
                    "Requested user_id doesn`t correspond current user_id"
                },
                status=403
            )

        old_password = request_user.password

        if not bcrypt.verify(data['old_password'], old_password):
            return web.json_response(
                {"message": "The old password you entered doesn`t match"},
                status=403
            )

        if data['new_password'] != data['new_password_repeat']:
            return web.json_response(
                {"message": "Passwords do not match"},
                status=403
            )

        try:
            await request_user.update(
                password=bcrypt.hash(data['new_password'])
            ).apply()

        except UniqueViolationError as ex:
            return web.json_response(
                {'message': ex.as_dict()['detail']},
                status=400
            )

        return web.json_response(status=204)


class UserChats(web.View):
    @docs(
        tags=['User Chats'],
        summary="Get a list of a user's chats",
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @response_schema(UserChatsResponseSchema())
    @token_and_active_required
    async def get(self):
        user = self.request["user"]
        request_user_id = int(self.request.match_info.get('user_id'))

        if user.id != request_user_id:
            return web.json_response(
                {"message": "Getting other's chats list is forbidden."},
                status=403
            )

        query = User.outerjoin(
            GroupMembership, onclause=(User.id == GroupMembership.user_id)
        ).outerjoin(
            GroupRoom, onclause=(
                GroupRoom.id == GroupMembership.room_id)
        ).select().where(User.id == request_user_id)

        print(query)

        ins_query = query.insert().values(
            GroupRoom.last_message_at == GroupMessage.query.order_by(desc(GroupMessage.created_at)).gino.iterate()
        )

        users = await query.gino.load(
            User.distinct(User.id).load(add_room=GroupRoom)).all()

        for _ in users[0].rooms:
            print(_.to_dict())

        return web.json_response(
            UserChatsResponseSchema().dump(
                [room.to_dict() for room in users[0].rooms],
                many=True
            ).data)
