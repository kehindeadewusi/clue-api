
def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello."}


def test_index(client):
    response = client.get('/')
    assert b"Hello" in response.data


def test_invalid_date_range(client):
    """Test the multiply route with valid input."""
    response = client.get('reports/monthly-sales-summary?start_date=2025-01-01&end_date=2024-01-01')
    assert response.status_code == 400
