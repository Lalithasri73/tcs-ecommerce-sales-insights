import pytest
from app import app

def test_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.json
    assert data['status'] == 'healthy'
    assert data['rows'] > 0

def test_kpis(client):
    response = client.get('/api/v1/kpis')
    assert response.status_code == 200
    data = response.json
    assert 'total_sales' in data
    assert data['orders'] > 0
