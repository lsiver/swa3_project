import pytest
import json
from unittest.mock import patch, Mock
import time

'''
Integration tests!
'''
class TestSimulationEndpoint:
    def test_simulation_success(self, client):
        payload = {
            'component_a': 'Toluene',
            'component_b': 'Benzene',
            'feed_composition':0.8,
            'distillate_purity':0.95,
            'bottoms_purity': 0.05,
            'pressure': 1.0,
            'reflux_ratio': 4.0
        }

        response = client.post('/api/simulate',data=json.dumps(payload),content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] == True
        assert 'results' in data
        assert 'Nmin' in data['results']
        assert 'Rmin' in data['results']
        assert 'stages' in data['results']
        assert data['results']['stage_count'] > 0

    def test_simulation_invalid_parameters(self,client):
        payload = {
            'component_a': 'ComponentThatDoesNotExistInDB',
            'component_b': 'Benzene',
            'feed_composition':0.8,
            'distillate_purity':0.95,
            'bottoms_purity': 0.05,
            'pressure': 1.0,
            'reflux_ratio': 4.0
        }

        response = client.post('/api/simulate',data=json.dumps(payload),content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data

class TestScrapingIntegration:
    @patch('tasks.build_antoine_list_oneshot')
    def test_scrape_endpoint_queues_task(self, mock_scraper, client, celery_worker):
        mock_scraper.return_value = None
        response = client.post('/api/rescrapeAntoine',data=json.dumps({'flag':1}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'task_id' in data

        assert mock_scraper.called

    def test_task_status_endpoint(self,client,celery_worker):
        with patch('tasks.build_antoine_list_oneshot'):
            response = client.post('/api/rescrapeAntoine',data=json.dumps({'flag':1}),content_type = 'application/json')
            task_id = json.loads(response.data)['task_id']

            response = client.get(f'/api/task-status/{task_id}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'state' in data
            assert data['state'] in ['PENDING', 'SUCCESS', 'FAILURE']

