from aiohttp import web

from .views.auth import signin, signup
from .views.contacts import ContactDetails, Contacts
from .views.users import MeDetails, UserDetails


def setup_routes(app):
    app.add_routes([
        web.post('/api/auth/signup/', signup),
        web.post('/api/auth/signin/', signin),

        web.view('/api/contacts/', Contacts),
        web.view(r'/api/contacts/{contact_id:\d+}/', ContactDetails),

        web.view(r'/api/users/{user_id:\d+}/', UserDetails),
        web.view('/api/me/', MeDetails)
    ])
