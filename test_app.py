from app import app, add


def test_add():
    assert add(2, 3) == 5


def test_index():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add_route():
    client = app.test_client()
    assert client.get("/add/2/2").get_json()["result"] == 4
