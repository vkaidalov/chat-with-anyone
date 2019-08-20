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


class UserDetails(web.View):

    async def _validate_user(self):
        # for midleware in future ===>
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
        # <=== for midleware in future
        return user

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
    @response_schema(UserResponseSchema(), 200)
    async def get(self):
        user = await UserDetails._validate_user(self)

        request_user_id = self.request.match_info.get('user_id')
        request_user = await User.get(int(request_user_id))

        if request_user is None:
            raise web.HTTPNotFound(
                body=json.dumps({'message': 'Invalid id'}),
                content_type='application/json'
            )

        if user.id == request_user.id:
            try:
                return web.json_response(
                    UserResponseSchema().dump(request_user.to_dict()).data,
                    status=200
                )
            except Exception as e:
                print(type(e))
                print('Something went wrong :(')
        else:
            try:
                return web.json_response( 
                    UserResponseSchema().dump(request_user.to_dict()).data,
                    status=200
                )
            except Exception as e:
                print(type(e))
                print('Something went wrong :(')


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
    @response_schema(UserResponseSchema(), 200)
    async def patch(self):
        user = await UserDetails._validate_user(self)
        request_user_id = int(self.request.match_info.get('user_id'))

        if user.id != request_user_id:
            return web.json_response({"message": "Provided token is invalid."}, status=403)
        
        else:
            data = await self.request.json()
            try:
                await user.update(
                    username=data.get('username'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                ).apply()
                return web.json_response({}, status=200)
            except Exception as e:
                print(type(e))
                print('Something went wrong :(')

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
        user = await UserDetails._validate_user(self)
        request_user_id = int(self.request.match_info.get('user_id'))

        if user.id != request_user_id:
            return web.json_response({"message": "Provided token is invalid."}, status=403)
        else:
            try:
                await user.delete()
                return web.json_response(status=200)   
            except Exception as e: 
                print(type(e))
                print('Something went wrong :(') 


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
