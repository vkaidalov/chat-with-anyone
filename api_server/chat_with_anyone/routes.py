from aiohttp import web

from .views.auth import signin, signup
from .views.contacts import ContactDetails, Contacts
from .views.users import MeDetails, UserDetails
from .views.chats import Chats, ChatMessages, ChatMessageDetails


def setup_routes(app):
    app.add_routes([
        web.post('/api/auth/signup/', signup),
        web.post('/api/auth/signin/', signin),

        web.view('/api/contacts/', Contacts),
        web.view(r'/api/contacts/{contact_id:\d+}/', ContactDetails),

        web.view(r'/api/users/{user_id:\d+}/', UserDetails),
        web.view('/api/me/', MeDetails),

        web.view('/api/chats/', Chats),
        web.view(r'/api/chats/{chat_id:\d+}/messages/', ChatMessages),
        web.view(
            r'/api/chats/{chat_id:\d+}/messages/{message_id:\d+}/',
            ChatMessageDetails
        ),
    ])
