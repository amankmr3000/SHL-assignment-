from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def chat(text):
    return client.post("/chat", json={"messages":[{"role":"user","content":text}]}).json()

def test_vague_clarifies():
    r = chat("I need an assessment")
    assert r["recommendations"] == []

def test_refuses_legal():
    r = chat("Give me legal advice about firing someone")
    assert r["recommendations"] == []

def test_java_recommends():
    r = chat("Hiring a Java backend developer with Spring Boot Docker AWS and personality")
    names = [x["name"].lower() for x in r["recommendations"]]
    assert any("java" in x for x in names)
    assert any("spring" in x for x in names)
    assert all(x["url"].startswith("https://www.shl.com/") for x in r["recommendations"])

def test_compare():
    r = chat("What is the difference between OPQ32r and Verify Numerical?")
    names = [x["name"].lower() for x in r["recommendations"]]
    assert any("opq" in x for x in names)
    assert any("numerical" in x for x in names)

def test_schema():
    r = chat("Hiring finance graduate with numerical reasoning")
    assert set(r.keys()) == {"reply","recommendations","end_of_conversation"}
