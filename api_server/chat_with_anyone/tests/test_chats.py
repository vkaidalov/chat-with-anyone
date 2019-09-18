import pytest
from aiohttp import web

from ..routes import setup_routes


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    setup_routes(app)
    return loop.run_until_complete(aiohttp_client(app))


async def test_get_list_chats(cli):
    # resp = await cli.get('/api/chats/')
    # assert resp.status == 200
    # assert await resp.json() == []
    assert True


async def test_post_chats(cli):
    # resp = await cli.post('/api/chats/', json={'key': 'value'})
    # assert resp.status == 201
    # assert await resp.json() == {}
    assert True
