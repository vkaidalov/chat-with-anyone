from .conftest import TOKEN


async def test_get_list_users(cli, user):
    resp = await cli.get('/api/users/', headers={'Authorization': TOKEN})
    response_json = [{"id": 1, "username": "test_data",
                      "first_name": "test_data", "last_name": "test_data"}]

    assert resp.status == 200
    assert await resp.json() == response_json


async def test_get_list_users_with_param(cli, user):
    response_json = [{"id": 1, "username": "test_data",
                      "first_name": "test_data", "last_name": "test_data"}]

    resp = await cli.get('/api/users/?username=test',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?first_name=test',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?last_name=test',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?page=1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?page_size=1',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?username=wrong_param',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == []

    resp = await cli.get('/api/users/?first_name=wrong_param',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == []

    resp = await cli.get('/api/users/?last_name=wrong_param',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == []

    resp = await cli.get('/api/users/?page=wrong_param',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/?page=2',
                         headers={'Authorization': TOKEN})
    assert resp.status == 200
    assert await resp.json() == []

    # resp = await cli.get('/api/users/?page=-1',
    #                      headers={'Authorization': TOKEN})
    # assert resp.status == 200
    # assert await resp.json() == response_json
    #
    # resp = await cli.get('/api/users/?page_size=-1',
    #                      headers={'Authorization': TOKEN})
    # assert resp.status == 200
    # assert await resp.json() == response_json


async def test_get_user_detail(cli, user):
    resp = await cli.get('/api/users/1',
                         headers={'Authorization': TOKEN})
    response_json = {"id": 1, "username": "test_data",
                     "first_name": "test_data", "last_name": "test_data"}

    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await cli.get('/api/users/2',
                         headers={'Authorization': TOKEN})

    assert resp.status == 404
    assert await resp.text() == '{"message": "User not found."}'


async def test_edit_user_profile(cli, user, additional_user):
    resp = await cli.patch('/api/users/1',
                           headers={'Authorization': TOKEN},
                           json={"username": "test_value",
                                 "first_name": "test_value",
                                 "last_name": "test_value"})

    assert resp.status == 204

    resp = await cli.patch('/api/users/2',
                           headers={'Authorization': TOKEN},
                           json={"username": "test_value",
                                 "first_name": "test_value",
                                 "last_name": "test_value"})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Patching other\'s ' \
                                'profile is forbidden."}'

    resp = await cli.patch('/api/users/2',
                           headers={'Authorization': TOKEN[::-1]},
                           json={"username": "test_value",
                                 "first_name": "test_value",
                                 "last_name": "test_value"})

    assert resp.status == 400
    assert await resp.text() == '{"message": "Key (username)=' \
                                '(test_value) already exists."}'


async def test_delete_user_profile(cli, user):
    resp = await cli.delete('/api/users/2',
                            headers={'Authorization': TOKEN})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Deleting other\'s ' \
                                'profile is forbidden."}'

    resp = await cli.delete('/api/users/1',
                            headers={'Authorization': TOKEN})

    assert resp.status == 204


async def test_change_password(cli, user, additional_user):
    resp = await cli.patch('/api/users/1/change-password',
                           headers={'Authorization': TOKEN},
                           json={"old_password": "test_data",
                                 "new_password": "test_value",
                                 "new_password_repeat": "test_wrong_value"})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Passwords do not match"}'

    resp = await cli.patch('/api/users/1/change-password',
                           headers={'Authorization': TOKEN},
                           json={"old_password": "test_value",
                                 "new_password": "test_value",
                                 "new_password_repeat": "test_value"})

    assert resp.status == 403
    assert await resp.text() == '{"message": "The old password ' \
                                'you entered doesn\'t match"}'

    resp = await cli.patch('/api/users/1/change-password',
                           headers={'Authorization': TOKEN},
                           json={"old_password": "test_data",
                                 "new_password": "test_value",
                                 "new_password_repeat": "test_value"})

    assert resp.status == 204

    resp = await cli.patch('/api/users/3/change-password',
                           headers={'Authorization': TOKEN},
                           json={"old_password": "test_data",
                                 "new_password": "test_value",
                                 "new_password_repeat": "test_value"})

    assert resp.status == 404
    assert await resp.text() == '{"message": "User not found"}'

    resp = await cli.patch('/api/users/2/change-password',
                           headers={'Authorization': TOKEN},
                           json={"old_password": "test_data",
                                 "new_password": "test_value",
                                 "new_password_repeat": "test_value"})

    assert resp.status == 403
    assert await resp.text() == '{"message": "Requested user_id doesn\'t ' \
                                'correspond current user_id"}'
