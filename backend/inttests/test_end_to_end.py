import pytest
from unittest.mock import patch, Mock
import json

class TestEndToEndWorkflow:
    @patch('tasks.build_antoine_list_oneshot')
    def test_complete_scraping_workflow_simple(self, mock_scraper, client, celery_app):
        mock_scraper.return_value = None

        response = client.post('/api/rescrapeAntoine', data=json.dumps({'flag': 1}), content_type='application/json')

        assert response.status_code == 200
        assert mock_scraper.called