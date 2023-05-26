import pytest
from flask import Flask
from flask.testing import FlaskClient

from main import app

@pytest.fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client

    
def test_web_predict_1(client: FlaskClient):
    response = client.post('/predict', data={
        'Q1': '0',
        'Q2': '0',
        'Q3': '0',
        'Q4': '0',
        'Q5': '0',
        'Q6': '0',
        'Q7': '0',
        'Q8': '0',
        'Q9': '0',
        'Q10': '0',
        'Q11': '0'
    })
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == '/result?result=Not+Depressed'

def test_web_predict_2(client: FlaskClient):
    response = client.post('/predict', data={
        'Q1': '2',
        'Q2': '2',
        'Q3': '3',
        'Q4': '3',
        'Q5': '2',
        'Q6': '1',
        'Q7': '1',
        'Q8': '3',
        'Q9': '0',
        'Q10': '1',
        'Q11': '0'
    })
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == '/result?result=Depressed'

        
def test_web_predict_3(client: FlaskClient):
    response = client.post('/predict', data={
        'Q1': '3',
        'Q2': '3',
        'Q3': '3',
        'Q4': '3',
        'Q5': '3',
        'Q6': '3',
        'Q7': '3',
        'Q8': '3',
        'Q9': '3',
        'Q10': '3',
        'Q11': '3'
    })
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == '/result?result=Severely+Depressed'


def test_app_predict_1(client: FlaskClient):
    data = {
        "responses": ["3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3"]
    }

    response = client.post('/appPredict', json=data)
    assert response.status_code == 200
    assert b"Severely Depressed" in response.data


def test_app_predict_2(client: FlaskClient):
    data = {
        "responses": ["2", "2", "3", "3", "2", "1", "1", "3", "0", "1", "0"]
    }

    response = client.post('/appPredict', json=data)
    assert response.status_code == 200
    assert b"Depressed" in response.data

def test_app_predict_3(client: FlaskClient):
    data = {
        "responses": ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    }

    response = client.post('/appPredict', json=data)
    assert response.status_code == 200
    assert b"Not Depressed" in response.data

def test_home_route(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Find your depression level!" in response.data

def test_web_result(client: FlaskClient):
    response = client.get('/result?result=Not+Depressed')
    assert response.status_code == 200
    assert b"You are not suffering from depression." in response.data