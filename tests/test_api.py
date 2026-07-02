from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get('/health').json() == {'status':'ok'}

def test_chat_schema():
    r = client.post('/chat', json={'messages':[{'role':'user','content':'Hiring a Java backend developer'}]})
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {'reply','recommendations','end_of_conversation'}
    assert isinstance(data['recommendations'], list)
