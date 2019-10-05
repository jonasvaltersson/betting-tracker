def test_get_status(test_client):
    response = test_client.get('v1/status').json
    assert False