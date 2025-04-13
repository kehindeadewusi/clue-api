import pytest
from clue_oda.api import create_app


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
