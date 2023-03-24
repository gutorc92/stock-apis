import pytest

from app import create_app

@pytest.fixture(autouse=True, scope="module")
def client():
    """Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """

    flask_app = create_app()
    flask_app.config['TESTING'] = True

    print('passou aqui')

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
