from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, make_mocked_request
from aiohttp import web

from ..routes import setup_routes
from ..models.user import User


class UserTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        setup_routes(app)
        return app

    @unittest_run_loop
    async def test_get_users(self):
        req = make_mocked_request('GET', '/api/users',
                                  headers={'Authorization': 'token'})
        assert req.headers.get('Authorization') == 'token'
        users = str([User(id=1, username='username')])
        resp = web.Response(body=bytes(users, 'utf-8'))
        assert resp.body.decode() == users
        assert resp.status == 200

