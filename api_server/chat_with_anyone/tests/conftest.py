import argparse
from datetime import datetime

import pathlib
import pytest
from trafaret_config import commandline
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from passlib.hash import bcrypt

from utils import TRAFARET
from ..routes import setup_routes
from ..middlewares import setup_middlewares
from ..db import db
from ..models.user import User
from ..models.contact import Contact
from ..models.group_room import GroupRoom
from ..models.group_membership import GroupMembership
from ..models.group_message import GroupMessage

BASE_DIR = pathlib.Path(__file__).parents[2]
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'test_chat_with_anyone'
TOKEN = 'EMgHRURmDq8xjXVULw7A7fD1ZvBpR9MKhgSUZ5U8'


@pytest.fixture
def create_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    return config


@pytest.fixture
def cli(loop, aiohttp_client, create_config):
    config = create_config
    app = web.Application(middlewares=[db])
    app['config'] = config
    db.init_app(app, config=config["postgres"])
    setup_middlewares(app)
    setup_routes(app)
    setup_aiohttp_apispec(app)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def gino_db(cli):
    return cli.app['db']


@pytest.fixture
async def tables(gino_db):
    await gino_db.gino.create_all()

    yield

    await gino_db.gino.drop_all()


@pytest.fixture
async def user(tables):
    await User.create(
        username='test_data',
        email='test_data@gmail.com',
        password=bcrypt.hash('test_data'),
        first_name='test_data',
        last_name='test_data',
        token=TOKEN,
        is_active=True
    )


@pytest.fixture
async def additional_user(user):
    await User.create(
        username='test_data2',
        email='test_data2@gmail.com',
        password=bcrypt.hash('test_data2'),
        first_name='test_data2',
        last_name='test_data2',
        token=TOKEN[::-1],
        is_active=True
    )


@pytest.fixture
async def contact(additional_user):
    await Contact.create(
        owner_id=1,
        contact_id=2
    )


@pytest.fixture
async def chat(user):
    created_chat = await GroupRoom.create(
        name='test_data'
    )

    await GroupMembership.create(
        room_id=created_chat.id,
        user_id=1
    )


@pytest.fixture
async def additional_chat(additional_user, chat):
    created_chat = await GroupRoom.create(
        name='test_data'
    )

    await GroupMembership.create(
        room_id=created_chat.id,
        user_id=2
    )


@pytest.fixture
async def message(chat):
    await GroupMessage.create(
        text="test_data",
        room_id=1,
        user_id=1,
        created_at=datetime(year=2019, month=10, day=2,
                            hour=13, minute=0, second=0)
    )


@pytest.fixture
async def additional_message(message):
    await GroupMessage.create(
        text="test_data2",
        room_id=1,
        user_id=1,
        created_at=datetime(year=2019, month=10, day=2,
                            hour=13, minute=0, second=0)
    )


@pytest.fixture
async def message_in_additional_chat(additional_chat, message):
    await GroupMessage.create(
        text="test_data2",
        room_id=2,
        user_id=2,
        created_at=datetime(year=2019, month=10, day=2,
                            hour=13, minute=0, second=0)
    )
