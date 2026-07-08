def test_homepage_loads():
    import app

    client = app.app.test_client()
    res = client.get("/")

    assert res.status_code == 200


def test_empty_product_returns_error_page(monkeypatch):
    import app

    client = app.app.test_client()
    res = client.post("/", data={"product": ""})

    assert res.status_code == 200
    assert b"Missing product description" in res.data
