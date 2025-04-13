import pytest, psycopg2
from clue_oda.api import create_app
from clue_oda.settings import DB_CONFIGS


@pytest.fixture
def app():
    app = create_app(testing=True)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_db_conn():
    DB_CONFIG = DB_CONFIGS.get("test")
    return psycopg2.connect(**DB_CONFIG)
