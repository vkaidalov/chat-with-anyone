from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema


class ContactRequestSchema(Schema):
    pass


class ContactResponseSchema(Schema):
    pass


class Contacts(web.View):
    @docs(tags=['contacts'], summary='Create new contact')
    @request_schema(ContactRequestSchema(strict=True))
    @response_schema(ContactResponseSchema(), 200)
    async def post(self):
        data = await self.request.json()
        print('contacts.post', data)

        return web.json_response(status=201)

    @docs(tags=['contacts'], summary='Fetch list of contacts')
    @response_schema(ContactResponseSchema(), 200)
    async def get(self):
        query = self.request.query
        print('contacts.get', query)

        return web.json_response(status=200)


class ContactDetails(web.View):
    @docs(tags=['contacts'], summary='Delete contact')
    async def delete(self):
        contact_id = self.request.match_info.get('contact_id')
        print('contacts.details.delete', contact_id)

        return web.json_response(status=204)

    @docs(tags=['contacts'], summary='Fetch contact details')
    @response_schema(ContactResponseSchema(), 200)
    async def get(self):
        contact_id = self.request.match_info.get('contact_id')
        print('contacts.details.get', contact_id)

        return web.json_response(status=200)
