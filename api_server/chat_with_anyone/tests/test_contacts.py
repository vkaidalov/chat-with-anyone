from .conftest import TOKEN


async def test_create_contact(cli, user, additional_user):
    resp = await cli.post('/api/users/1/contacts/',
                          headers={'Authorization': TOKEN},
                          json={'contact_id': 2})

    assert resp.status == 201

    resp = await cli.post('/api/users/2/contacts/',
                          headers={'Authorization': TOKEN},
                          json={'contact_id': 2})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Posting to other\'s ' \
                                'contact list is forbidden."}'

    resp = await cli.post('/api/users/1/contacts/',
                          headers={'Authorization': TOKEN},
                          json={'contact_id': 2})

    assert resp.status == 400
    assert await resp.text() == '{"message": "\'contact_id\' already exists"}'

    resp = await cli.post('/api/users/1/contacts/',
                          headers={'Authorization': TOKEN},
                          json={'contact_id': 3})

    assert resp.status == 400
    assert await resp.text() == '{"message": ' \
                                '"Specified \'contact_id\' is invalid."}'


async def test_get_contacts(cli, user, contact):
    response_json = [{"first_name": "test_data2", "id": 2,
                      "last_name": "test_data2", "username": "test_data2"}]

    resp = await cli.get('/api/users/1/contacts/',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/2/contacts/',
                         headers={'Authorization': TOKEN})
    assert resp.status == 403
    assert await resp.text() == '{"message": "Getting other\'s ' \
                                'contact list is forbidden."}'


async def test_delete_contact(cli, user, contact):
    resp = await cli.delete('/api/users/1/contacts/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 204

    resp = await cli.delete('/api/users/1/contacts/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": ' \
                                '"Contact with ID \\"2\\" already deleted"}'

    resp = await cli.delete('/api/users/2/contacts/3',
                            headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Deleting from other\'s ' \
                                'contact list is forbidden"}'
