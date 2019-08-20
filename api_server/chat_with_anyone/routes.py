from aiohttp import web

from .views.auth import signin, signup
from .views.users import UserDetails, ContactDetails, Contacts
from .views.chats import Chats, ChatMessages, ChatMessageDetails


def setup_routes(app):
    app.add_routes([
        web.post('/api/auth/signup/', signup),
        web.post('/api/auth/signin/', signin),

        web.view(r'/api/users/{user_id:\d+}/contacts/', Contacts),
        web.view(
            r'/api/users/{user_id:\d+}/contacts/{contact_id:\d+}/',
            ContactDetails
        ),

        web.view(r'/api/users/{user_id:\d+}/', UserDetails),

        web.view('/api/chats/', Chats),
        web.view(r'/api/chats/{chat_id:\d+}/messages/', ChatMessages),
        web.view(
            r'/api/chats/{chat_id:\d+}/messages/{message_id:\d+}/',
            ChatMessageDetails
        ),
    ])
