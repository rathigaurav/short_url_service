# test_short_url_service.py

import pytest
from fastapi import HTTPException, status
from unittest.mock import MagicMock, patch
from api.metrics.metrics_service import MetricsService
from datetime import datetime, timedelta

@pytest.fixture
def metrics_service():
    return MetricsService(MagicMock(), MagicMock())

def test_generate_access_metrics(metrics_service):
    short_url = "https://shorty/Test123"
    mock_access_count = MagicMock(return_value=1)
    metrics_service.get_access_count_metric_from_db = mock_access_count
    result = metrics_service.generate_access_metrics(short_url)
    assert result == { "24_hr": 1, "1_week": 1, "all_time": 1}

def test_generate_access_metrics_short_url_does_not_exist(metrics_service):
    short_url = "https://shorty/Test123"
    mock_document = MagicMock(return_value=None)
    metrics_service.mongodb_service.fetch_long_url = mock_document
    with pytest.raises(HTTPException):
        metrics_service.generate_access_metrics(short_url)