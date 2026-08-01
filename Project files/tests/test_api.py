import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    res = client.get('/api/v1/health')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['version'] == '2.0.0'

def test_statistics_endpoint(client):
    res = client.get('/api/v1/statistics')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'success'
    assert 'total_predictions' in json_data['data']

def test_history_endpoint(client):
    res = client.get('/api/v1/history')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'success'
    assert isinstance(json_data['data'], list)
