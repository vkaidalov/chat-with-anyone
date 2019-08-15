# Chat With Anyone API Server

## Setup (Ubuntu)

Create a virtual environment and install the requirements:

```bash
$ cd api_server
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt  # (venv) is supposed there and below
```

Install and run PostgreSQL:

```bash
$ sudo apt-get install postgresql-10
$ sudo service postgresql start
```

By default, the `postgres` user has no password. Let's set it:

```bash
$ sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

Run the PostgreSQL interactive shell:

```bash
$ psql -u postgres -h localhost
```

Create the database and the user, then quit from the shell:

```sql
CREATE DATABASE chat_with_anyone;
CREATE USER chat_with_anyone WITH PASSWORD 'chat_with_anyone';
GRANT ALL PRIVILEGES ON DATABASE chat_with_anyone to chat_with_anyone;
\q
```

Create new migration
```bash
alembic revision -m "<Message for migration>" --autogenerate --head head
```
Apply the migrations to fill the database with the needed tables:

```bash
$ alembic upgrade head
```

Now run the freaking server!

```bash
$ python main.py
```

Or use the `aiohttp-devtools` CLI to get such features as live reload
and rich debug information for incoming requests into your console:

```bash
$ adev runserver .
``` 

Now go to `/api/v1/docs` in your browser and get the Swagger UI to
explore this API.
