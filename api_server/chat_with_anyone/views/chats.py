from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from marshmallow import Schema, fields
from sqlalchemy import and_

from ..db import db
from ..decorators import token_and_active_required
from ..models.group_membership import GroupMembership
from ..models.group_room import GroupRoom


class ChatRequestSchema(Schema):
    name = fields.Str()
    description = fields.Str()


class ChatResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


class AddUserRequestSchema(Schema):
    user_id = fields.Int()


class MessageRequestSchema(Schema):
    pass


class MessageResponseSchema(Schema):
    pass


class Chats(web.View):
    @docs(tags=['chats'], summary='Create new chat')
    @request_schema(ChatRequestSchema(strict=True))
    @response_schema(ChatResponseSchema(), 200)
    async def post(self):
        data = await self.request.json()
        print('chats.post', data)

        return web.json_response({}, status=201)

    @docs(tags=['chats'], summary='Fetch list of chats')
    @response_schema(ChatResponseSchema(), 200)
    async def get(self):
        query = self.request.query
        print('chats.get', query)

        return web.json_response([])


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

        last_user = await db\
            .select([db.func.count(GroupMembership.user_id)])\
            .where(GroupMembership.room_id == request_chat_id)\
            .gino\
            .scalar()

        if last_user == 0:
            await GroupRoom.delete.where(
                GroupRoom.id == request_chat_id).gino.status()

        return web.json_response(status=204)


class ChatMessages(web.View):
    @docs(tags=['message'], summary='Create new message')
    @request_schema(MessageRequestSchema(strict=True))
    @response_schema(MessageResponseSchema(), 200)
    async def post(self):
        chat_id = self.request.match_info.get('chat_id')
        print('chat.messages.post', chat_id)

        return web.json_response({}, status=201)

    @docs(tags=['message'], summary='Fetch all message in chat')
    @response_schema(MessageResponseSchema(), 200)
    async def get(self):
        chat_id = self.request.match_info.get('chat_id')
        print('chat.messages.get', chat_id)

        return web.json_response([])


class ChatMessageDetails(web.View):
    @docs(tags=['message'], summary='Fetch message details')
    @response_schema(MessageResponseSchema(), 200)
    async def get(self):
        chat_id = self.request.match_info.get('chat_id')
        message_id = self.request.match_info.get('message_id')
        print('chat.messages.details.get.chat_id', chat_id)
        print('chat.messages.details.get.message_id', message_id)

        return web.json_response({})

    @docs(tags=['message'], summary='Update message details')
    @request_schema(MessageRequestSchema(strict=True))
    @response_schema(MessageResponseSchema(), 200)
    async def patch(self):
        chat_id = self.request.match_info.get('chat_id')
        message_id = self.request.match_info.get('message_id')
        print('chat.messages.details.patch.chat_id', chat_id)
        print('chat.messages.details.patch.message_id', message_id)

        return web.json_response({})

    @docs(tags=['message'], summary='Delete message')
    async def delete(self):
        chat_id = self.request.match_info.get('chat_id')
        message_id = self.request.match_info.get('message_id')
        print('chat.messages.details.delete.chat_id', chat_id)
        print('chat.messages.details.delete.message_id', message_id)

        return web.json_response(status=204)
