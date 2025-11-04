import os
import tempfile
import importlib

def test_change_password():
    db = tempfile.NamedTemporaryFile(delete=False)
    db_path = db.name
    db.close()
    os.environ['DB_PATH'] = db_path

    app_module = importlib.import_module('app')
    importlib.reload(app_module)
    app = app_module.app
    app_module.init_db()
    app.testing = True

    with app.test_client() as client:
        client.post('/api/register', json={'username': 'fstez', 'password': '123123'})
        client.post('/api/login', json={'username': 'fstez', 'password': '123123'})  # Correct password

        r = client.post('/api/change-password', json={'old_password': '123123', 'new_password': 'newpass'})
        data = r.get_json()
        print("DEBUG:", data)  
        assert data['success'] is True, f"Unexpected response: {data}"

        client.post('/api/logout')
        r = client.post('/api/login', json={'username': 'fstez', 'password': 'newpass'})
        assert r.get_json()['success'] is True
