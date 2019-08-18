import json

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields

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
    pass


class ContactResponseSchema(Schema):
    pass


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


class Contacts(web.View):
    @docs(tags=['user'], summary='Create new contact')
    @request_schema(ContactRequestSchema(strict=True))
    @response_schema(ContactResponseSchema(), 200)
    async def post(self):
        user_id = self.request.match_info.get('user_id')
        data = await self.request.json()

        print('contacts.post.data', data)
        print('contacts.post.user_id', user_id)

        return web.json_response(status=201)

    @docs(tags=['user'], summary='Fetch list of contacts')
    @response_schema(ContactResponseSchema(), 200)
    async def get(self):
        user_id = self.request.match_info.get('user_id')
        query = self.request.query

        print('contacts.get.query', query)
        print('contacts.get.user_id', user_id)

        UserContact = User.alias()

        query = User.outerjoin(
            Contact, onclause=(User.id == Contact.owner_id)
        ).outerjoin(
            UserContact, onclause=(UserContact.id == Contact.contact_id)
        ).select().where(User.id == int(user_id))

        users = await query.gino.load(
            User.distinct(User.id).load(add_contact=UserContact)).all()

        if not users:
            raise web.HTTPNotFound(
                body=json.dumps({'message': 'Invalid id'}),
                content_type='application/json'
            )

        return web.json_response(
            UserResponseSchema().dump(
                [contact.to_dict() for contact in users[0].contacts],
                many=True
            ).data)


class ContactDetails(web.View):
    @docs(tags=['user'], summary='Delete contact')
    async def delete(self):
        user_id = self.request.match_info.get('user_id')
        contact_id = self.request.match_info.get('contact_id')

        print('contacts.details.delete.contact_id', contact_id)
        print('contacts.details.delete.user_id', user_id)

        return web.json_response(status=204)

    @docs(tags=['user'], summary='Fetch contact details')
    @response_schema(ContactResponseSchema(), 200)
    async def get(self):
        user_id = self.request.match_info.get('user_id')
        contact_id = self.request.match_info.get('contact_id')

        print('contacts.details.delete.contact_id', contact_id)
        print('contacts.details.delete.user_id', user_id)

        return web.json_response(status=200)
