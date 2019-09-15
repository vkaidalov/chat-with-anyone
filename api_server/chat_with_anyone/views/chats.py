from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from marshmallow import Schema, fields, validate
from sqlalchemy import and_

from ..db import db
from ..decorators import token_and_active_required
from ..models.group_membership import GroupMembership
from ..models.group_message import GroupMessage
from ..models.group_room import GroupRoom
from ..models.user import User


class ChatRequestSchema(Schema):
    name = fields.Str(
        validate=validate.Length(max=200), required=True
    )


class ChatResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        validate=validate.Length(max=200), required=True
    )


class AddUserRequestSchema(Schema):
    user_id = fields.Int()


class MessageRequestSchema(Schema):
    text = fields.Str(validate=validate.Length(max=500), required=True)


class MessageResponseSchema(Schema):
    id = fields.Int()
    text = fields.Str(validate=validate.Length(max=500), required=True)
    created_at = fields.DateTime()
    username = fields.Str(validate=validate.Length(max=40), required=True)


class Chats(web.View):
    @docs(
        tags=['chats'],
        summary='Create a new chat',
        parameters=[
            {
                'in': 'header',
                'name': 'Authorization',
                'schema': {'type': 'string'},
                'required': 'true'
            }
        ]
    )
    @request_schema(ChatRequestSchema(strict=True))
    @token_and_active_required
    async def post(self):
        data = await self.request.json()
        user = self.request["user"]
        created_chat = await GroupRoom.create(
            name=data['name']
        )

        await GroupMembership.create(
            room_id=created_chat.id,
            user_id=user.id
        )

        return web.json_response(status=201)

    @docs(
        tags=['chats'],
        summary='Fetch list of chats',
        parameters=[
            {
                'in': 'header',
                'name': 'Authorization',
                'schema': {'type': 'string'},
                'required': 'true'
            },
            {
                'in': 'query',
                'name': 'name',
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
    @response_schema(ChatResponseSchema(many=True), 200)
    @token_and_active_required
    async def get(self):
        query = self.request.query

        try:
            page = int(query.get('page', 1))
            page_size = int(query.get('page_size', 10))
        except ValueError:
            page = 1
            page_size = 10

        if page_size > 50:
            page_size = 50

        name = query.get('name')

        condition = []

        if name:
            condition.append(GroupRoom.name.ilike(f'%{name}%'))

        chats = await GroupRoom.query.where(and_(*condition)) \
            .limit(page_size).offset(page * page_size - page_size).gino.all()

        return web.json_response(
            ChatResponseSchema().dump(
                [chat.to_dict() for chat in chats],
                many=True
            ).data)


class ChatUserList(web.View):
    @docs(
        tags=['chats'],
        summary='Add user into chat',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @request_schema(AddUserRequestSchema(strict=True))
    @token_and_active_required
    async def post(self):
        user = self.request["user"]
        request_chat_id = int(self.request.match_info.get('chat_id'))
        request_chat = await GroupRoom.get(request_chat_id)

        if request_chat is None:
            return web.json_response(
                {'message': f'Chat with ID "{request_chat_id}" was not found'},
                status=404
            )

        user_id = self.request.get('data', {}).get('user_id')

        if user.id != user_id:
            user_group = await GroupMembership.query.where(
                and_(
                    GroupMembership.user_id == user.id,
                    GroupMembership.room_id == request_chat_id
                )
            ).gino.first()

            if user_group is None:
                message = 'You have not been assigned with provided chat'

                return web.json_response(
                    {'message': message},
                    status=403
                )

        try:
            await GroupMembership.create(
                room_id=request_chat_id,
                user_id=user_id
            )
        except ForeignKeyViolationError:
            return web.json_response(
                {"message": "Provided chat_id or user_id is invalid"},
                status=400
            )
        except UniqueViolationError:
            return web.json_response(
                {"message": f'User with ID "{user_id}" already exists'},
                status=400
            )

        return web.json_response(status=201)


class ChatUserDetails(web.View):
    @docs(
        tags=['chats'],
        summary='Delete from chats',
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
        request_chat_id = int(self.request.match_info.get('chat_id'))

        if user.id != request_user_id:
            return web.json_response(
                {"message": "Deleting another user is forbidden"},
                status=403
            )

        request_chat = await GroupRoom.get(request_chat_id)

        if request_chat is None:
            return web.json_response(
                {'message': f'Chat with ID "{request_chat_id}" was not found'},
                status=404
            )

        user_group = await GroupMembership.query.where(
            and_(
                GroupMembership.user_id == request_user_id,
                GroupMembership.room_id == request_chat_id
            )
        ).gino.first()

        if user_group is None:
            message = f'User with ID "{request_user_id}" does not exist'

            return web.json_response(
                {'message': message},
                status=404
            )

        await GroupMembership.delete.where(
            and_(
                GroupMembership.user_id == request_user_id,
                GroupMembership.room_id == request_chat_id
            )
        ).gino.status()

        last_user = await db \
            .select([db.func.count(GroupMembership.user_id)]) \
            .where(GroupMembership.room_id == request_chat_id) \
            .gino \
            .scalar()

        if last_user == 0:
            await GroupRoom.delete.where(
                GroupRoom.id == request_chat_id).gino.status()

        return web.json_response(status=204)


class ChatMessages(web.View):
    @docs(
        tags=['message'],
        summary='Fetch all message in chat',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @response_schema(MessageResponseSchema(many=True))
    @token_and_active_required
    async def get(self):
        chat_id = self.request.match_info.get('chat_id')
        chat = await GroupRoom.get(int(chat_id))
        if not chat:
            return web.json_response(
                {'message': 'Chat not found.'}, status=404
            )
        user = self.request["user"]

        room_member = await GroupMembership.query.where(and_(
            GroupMembership.room_id == int(chat_id),
            GroupMembership.user_id == user.id)).gino.first()
        if not room_member:
            return web.json_response(
                {'message': "Getting messages is forbidden. "
                            "User is not in chat."}, status=403
            )

        query = GroupMessage.outerjoin(
            User, onclause=(GroupMessage.user_id == User.id)
        ).select().where(GroupMessage.room_id == int(chat_id))

        messages = await query.gino.load((GroupMessage, User.username)).all()

        return web.json_response(
            MessageResponseSchema().dump(
                [{
                    "id": message.id,
                    "text": message.text,
                    "created_at": message.created_at,
                    "username": username
                } for message, username in messages],
                many=True
            ).data)

    @docs(
        tags=['message'],
        summary='Create new message',
        parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
        }]
    )
    @request_schema(MessageRequestSchema(strict=True))
    @token_and_active_required
    async def post(self):
        chat_id = self.request.match_info.get('chat_id')
        user = self.request["user"]

        room_member = await GroupMembership.query.where(and_(
            GroupMembership.room_id == int(chat_id),
            GroupMembership.user_id == user.id)).gino.first()
        if not room_member:
            return web.json_response(
                {'message': "Posting messages is forbidden. "
                            "User is not in chat."}, status=403
            )

        await GroupMessage.create(
            text=self.request["data"]["text"],
            room_id=int(chat_id),
            user_id=user.id
        )

        return web.json_response(status=201)


class ChatMessageDetails(web.View):
    @docs(tags=['message'],
          summary='Update message',
          parameters=[{
              'in': 'header',
              'name': 'Authorization',
              'schema': {'type': 'string'},
              'required': 'true'
          }]
          )
    @request_schema(MessageRequestSchema(strict=True))
    @token_and_active_required
    async def patch(self):
        data = await self.request.json()
        user = self.request['user']

        request_message_id = int(self.request.match_info.get('message_id'))

        user_message = await GroupMessage.query.where(
            GroupMessage.id == request_message_id).gino.first()

        if not user_message:
            return web.json_response(
                {'message': "Message not found. Incorrect id"},
                status=403
            )

        if user.id != user_message.user_id:
            return web.json_response(
                {'message': "Changing another user's message is prohibited"},
                status=403
            )

        try:
            await user_message.update(
                text=data['text']
            ).apply()

        except UniqueViolationError as ex:
            return web.json_response(
                {'message': ex.as_dict()['detail']},
                status=400
            )

        return web.json_response(status=204)

    @docs(tags=['message'],
          summary='Delete message',
          parameters=[{
              'in': 'header',
              'name': 'Authorization',
              'schema': {'type': 'string'},
              'required': 'true'
          }]
          )
    @token_and_active_required
    async def delete(self):
        # data = await self.request.json()
        user = self.request['user']

        request_message_id = int(self.request.match_info.get('message_id'))

        user_message = await GroupMessage.query.where(
            GroupMessage.id == request_message_id).gino.first()

        if not user_message:
            return web.json_response(
                {'message': "Message not found. Incorrect id"},
                status=403
            )

        if user.id != user_message.user_id:
            return web.json_response(
                {'message': "Changing another user's message is prohibited"},
                status=403
            )

        try:
            await GroupMessage.delete.where(
                GroupMessage.id == request_message_id
            ).gino.status()

        except UniqueViolationError as ex:
            return web.json_response(
                {'message': ex.as_dict()['detail']},
                status=400
            )

        return web.json_response(status=204)
