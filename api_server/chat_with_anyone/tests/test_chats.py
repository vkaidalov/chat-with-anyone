from .conftest import TOKEN


async def test_get_list_chats(cli, chat):
    response_json = [{'id': 1, 'name': 'test_data'}]
    resp = await cli.get('/api/chats/', headers={'Authorization': TOKEN})

    assert resp.status == 200
    assert await resp.json() == response_json


async def test_get_list_chats_with_param(cli, chat):
    response_json = [{'id': 1, 'name': 'test_data'}]

    resp = await cli.get('/api/chats/?page=1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/chats/?page_size=1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/chats/?page=wrong_param',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/chats/?page=2',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == []

    resp = await cli.get('/api/chats/?page=-1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/chats/?page_size=-1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json


async def test_create_chat(cli, user):
    resp = await cli.post('/api/chats/', json={'name': 'test_data'},
                          headers={'Authorization': TOKEN})
    assert resp.status == 201


async def test_add_user_into_chat(cli, additional_user, additional_chat):
    resp = await cli.post('/api/chats/1/users/', json={'user_id': 2},
                          headers={'Authorization': TOKEN})

    assert resp.status == 201

    resp = await cli.post('/api/chats/3/users/', json={'user_id': 2},
                          headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"Chat with ID \\"3\\" was not found"}'

    resp = await cli.post('/api/chats/2/users/', json={'user_id': 2},
                          headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "You have not been ' \
                                'assigned with provided chat"}'

    resp = await cli.post('/api/chats/1/users/', json={'user_id': 3},
                          headers={'Authorization': TOKEN})

    assert resp.status == 400
    assert await resp.text() == '{"message": ' \
                                '"Provided chat_id or user_id is invalid"}'

    resp = await cli.post('/api/chats/1/users/', json={'user_id': 1},
                          headers={'Authorization': TOKEN})

    assert resp.status == 400
    assert await resp.text() == '{"message": ' \
                                '"User with ID \\"1\\" already exists"}'


async def test_delete_user_from_chat(cli, additional_user, additional_chat):
    resp = await cli.delete('/api/chats/2/users/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": ' \
                                '"Deleting another user is forbidden"}'

    resp = await cli.delete('/api/chats/3/users/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"Chat with ID \\"3\\" was not found"}'

    resp = await cli.delete('/api/chats/2/users/1',
                            headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"User with ID \\"1\\" does not exist in chat"}'

    resp = await cli.delete('/api/chats/1/users/1',
                            headers={'Authorization': TOKEN})

    assert resp.status == 204


async def test_get_all_messages_from_chat(cli, additional_chat, message):
    response_json = [{'id': 1, 'text': 'test_data', 'username': 'test_data',
                      'created_at': '01:00 PM'}]

    resp = await cli.get('/api/chats/1/messages/',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/chats/3/messages/',
                         headers={'Authorization': TOKEN})
    assert resp.status == 404
    assert await resp.text() == '{"message": "Chat not found."}'

    resp = await cli.get('/api/chats/2/messages/',
                         headers={'Authorization': TOKEN})
    assert resp.status == 403
    assert await resp.text() == '{"message": "Getting messages is forbidden. ' \
                                'User is not in chat."}'


async def test_create_message(cli, additional_chat):
    resp = await cli.post('/api/chats/1/messages/', json={'text': 'test_data'},
                          headers={'Authorization': TOKEN})

    assert resp.status == 201

    resp = await cli.post('/api/chats/2/messages/', json={'text': 'test_data'},
                          headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Posting messages is forbidden. ' \
                                'User is not in chat."}'


async def test_update_message(cli, additional_message):
    resp = await cli.patch('/api/chats/1/messages/1',
                           json={'text': 'test_data'},
                           headers={'Authorization': TOKEN})

    assert resp.status == 204

    resp = await cli.patch('/api/chats/1/messages/2',
                           json={'text': 'test_data'},
                           headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"Message not found. Incorrect id"}'

    resp = await cli.patch('/api/chats/2/messages/2',
                           json={'text': 'test_data'},
                           headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Changing another user\'s ' \
                                'message is prohibited"}'


async def test_delete_message(cli, additional_message):
    resp = await cli.delete('/api/chats/1/messages/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"Message not found. Incorrect id"}'

    resp = await cli.delete('/api/chats/2/messages/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Deleting another user\'s ' \
                                'message is prohibited"}'

    resp = await cli.delete('/api/chats/1/messages/1',
                            headers={'Authorization': TOKEN})

    assert resp.status == 204
