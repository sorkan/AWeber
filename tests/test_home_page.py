from app import app

def test_home_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b"Widgets Factory" in response.data


def test_create_new_widget():
    response = app.test_client().get('/add')

    assert response.status_code == 200
    assert b"Add new Widget" in response.data
    assert b"Num of parts" in response.data

