# async def test_get_list_chats(cli, tables):
#     resp = await cli.get('/api/chats/')
#     assert resp.status == 200
#     assert await resp.json() == []
#
#
# async def test_post_chats(cli, tables):
#     resp = await cli.post('/api/chats/', json={'name': 'value'})
#     assert resp.status == 201
#     assert await resp.json() == {}
