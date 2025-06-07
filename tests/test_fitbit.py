from unittest.mock import patch, MagicMock
from collections.abc import Generator

import pytest
from requests import HTTPError

from src.fitbit import Fitbit
from src.models.fitbit import (
    CreateFoodLogParams,
    UpdateFoodLogParams,
    GetFoodLogResponse,
)
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
    return Fitbit(
        "client_id",
        "access_token",
        "refresh_token",
        auto_token_refresh=True,
        callback_on_token_refreshed=MagicMock(return_value=lambda: ...),
    )


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
    # ===== Fetch Food Log =====
    def test_fetch_food_log_success(self, fitbit: Fitbit, mock_get: MagicMock):
        date = "2024-06-01"

        mock_get.return_value.json.side_effect = MagicMock(
            return_value=GET_FOOD_LOG_RESPONSE_JSON
        )
        mock_get.return_value.raise_for_status.side_effect = None

        response = fitbit.fetch_food_log(date)
        mock_get.assert_called_once()
        assert response == GetFoodLogResponse(**GET_FOOD_LOG_RESPONSE_JSON)

        requested_url = mock_get.call_args[0][0]
        assert (
            requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/date/{date}.json"
        ), "URL mismatch"

    def test_fetch_food_log_http_error(self, fitbit: Fitbit, mock_get: MagicMock):
        mock_get.return_value.raise_for_status.side_effect = HTTPError(
            "HTTPError", response=MagicMock(status_code=400)
        )
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.fetch_food_log("2024-06-01")

    @pytest.mark.parametrize("auto_token_refresh", [True, False])
    def test_fetch_food_log_auth_error(
        self,
        fitbit: Fitbit,
        mock_get: MagicMock,
        mock_post: MagicMock,
        auto_token_refresh: bool,
    ):
        date = "2024-06-01"
        fitbit._auto_token_refresh = auto_token_refresh

        # 初回実行時は認証エラー(401エラー)を起こし、2回目はトークンリフレッシュ後に実行される想定のため正常終了させる
        err_msg = "Auth Error"
        mock_get.return_value.raise_for_status.side_effect = [
            HTTPError(err_msg, response=MagicMock(status_code=401)),
            lambda: ...,
        ]
        mock_get.return_value.json.return_value = GET_FOOD_LOG_RESPONSE_JSON

        mock_post.return_value.json.return_value = REFRESH_ACCESS_TOKEN_RESPONSE
        mock_post.return_value.raise_for_status = MagicMock()

        if auto_token_refresh:
            # 自動トークンリフレッシュ有の場合
            response = fitbit.fetch_food_log(date)
            fitbit._callback_on_token_refreshed.assert_called_once_with(
                REFRESH_ACCESS_TOKEN_RESPONSE["access_token"],
                REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"],
            )
            assert response == GetFoodLogResponse(**GET_FOOD_LOG_RESPONSE_JSON)

            assert fitbit._access_token == REFRESH_ACCESS_TOKEN_RESPONSE["access_token"]
            assert (
                fitbit._refresh_token == REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"]
            )
        else:
            # 自動トークンリフレッシュ無の場合
            with pytest.raises(HTTPError, match=err_msg):
                response = fitbit.fetch_food_log(date)

            fitbit._callback_on_token_refreshed.assert_not_called()

    # ===== Create Food Log =====
    def test_create_food_log_success(self, fitbit: Fitbit, mock_post: MagicMock):
        mock_json = CREATE_FOOD_LOG_RESPONSE_JSON
        params = CreateFoodLogParams(**CREATE_FOOD_LOG_PARAMS_JSON)

        mock_post.return_value.json.side_effect = MagicMock(return_value=mock_json)
        mock_post.return_value.raise_for_status.side_effect = None

        response = fitbit.create_food_log(params)
        assert response == mock_json

        requested_url = mock_post.call_args[0][0]
        assert requested_url == f"{FITBIT_HOST}/1/user/-/foods/log.json", "URL mismatch"

        mock_post.assert_called_once()

    def test_create_food_log_http_error(self, fitbit: Fitbit, mock_post: MagicMock):
        params = CreateFoodLogParams(**CREATE_FOOD_LOG_PARAMS_JSON)
        mock_post.return_value.raise_for_status.side_effect = HTTPError(
            "HTTPError", response=MagicMock(status_code=400)
        )
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.create_food_log(params)

    @pytest.mark.parametrize("auto_token_refresh", [True, False])
    def test_create_food_log_auth_error(
        self, fitbit: Fitbit, mock_post: MagicMock, auto_token_refresh: bool
    ):
        params = CreateFoodLogParams(**CREATE_FOOD_LOG_PARAMS_JSON)
        mock_json = CREATE_FOOD_LOG_RESPONSE_JSON
        fitbit._auto_token_refresh = auto_token_refresh

        # 初回実行時は認証エラー(401エラー)を起こし、2回目はトークンリフレッシュ後に実行される想定のため正常終了させる
        err_msg = "Auth Error"
        mock_post.return_value.raise_for_status.side_effect = [
            HTTPError(err_msg, response=MagicMock(status_code=401)),
            lambda: ...,
            lambda: ...,
        ]
        mock_post.return_value.json.side_effect = [
            REFRESH_ACCESS_TOKEN_RESPONSE,
            mock_json,
        ]

        if auto_token_refresh:
            # 自動トークンリフレッシュ有の場合
            response = fitbit.create_food_log(params)
            fitbit._callback_on_token_refreshed.assert_called_once_with(
                REFRESH_ACCESS_TOKEN_RESPONSE["access_token"],
                REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"],
            )
            assert response == mock_json

            assert fitbit._access_token == REFRESH_ACCESS_TOKEN_RESPONSE["access_token"]
            assert (
                fitbit._refresh_token == REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"]
            )
        else:
            # 自動トークンリフレッシュ無の場合
            with pytest.raises(HTTPError, match=err_msg):
                response = fitbit.create_food_log(params)

            fitbit._callback_on_token_refreshed.assert_not_called()

    # ===== Update Food Log =====
    def test_update_food_log_success(self, fitbit: Fitbit, mock_post: MagicMock):
        food_log_id = 123
        params = UpdateFoodLogParams(**UPDATE_FOOD_LOG_PARAMS_JSON)

        mock_post.return_value.json.return_value = UPDATE_FOOD_LOG_RESPONSE_JSON
        mock_post.return_value.raise_for_status.side_effect = None

        result = fitbit.update_food_log(food_log_id, params)
        assert result == UPDATE_FOOD_LOG_RESPONSE_JSON

        requested_url = mock_post.call_args[0][0]
        assert requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/{food_log_id}.json"

        mock_post.assert_called_once()

    def test_update_food_log_http_error(self, fitbit: Fitbit, mock_post: MagicMock):
        food_log_id = 123
        params = UpdateFoodLogParams(**UPDATE_FOOD_LOG_PARAMS_JSON)
        mock_post.return_value.raise_for_status.side_effect = HTTPError(
            "HTTPError", response=MagicMock(status_code=400)
        )
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.update_food_log(food_log_id, params)

    @pytest.mark.parametrize("auto_token_refresh", [True, False])
    def test_update_food_log_auth_error(
        self, fitbit: Fitbit, mock_post: MagicMock, auto_token_refresh: bool
    ):
        food_log_id = 123
        params = UpdateFoodLogParams(**UPDATE_FOOD_LOG_PARAMS_JSON)
        mock_json = UPDATE_FOOD_LOG_RESPONSE_JSON
        fitbit._auto_token_refresh = auto_token_refresh

        # 初回実行時は認証エラー(401エラー)を起こし、2回目はトークンリフレッシュ後に実行される想定のため正常終了させる
        err_msg = "Auth Error"
        mock_post.return_value.raise_for_status.side_effect = [
            HTTPError(err_msg, response=MagicMock(status_code=401)),
            lambda: ...,
            lambda: ...,
        ]
        mock_post.return_value.json.side_effect = [
            REFRESH_ACCESS_TOKEN_RESPONSE,
            mock_json,
        ]

        if auto_token_refresh:
            # 自動トークンリフレッシュ有の場合
            response = fitbit.update_food_log(food_log_id, params)
            fitbit._callback_on_token_refreshed.assert_called_once_with(
                REFRESH_ACCESS_TOKEN_RESPONSE["access_token"],
                REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"],
            )
            assert response == mock_json

            assert fitbit._access_token == REFRESH_ACCESS_TOKEN_RESPONSE["access_token"]
            assert (
                fitbit._refresh_token == REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"]
            )
        else:
            # 自動トークンリフレッシュ無の場合
            with pytest.raises(HTTPError, match=err_msg):
                response = fitbit.update_food_log(food_log_id, params)

            fitbit._callback_on_token_refreshed.assert_not_called()

    # ===== Delete Food Log =====
    def test_delete_food_log_success(self, fitbit: Fitbit, mock_delete: MagicMock):
        food_log_id = 123
        mock_json = {}

        mock_delete.return_value.json.return_value = mock_json
        mock_delete.return_value.raise_for_status = MagicMock()

        result = fitbit.delete_food_log(food_log_id)
        assert result == mock_json

        requested_url = mock_delete.call_args[0][0]
        assert (
            requested_url == f"{FITBIT_HOST}/1/user/-/foods/log/{food_log_id}.json"
        ), "URL mismatch"

        mock_delete.assert_called_once()

    def test_delete_food_log_http_error(fsel, fitbit: Fitbit, mock_delete: MagicMock):
        mock_delete.return_value.raise_for_status.side_effect = HTTPError(
            "HTTPError", response=MagicMock(status_code=400)
        )
        with pytest.raises(HTTPError, match="HTTPError"):
            fitbit.delete_food_log(1)

    @pytest.mark.parametrize("auto_token_refresh", [True, False])
    def test_delete_food_log_auth_error(
        self,
        fitbit: Fitbit,
        mock_post: MagicMock,
        mock_delete: MagicMock,
        auto_token_refresh: bool,
    ):
        food_log_id = 123
        mock_response = MagicMock()
        fitbit._auto_token_refresh = auto_token_refresh

        # 初回実行時は認証エラー(401エラー)を起こし、2回目はトークンリフレッシュ後に実行される想定のため正常終了させる
        err_msg = "Auth Error"
        mock_delete.return_value.raise_for_status.side_effect = [
            HTTPError(err_msg, response=MagicMock(status_code=401)),
            lambda: ...,
            lambda: ...,
        ]
        mock_post.return_value.json.return_value = REFRESH_ACCESS_TOKEN_RESPONSE
        mock_delete.return_value.json.return_value = mock_response

        if auto_token_refresh:
            # 自動トークンリフレッシュ有の場合
            response = fitbit.delete_food_log(food_log_id)
            fitbit._callback_on_token_refreshed.assert_called_once_with(
                REFRESH_ACCESS_TOKEN_RESPONSE["access_token"],
                REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"],
            )
            assert response == mock_response

            assert fitbit._access_token == REFRESH_ACCESS_TOKEN_RESPONSE["access_token"]
            assert (
                fitbit._refresh_token == REFRESH_ACCESS_TOKEN_RESPONSE["refresh_token"]
            )
        else:
            # 自動トークンリフレッシュ無の場合
            with pytest.raises(HTTPError, match=err_msg):
                response = fitbit.delete_food_log(food_log_id)

            fitbit._callback_on_token_refreshed.assert_not_called()

    # ===== Refresh Access Token =====
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
