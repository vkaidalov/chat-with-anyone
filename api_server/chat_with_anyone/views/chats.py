from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields, validate
from sqlalchemy import and_

from ..models.group_room import GroupRoom
from ..models.group_message import GroupMessage
from ..models.group_membership import GroupMembership
from ..decorators import token_and_active_required


class ChatRequestSchema(Schema):
    name = fields.Str()
    description = fields.Str()


class ChatResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


class MessageRequestSchema(Schema):
    text = fields.Str(validate=validate.Length(max=500), required=True)


class MessageResponseSchema(Schema):
    id = fields.Int()
    text = fields.Str(validate=validate.Length(max=500), required=True)
    created_at = fields.DateTime()


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


class ChatMessages(web.View):
    @docs(tags=['message'],
          summary='Fetch all message in chat',
          parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
          }])
    @response_schema(MessageResponseSchema(many=True))
    @response_schema(MessageResponseSchema())
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

        messages = await GroupMessage.query.where(
            GroupMessage.room_id == int(chat_id)).gino.all()

        return web.json_response(
            MessageResponseSchema().dump(
                [message.to_dict() for message in messages],
                many=True
            ).data)

    @docs(tags=['message'],
          summary='Create new message',
          parameters=[{
            'in': 'header',
            'name': 'Authorization',
            'schema': {'type': 'string'},
            'required': 'true'
          }])
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
