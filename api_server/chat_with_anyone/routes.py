from aiohttp import web

from .views.auth import sign_in, signup
from .views.chats import Chats, ChatMessages, ChatMessageDetails
from .views.users import UserDetail, ContactDetail, ContactList
from .views.email_confirmation import set_active, send_email


def setup_routes(app):
    app.add_routes([
        web.post('/api/auth/signup', signup),
        web.post('/api/auth/signin', sign_in),

        web.get(r'/api/email-confirmation/{token}', set_active),

        web.view(r'/api/users/{user_id:\d+}/contacts/', ContactList),
        web.view(
            r'/api/users/{user_id:\d+}/contacts/{contact_id:\d+}',
            ContactDetail
        ),

        web.view(r'/api/users/{user_id:\d+}', UserDetail),

        web.view('/api/chats/', Chats),
        web.view(r'/api/chats/{chat_id:\d+}/messages/', ChatMessages),
        web.view(
            r'/api/chats/{chat_id:\d+}/messages/{message_id:\d+}',
            ChatMessageDetails
        ),
        
    ])
