# test_short_url_service.py

import pytest
from fastapi import HTTPException, status
from unittest.mock import MagicMock, patch
from api.shortner.short_url_service import ShortUrlService
from datetime import datetime, timedelta

class DeleteResultMock:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count

@pytest.fixture
def short_url_service():
    return ShortUrlService(MagicMock(), MagicMock(), MagicMock())

def test_short_url_generator(short_url_service):
    base_url = "https://shorty/"
    short_url = short_url_service.short_url_generator()
    assert short_url.startswith(base_url)
    
    path = short_url.replace(base_url,"")
    assert path.isalnum()
    assert len(path) == 6


def test_get_long_url_from_db_found(short_url_service):
    short_url = "https://shorty/Test123"
    long_url = "https://example.com"
    expiration_time = int((datetime.utcnow() + timedelta(days=1)).timestamp()) * 1000

    mock_fetch_long_url = MagicMock(return_value={
        "long_url": long_url,
        "expiration_time": expiration_time,
    })
    short_url_service.mongodb_service.fetch_long_url = mock_fetch_long_url
    result = short_url_service.get_long_url_from_db(short_url)
    assert result == long_url

def test_get_long_url_from_db_when_short_url_has_expired(short_url_service):
    short_url = "https://shorty/Test123"
    long_url = "https://example.com"
    expiration_time = int((datetime.utcnow() - timedelta(days=1)).timestamp()) * 1000

    mock_fetch_long_url = MagicMock(return_value={
        "long_url": long_url,
        "expiration_time": expiration_time,
    })
    short_url_service.mongodb_service.fetch_long_url = mock_fetch_long_url
    with pytest.raises(HTTPException, match="400: {'error': 'short_url: https://shorty/Test123 has expired.'}"):
        short_url_service.get_long_url_from_db(short_url)

def test_get_long_url_from_db_when_short_url_not_found(short_url_service):
    short_url = "https://shorty/Test123"
    mock_fetch_long_url = MagicMock(return_value=None)
    short_url_service.mongodb_service.fetch_long_url = mock_fetch_long_url
    with pytest.raises(HTTPException, match="404: {'error': 'Cannot redirect. short_url: https://shorty/Test123 not found.'}"):
        short_url_service.get_long_url_from_db(short_url)
    
def test_get_long_url(short_url_service):
    short_url = "https://shorty/Test123"
    long_url = "https://example.com"
    mock_fetch_long_url = MagicMock(return_value=long_url)
    short_url_service.redis_service.get_long_url = mock_fetch_long_url
    result = short_url_service.get_long_url(short_url)
    assert result == long_url


def test_delete_short_url_from_db(short_url_service):
    short_url = "https://shorty/Test123"
    mock_delete_long_url = MagicMock(return_value=DeleteResultMock(1))
    short_url_service.mongodb_service.delete_short_url = mock_delete_long_url
    result = short_url_service.delete_short_url_from_db(short_url)
    assert result.deleted_count == 1