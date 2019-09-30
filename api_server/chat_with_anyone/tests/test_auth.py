from .conftest import TOKEN


async def test_sign_up(cli, user):
    resp = await cli.post('/api/signup',
                          json={"email": "test_data@gmail.com",
                                "username": "test_data",
                                "password": "test_data",
                                "first_name": "test_data",
                                "last_name": "test_data"}
                          )
    assert resp.status == 400
    assert await resp.text() == '{"message": ' \
                                '"Key (username)=(test_data) already exists."}'

    resp = await cli.post('/api/signup',
                          json={"email": "test_value",
                                "username": "test_value",
                                "password": "test_value",
                                "first_name": "test_value",
                                "last_name": "test_value"}
                          )
    assert resp.status == 422
    assert await resp.text() == '{"email": ["Not a valid email address."]}'

    # resp = await cli.post('/api/signup',
    #                       json={"email": "test_value@gmail.com",
    #                             "username": "test_value",
    #                             "password": "test_value",
    #                             "first_name": "test_value",
    #                             "last_name": "test_value"}
    #                       )
    # assert resp.status == 201


async def test_sign_in(cli, user):
    resp = await cli.post('/api/sign-in',
                          json={"email": "test_value@gmail.com",
                                "password": "test_data"}
                          )
    assert resp.status == 400
    assert await resp.text() == '{"message": "Invalid credentials."}'

    resp = await cli.post('/api/sign-in',
                          json={"email": "test_data@gmail.com",
                                "password": "test_data"}
                          )
    assert resp.status == 200


async def test_sign_out(cli, user):
    resp = await cli.post('/api/users/2/sign-out',
                          headers={'Authorization': TOKEN})
    assert resp.status == 403
    assert await resp.text() == '{"message": "Invalid credentials"}'

    resp = await cli.post('/api/users/1/sign-out',
                          headers={'Authorization': TOKEN})
    assert resp.status == 200
