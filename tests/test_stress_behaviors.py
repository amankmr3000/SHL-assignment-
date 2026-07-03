from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def post(text):
    return client.post("/chat", json={"messages":[{"role":"user","content":text}]}).json()

def names(r):
    return [x["name"].lower() for x in r["recommendations"]]

def test_finance_graduate():
    r = post("Graduate finance analyst role needing numerical reasoning and personality")
    ns = names(r)
    assert any("numerical" in n or "verify" in n for n in ns)
    assert any("accounting" in n or "statistics" in n or "graduate" in n for n in ns)

def test_admin_assistant():
    r = post("Administrative assistant role requiring Microsoft Excel and Word skills")
    ns = names(r)
    assert any("excel" in n for n in ns)
    assert any("word" in n for n in ns)

def test_contact_center():
    r = post("Hiring contact center agents with spoken English and customer service skills")
    ns = names(r)
    assert any("customer" in n or "contact" in n or "svar" in n for n in ns)

def test_leadership():
    r = post("Need leadership assessment for senior managers and executives")
    ns = names(r)
    assert any("opq" in n for n in ns)
    assert len(r["recommendations"]) <= 10

def test_rust_networking():
    r = post("Hiring a senior Rust systems engineer with Linux and networking experience")
    ns = names(r)
    assert any("linux" in n or "network" in n or "automata" in n for n in ns)

def test_add_personality_followup():
    r = client.post("/chat", json={"messages":[
        {"role":"user","content":"Hiring Java backend developer with Spring"},
        {"role":"assistant","content":"Here are recommendations."},
        {"role":"user","content":"Actually add personality tests"}
    ]}).json()
    assert any("opq" in n for n in names(r))

def test_no_recommendation_for_vague_first_turn():
    r = post("Need hiring solution")
    assert r["recommendations"] == []
