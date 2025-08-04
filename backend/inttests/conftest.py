import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app as flask_app
from tasks import celery, scrape_antoine_data

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def celery_app(monkeypatch):
    celery.conf.task_always_eager = True
    celery.conf.task_eager_propagates = True
    celery.conf.task_store_eager_result = True
    celery.conf.broker_url = 'memory://'
    celery.conf.result_backend = 'cache+memory://'

    yield celery
    celery.conf.task_always_eager = False
    celery.conf.task_eager_propagates = False
    celery.conf.task_store_eager_result = False

@pytest.fixture
def celery_worker(celery_app):
    return celery_app