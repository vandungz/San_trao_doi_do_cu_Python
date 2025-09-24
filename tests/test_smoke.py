def test_homepage_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Skeleton Django" in response.content


