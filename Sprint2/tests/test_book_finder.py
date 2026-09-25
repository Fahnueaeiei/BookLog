"""Tests for src/book_finder.py (Data Access Layer).

requests.get is monkeypatched throughout, so these tests never hit
the real network — fast, deterministic, and safe to run in CI without
a Google Books API key.
"""

import pytest
import requests

from src.book_finder import BookFinder
from src.exceptions import APIError


class FakeResponse:
    """Stands in for requests.Response in these tests."""

    def __init__(self, json_data=None, status_code=200, raise_json_error=False):
        self._json_data = json_data
        self.status_code = status_code
        self._raise_json_error = raise_json_error

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        if self._raise_json_error:
            raise ValueError("not valid json")
        return self._json_data


SAMPLE_VOLUME = {
    "id": "abc123",
    "volumeInfo": {
        "title": "Deep Work",
        "authors": ["Cal Newport"],
        "description": "Rules for focused success.",
        "publishedDate": "2016-01-05",
        "categories": ["Self-Help"],
        "imageLinks": {"thumbnail": "https://example.com/deep-work.jpg"},
        "pageCount": 304,
    },
}


@pytest.fixture
def finder():
    return BookFinder(api_key="test-key")


class TestSearch:
    def test_search_returns_parsed_books(self, finder, monkeypatch):
        def fake_get(url, params=None, timeout=None):
            assert params["q"] == "intitle:deep work"
            return FakeResponse(json_data={"items": [SAMPLE_VOLUME]})

        monkeypatch.setattr(requests, "get", fake_get)

        results = finder.search("title", "deep work")
        assert len(results) == 1
        assert results[0].title == "Deep Work"
        assert results[0].authors == ["Cal Newport"]
        assert results[0].published_year == 2016

    def test_search_no_results_returns_empty_list(self, finder, monkeypatch):
        monkeypatch.setattr(
            requests, "get", lambda *a, **k: FakeResponse(json_data={})
        )
        assert finder.search("title", "zzzznonexistent") == []

    def test_search_invalid_field_raises_value_error(self, finder):
        with pytest.raises(ValueError):
            finder.search("isbn", "12345")

    def test_search_uses_correct_prefix_per_field(self, finder, monkeypatch):
        seen_queries = []

        def fake_get(url, params=None, timeout=None):
            seen_queries.append(params["q"])
            return FakeResponse(json_data={"items": []})

        monkeypatch.setattr(requests, "get", fake_get)
        finder.search("author", "cal newport")
        finder.search("genre", "productivity")

        assert seen_queries == [
            "inauthor:cal newport",
            "subject:productivity",
        ]


class TestGetDetails:
    def test_get_details_returns_book(self, finder, monkeypatch):
        monkeypatch.setattr(
            requests, "get", lambda *a, **k: FakeResponse(json_data=SAMPLE_VOLUME)
        )
        book = finder.get_details("abc123")
        assert book.book_id == "abc123"
        assert book.page_count == 304


class TestParseVolumeDefaults:
    def test_missing_fields_get_safe_defaults(self, finder, monkeypatch):
        sparse_volume = {"id": "sparse-1", "volumeInfo": {}}
        monkeypatch.setattr(
            requests,
            "get",
            lambda *a, **k: FakeResponse(json_data={"items": [sparse_volume]}),
        )

        [book] = finder.search("title", "anything")
        assert book.title == "Untitled"
        assert book.authors == []
        assert book.categories == []
        assert book.description is None
        assert book.cover_url is None
        assert book.page_count is None


class TestErrorHandling:
    def test_timeout_raises_api_error(self, finder, monkeypatch):
        def fake_get(*args, **kwargs):
            raise requests.Timeout()

        monkeypatch.setattr(requests, "get", fake_get)
        with pytest.raises(APIError):
            finder.search("title", "anything")

    def test_connection_error_raises_api_error(self, finder, monkeypatch):
        def fake_get(*args, **kwargs):
            raise requests.ConnectionError()

        monkeypatch.setattr(requests, "get", fake_get)
        with pytest.raises(APIError):
            finder.search("title", "anything")

    def test_http_error_status_raises_api_error(self, finder, monkeypatch):
        monkeypatch.setattr(
            requests, "get", lambda *a, **k: FakeResponse(status_code=404)
        )
        with pytest.raises(APIError):
            finder.get_details("does-not-exist")

    def test_unparseable_json_raises_api_error(self, finder, monkeypatch):
        monkeypatch.setattr(
            requests,
            "get",
            lambda *a, **k: FakeResponse(raise_json_error=True),
        )
        with pytest.raises(APIError):
            finder.search("title", "anything")


class TestApiKeyHandling:
    def test_api_key_included_in_params_when_set(self, finder, monkeypatch):
        seen_params = {}

        def fake_get(url, params=None, timeout=None):
            seen_params.update(params)
            return FakeResponse(json_data={"items": []})

        monkeypatch.setattr(requests, "get", fake_get)
        finder.search("title", "anything")
        assert seen_params.get("key") == "test-key"

    def test_no_api_key_omits_key_param(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_BOOKS_API_KEY", raising=False)
        finder_without_key = BookFinder(api_key=None)

        seen_params = {}

        def fake_get(url, params=None, timeout=None):
            seen_params.update(params)
            return FakeResponse(json_data={"items": []})

        monkeypatch.setattr(requests, "get", fake_get)
        finder_without_key.search("title", "anything")
        assert "key" not in seen_params