from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, make_mocked_request
from aiohttp import web

from ..routes import setup_routes
from ..models.group_room import GroupRoom


class ChatTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        setup_routes(app)
        return app

    @unittest_run_loop
    async def test_get_list_chats(self):
        req = make_mocked_request('GET', '/api/users',
                                  headers={'Authorization': 'token'})
        assert req.headers.get('Authorization') == 'token'
        chats = str([GroupRoom()])
        resp = web.Response(body=bytes(chats, 'utf-8'))
        assert resp.status == 200
        assert resp.body.decode() == chats

    async def test_post_chats(cli):
        pass
        # resp = await cli.post('/api/chats/', json={'key': 'value'})
        # assert resp.status == 201
        # assert await resp.json() == {}
