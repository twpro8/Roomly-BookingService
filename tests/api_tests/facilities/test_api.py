from tests.conftest import read_json


async def test_add_facilities(ac):
    for facility in read_json("mock_facilities"):
        response = await ac.post(
            "/facilities",
            json=facility,
        )
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)
        assert result["data"]["title"] == facility["title"]


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200

    mock_data = read_json("mock_facilities")
    response_data = response.json()

    mock_titles = {item["title"] for item in mock_data}
    response_titles = {item["title"] for item in response_data}

    assert mock_titles == response_titles
    assert isinstance(response.json(), list)
