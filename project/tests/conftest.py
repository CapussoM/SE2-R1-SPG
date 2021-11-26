import pytest
from project import create_app, db
from project.models import User, Product

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    # Insert user data
    user1 = User(name='Pat', surname='Farmer', email='patfarmer@gmail.com', role='F', password='FlaskIsAwesome', company="Pat's Farm")
    user2 = User(name='Matt', surname='Smith', email='mattsmith@gmail.com', role='S', password='UserPassword', company="")
    user3 = User(name='Ella', surname='Clint', email='ellaclint@gmail.com', role='C', password='UserPassword', wallet=30)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='function')
def login_farmer_user(test_client):
    test_client.post('/login',
                     data=dict(email='patfarmer@gmail.com', password='FlaskIsAwesome'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_employee_user(test_client):
    test_client.post('/login',
                     data=dict(email='mattsmith@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_employee_user(test_client):
    test_client.post('/login',
                     data=dict(email='ellaclint@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)