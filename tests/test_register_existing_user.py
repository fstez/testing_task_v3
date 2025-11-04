import os
import tempfile
import importlib

def test_register_existing_user():
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

    # Esimene registreerimine (успешная)
    r = client.post('/api/register', json={'username': 'peeter', 'password': 'qwerty'})
    assert r.is_json and r.get_json()['success'] is True

    # Teine registreerimine (не должна пройти)
    r = client.post('/api/register', json={'username': 'peeter', 'password': 'qwerty'})
    assert r.is_json and r.get_json()['success'] is False
