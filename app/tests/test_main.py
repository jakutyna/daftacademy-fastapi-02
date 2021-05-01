from datetime import date

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert f'<h1>Hello! Today date is {str(date.today())}</h1>' in response.text
