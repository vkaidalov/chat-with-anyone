from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields


class ChatRequestSchema(Schema):
    name = fields.Str()
    description = fields.Str()


class ChatResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


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
