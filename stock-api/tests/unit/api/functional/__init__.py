import pytest

from app import create_app

@pytest.fixture(scope="module")
def client():
    """Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """

    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client