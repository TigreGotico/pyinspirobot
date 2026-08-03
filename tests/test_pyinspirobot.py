"""Tests for pyinspirobot, replaying recorded InspiroBot API responses.

No test in this module makes a network call. The fixtures under
tests/fixtures/ were recorded from the live InspiroBot API on 2026-08-03:

- normal_response.txt: GET https://inspirobot.me/api/?generate=true
- xmas_response.txt:   GET https://inspirobot.me/api/?generate=true&season=xmas
- image_sample.jpg:    binary body fetched from a URL returned by the request above
"""

import os
from unittest.mock import patch, Mock

import pytest

from pyinspirobot import InspiroBot, get_image, get_image_url

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def _read_fixture(name, mode="r"):
    with open(os.path.join(FIXTURES_DIR, name), mode) as f:
        return f.read()


def _fake_response(text=None, content=None, status_code=200):
    resp = Mock()
    resp.status_code = status_code
    if text is not None:
        resp.text = text
    if content is not None:
        resp.content = content

    def raise_for_status():
        if status_code >= 400:
            raise __import__("requests").HTTPError(f"{status_code} error")

    resp.raise_for_status.side_effect = raise_for_status
    return resp


class TestGetImageUrl:
    def test_happy_path(self):
        recorded = _read_fixture("normal_response.txt").strip()
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text=recorded)) as mocked:
            bot = InspiroBot()
            url = bot.get_image_url()

        assert url == recorded
        assert url.startswith("https://")
        args, kwargs = mocked.call_args
        assert kwargs["params"] == {"generate": "true"}
        assert kwargs["timeout"] == bot.timeout

    def test_season_xmas(self):
        recorded = _read_fixture("xmas_response.txt").strip()
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text=recorded)) as mocked:
            url = InspiroBot().get_image_url(season="xmas")

        assert url == recorded
        args, kwargs = mocked.call_args
        assert kwargs["params"] == {"generate": "true", "season": "xmas"}

    def test_protocol_relative_url_is_made_absolute(self):
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="//generated.inspirobot.me/a/x.jpg")):
            url = InspiroBot().get_image_url()

        assert url == "https://generated.inspirobot.me/a/x.jpg"

    def test_site_relative_url_is_made_absolute(self):
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="/a/x.jpg")):
            url = InspiroBot().get_image_url()

        assert url == "https://inspirobot.me/a/x.jpg"

    def test_empty_response_raises_value_error(self):
        # Regression test: previously an empty/malformed body was returned
        # as-is, only failing later (and confusingly) inside get_image().
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="")):
            with pytest.raises(ValueError):
                InspiroBot().get_image_url()

    def test_malformed_response_raises_value_error(self):
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="Service Unavailable")):
            with pytest.raises(ValueError):
                InspiroBot().get_image_url()

    def test_timeout_is_passed_to_request(self):
        recorded = _read_fixture("normal_response.txt").strip()
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text=recorded)) as mocked:
            InspiroBot(timeout=5).get_image_url()

        assert mocked.call_args.kwargs["timeout"] == 5

    def test_http_error_propagates(self):
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="", status_code=503)):
            with pytest.raises(Exception):
                InspiroBot().get_image_url()


class TestGetImage:
    def test_happy_path(self):
        recorded_url = _read_fixture("normal_response.txt").strip()
        image_bytes = _read_fixture("image_sample.jpg", mode="rb")

        url_response = _fake_response(text=recorded_url)
        image_response = _fake_response(content=image_bytes)

        with patch("pyinspirobot.requests.get", side_effect=[url_response, image_response]) as mocked:
            data = InspiroBot().get_image()

        assert data == image_bytes
        assert len(data) > 0
        assert mocked.call_count == 2
        second_call_args, second_call_kwargs = mocked.call_args_list[1]
        assert second_call_args[0] == recorded_url
        assert second_call_kwargs["timeout"] == InspiroBot().timeout

    def test_season_forwarded_to_url_request(self):
        recorded_url = _read_fixture("xmas_response.txt").strip()
        image_bytes = b"\xff\xd8\xff"  # minimal JPEG magic bytes

        url_response = _fake_response(text=recorded_url)
        image_response = _fake_response(content=image_bytes)

        with patch("pyinspirobot.requests.get", side_effect=[url_response, image_response]) as mocked:
            data = InspiroBot().get_image(season="xmas")

        assert data == image_bytes
        first_call_kwargs = mocked.call_args_list[0].kwargs
        assert first_call_kwargs["params"]["season"] == "xmas"

    def test_malformed_url_response_raises_before_second_request(self):
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text="")) as mocked:
            with pytest.raises(ValueError):
                InspiroBot().get_image()

        # get_image_url() must fail fast; no second request for the image itself.
        assert mocked.call_count == 1


class TestConvenienceFunctions:
    def test_get_image_url(self):
        recorded = _read_fixture("normal_response.txt").strip()
        with patch("pyinspirobot.requests.get", return_value=_fake_response(text=recorded)):
            assert get_image_url() == recorded

    def test_get_image(self):
        recorded_url = _read_fixture("normal_response.txt").strip()
        image_bytes = _read_fixture("image_sample.jpg", mode="rb")
        url_response = _fake_response(text=recorded_url)
        image_response = _fake_response(content=image_bytes)

        with patch("pyinspirobot.requests.get", side_effect=[url_response, image_response]):
            assert get_image() == image_bytes
