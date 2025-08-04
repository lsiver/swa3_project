import pytest
import sys
import os
from celery import Celery

#parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app as flask_app
from tasks import celery

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def celery_app():
    celery.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
        broker_url='memory://',
        result_backend='cache+memory://'
    )
    return celery

@pytest.fixture
def celery_worker(celery_app):
    celery_app.Task.__call__ = celery_app.Task.run
    return celery_app