from aiohttp import web

from .views.auth import sign_in, sign_out, sign_up
from .views.chats import (ChatUserList, ChatMessageDetails, ChatMessages,
                          Chats, ChatUserDetails)
from .views.email_confirmation import email_token_confirmation
from .views.users import ContactDetail, ContactList, UserDetail, UserList


def setup_routes(app):
    app.add_routes([
        web.post('/api/signup', sign_up),
        web.post('/api/sign-in', sign_in),
        web.post(r'/api/users/{user_id:\d+}/sign-out', sign_out),

        web.get(r'/api/email-confirmation/{token}', email_token_confirmation,
                allow_head=False
                ),

        web.view(r'/api/users/{user_id:\d+}/contacts/', ContactList),
        web.view(
            r'/api/users/{user_id:\d+}/contacts/{contact_id:\d+}',
            ContactDetail
        ),

        web.view(r'/api/users/', UserList),
        web.view(r'/api/users/{user_id:\d+}', UserDetail),

        web.view('/api/chats/', Chats),
        web.view(r'/api/chats/{chat_id:\d+}/users/', ChatUserList),
        web.view(
            r'/api/chats/{chat_id:\d+}/users/{user_id:\d+}/',
            ChatUserDetails
        ),

        web.view(r'/api/chats/{chat_id:\d+}/messages/', ChatMessages),
        web.view(
            r'/api/chats/{chat_id:\d+}/messages/{message_id:\d+}',
            ChatMessageDetails
        ),
    ])
