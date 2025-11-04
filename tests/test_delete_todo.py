import os
import tempfile
import importlib

def test_delete_todo():
    db = tempfile.NamedTemporaryFile(delete=False)
    db_path = db.name
    db.close()
    os.environ['DB_PATH'] = db_path

    app_module = importlib.import_module('app')
    importlib.reload(app_module)
    app = app_module.app
    app_module.init_db()
    app.testing = True

    client = app.test_client()

    # Registreerime ja logime sisse
    client.post('/api/register', json={'username': 'liis', 'password': 'saladus'})
    client.post('/api/login', json={'username': 'liis', 'password': 'saladus'})

    # Lisame ülesande
    client.post('/api/todos', json={'title': 'Katsetus', 'description': 'Testimiseks'})

    # Kontrollime, et on olemas
    r = client.get('/api/todos')
    todo_id = r.get_json()['todos'][0]['id']

    # Kustutame ülesande
    r = client.delete(f'/api/todos/{todo_id}')
    assert r.is_json and r.get_json()['success'] is True

    # Kontrollime, et enam ei ole
    r = client.get('/api/todos')
    assert len(r.get_json()['todos']) == 0
