from unittest.mock import patch, MagicMock
from collections.abc import Generator

import pytest
from requests import HTTPError

from src.fitbit import Fitbit
from src.models.fitbit import CreateFoodLogParams, UpdateFoodLogParams
from tests.data.json import (
    GET_FOOD_LOG_RESPONSE_JSON,
    CREATE_FOOD_LOG_PARAMS_JSON,
    CREATE_FOOD_LOG_RESPONSE_JSON,
    UPDATE_FOOD_LOG_PARAMS_JSON,
    UPDATE_FOOD_LOG_RESPONSE_JSON,
    REFRESH_ACCESS_TOKEN_RESPONSE,
)


FITBIT_HOST = "https://api.fitbit.com"


@pytest.fixture
def fitbit() -> Fitbit:
    return Fitbit("client_id", "access_token", "refresh_token")


@pytest.fixture
def mock_get() -> Generator[MagicMock]:
    with patch("src.fitbit.requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_post() -> Generator[MagicMock]:
    with patch("src.fitbit.requests.post") as mock_post:
        yield mock_post


@pytest.fixture
def mock_delete() -> Generator[MagicMock]:
    with patch("src.fitbit.requests.delete") as mock_delete:
        yield mock_delete


class TestFitbit:
    def test_fetch_food_log_success(self, fitbit: Fitbit, mock_get: MagicMock):
        date = "2024-06-01"

        mock_get.return_value.json.return_value = GET_FOOD_LOG_RESPONSE_JSON
        mock_get.return_value.raise_for_status.side_effect = None

        fitbit.fetch_food_log(date)
        mock_get.assert_called_once()

        requested_url = mock_get.call_args[0][0]
        assert (
            requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/date/{date}.json"
        ), "URL mismatch"

    def test_fetch_food_log_http_error(self, fitbit: Fitbit, mock_get: MagicMock):
        mock_get.return_value.raise_for_status.side_effect = HTTPError("HTTPError")
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.fetch_food_log("2024-06-01")

    def test_create_food_log_success(self, fitbit: Fitbit, mock_post: MagicMock):
        mock_json = CREATE_FOOD_LOG_RESPONSE_JSON
        params = CreateFoodLogParams(**CREATE_FOOD_LOG_PARAMS_JSON)

        mock_post.return_value.json.return_value = mock_json
        mock_post.return_value.raise_for_status.side_effect = None

        result = fitbit.create_food_log(params)
        assert result == mock_json

        requested_url = mock_post.call_args[0][0]
        assert requested_url == f"{FITBIT_HOST}/1/user/-/foods/log.json", "URL mismatch"

        mock_post.assert_called_once()

    def test_create_food_log_http_error(self, fitbit: Fitbit, mock_post: MagicMock):
        params = CreateFoodLogParams(**CREATE_FOOD_LOG_PARAMS_JSON)
        mock_post.return_value.raise_for_status.side_effect = HTTPError("HTTPError")
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.create_food_log(params)

    def test_update_food_log_success(self, fitbit: Fitbit, mock_post: MagicMock):
        food_log_id = 123
        params = UpdateFoodLogParams(**UPDATE_FOOD_LOG_PARAMS_JSON)
        with patch("src.fitbit.requests.post") as mock_post:
            mock_post.return_value.json.return_value = UPDATE_FOOD_LOG_RESPONSE_JSON
            mock_post.return_value.raise_for_status.side_effect = None

            result = fitbit.update_food_log(food_log_id, params)
            assert result == UPDATE_FOOD_LOG_RESPONSE_JSON

            requested_url = mock_post.call_args[0][0]
            assert (
                requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/{food_log_id}.json"
            )

            mock_post.assert_called_once()

    def test_update_food_log_http_error(self, fitbit: Fitbit, mock_post: MagicMock):
        food_log_id = 123
        params = UpdateFoodLogParams(**UPDATE_FOOD_LOG_PARAMS_JSON)
        mock_post.return_value.raise_for_status.side_effect = HTTPError("HTTPError")
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.update_food_log(food_log_id, params)

    def test_delete_food_log_success(self, fitbit: Fitbit, mock_delete: MagicMock):
        food_log_id = 123
        mock_response = MagicMock()

        mock_delete.return_value = mock_response
        mock_delete.return_value.raise_for_status = MagicMock()

        result = fitbit.delete_food_log(food_log_id)
        assert result == mock_response

        requested_url = mock_delete.call_args[0][0]
        assert (
            requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/{food_log_id}.json"
        ), "URL mismatch"

        mock_delete.assert_called_once()

    def test_delete_food_log_http_error(fsel, fitbit: Fitbit, mock_delete: MagicMock):
        mock_delete.return_value.raise_for_status.side_effect = HTTPError("HTTPError")
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.delete_food_log(1)

    def test_refresh_access_token_success(self, fitbit: Fitbit, mock_post: MagicMock):
        mock_post.return_value.json.return_value = REFRESH_ACCESS_TOKEN_RESPONSE
        mock_post.return_value.raise_for_status = MagicMock()

        result = fitbit.refresh_access_token()
        assert result == REFRESH_ACCESS_TOKEN_RESPONSE

        requested_url = mock_post.call_args[0][0]
        assert requested_url == f"{FITBIT_HOST}/oauth2/token", "URL mismatch"

        mock_post.assert_called_once()

    def test_refresh_access_token_http_error(
        self, fitbit: Fitbit, mock_post: MagicMock
    ):
        mock_post.return_value.raise_for_status.side_effect = HTTPError("HTTPError")
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.refresh_access_token()
