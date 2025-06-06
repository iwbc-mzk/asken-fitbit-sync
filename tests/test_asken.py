import pytest
from unittest.mock import patch, MagicMock

from src.asken import Asken

ONE_MEAL_LOG_MOCK = MagicMock(
    model_dump=MagicMock(
        return_value={
            "calories": 100,
            "protein": 9,
            "fat": 2,
            "carbs": 20,
            "calcium": 1,
            "magnesium": 2,
            "iron": 3,
            "zinc": 4,
            "vitamin_a": 5,
            "vitamin_d": 6,
            "vitamin_b1": 3,
            "vitamin_b2": 10,
            "vitamin_b6": 2,
            "vitamin_c": 4,
            "fiber": 6,
            "saturatedFat": 7,
            "solt": 10,
            "meal_type_id": 1,
            "date": "2024-01-01",
        },
    )
)

DAILY_MEAL_LOG_MOCK = MagicMock(
    model_dump=MagicMock(
        return_value={
            "calories": 300,
            "protein": 27,
            "fat": 6,
            "carbs": 60,
            "calcium": 3,
            "magnesium": 6,
            "iron": 9,
            "zinc": 12,
            "vitamin_a": 15,
            "vitamin_d": 18,
            "vitamin_b1": 9,
            "vitamin_b2": 30,
            "vitamin_b6": 6,
            "vitamin_c": 12,
            "fiber": 18,
            "saturatedFat": 21,
            "solt": 30,
            "meal_type_id": 3,
            "date": "2024-01-01",
        },
    )
)


@pytest.fixture
def mock_logger():
    with patch("src.asken.get_logger") as logger:
        yield logger


@pytest.fixture
def mock_foodlog():
    with patch("src.asken.FoodLog") as fl:
        fl.return_value = MagicMock(spec=["logged", "model_dump"])
        fl.return_value.model_dump.return_value = {
            "calories": 100,
            "protein": 10,
            "fat": 5,
            "carbs": 20,
            "calcium": 1,
            "magnesium": 2,
            "iron": 3,
            "zinc": 4,
            "vitamin_a": 5,
            "vitamin_d": 6,
            "vitamin_b1": 7,
            "vitamin_b2": 8,
            "vitamin_b6": 9,
            "vitamin_c": 10,
            "fiber": 11,
            "saturatedFat": 12,
            "solt": 13,
            "meal_type_id": 5,
            "date": "2024-01-01",
        }
        yield fl


@pytest.fixture
def mock_session():
    with patch("requests.Session") as sess, open(
        "tests/data/html/asken_food_log.html", "r", encoding="utf-8"
    ) as f:
        html = f.read()
        sess_inst = sess.return_value
        sess_inst.post.return_value = MagicMock(
            status_code=200, text="ok", raise_for_status=MagicMock()
        )
        sess_inst.get.return_value = MagicMock(
            status_code=200,
            text=html,
            raise_for_status=MagicMock(),
        )
        yield sess


class TestAsken:
    def test_headers(self):
        assert "User-Agent" in Asken._headers()

    def test_init_success(self, mock_session):
        a = Asken("a@b.com", "pw")
        assert hasattr(a, "_session")

    def test_init_login_fail(self, mock_session):
        mock_session.return_value.post.side_effect = Exception("fail")
        with pytest.raises(Exception):
            Asken("a@b.com", "pw")

    def test_login_success(self):
        a = Asken("a@b.com", "pw")
        sess = a.login("a@b.com", "pw")
        assert sess is not None

    def test_login_http_error(self, mock_session):
        mock_session.return_value.post.return_value.raise_for_status.side_effect = (
            Exception("http error")
        )
        with pytest.raises(Exception):
            Asken("a@b.com", "pw")

    @patch.object(Asken, "fetch_one_meal_log")
    @patch.object(Asken, "fetch_snack_log")
    @patch.object(Asken, "fetch_daily_food_log")
    def test_fetch_food_log_calls_correct_method(
        self, mock_daily, mock_snack, mock_one
    ):
        a = Asken("a@b.com", "pw")

        a.fetch_food_log("2024-01-01", 1)
        mock_one.assert_called_with("2024-01-01", 1)

        a.fetch_food_log("2024-01-01", 2)
        mock_one.assert_called_with("2024-01-01", 2)

        a.fetch_food_log("2024-01-01", 3)
        mock_one.assert_called_with("2024-01-01", 3)

        a.fetch_food_log("2024-01-01", 4)
        mock_snack.assert_called_with("2024-01-01")

        a.fetch_food_log("2024-01-01", 5)
        mock_daily.assert_called_with("2024-01-01")

        a.fetch_food_log("2024-01-01", 5)
        mock_one.assert_called_with("2024-01-01", 3)
        mock_snack.assert_called_with("2024-01-01")
        mock_daily.assert_called_with("2024-01-01")

    @patch.object(Asken, "_scrape_food_log")
    def test_fetch_one_meal_log_success(self, mock_scrape):
        mock_scrape.return_value = {"calories": 100}
        a = Asken("a@b.com", "pw")
        result = a.fetch_one_meal_log("2024-01-01", 1)
        assert result is not None
        assert result.calories == 100
        assert result.logged

    def test_fetch_one_meal_log_no_record(self, mock_session):
        mock_session.return_value.get.return_value.text = (
            "食事記録が無いためアドバイスが計算できません"
        )
        a = Asken("a@b.com", "pw")
        result = a.fetch_one_meal_log("2024-01-01", 1)
        assert result is None

    def test_fetch_one_meal_log_http_error(self, mock_session):
        mock_session.return_value.get.return_value.raise_for_status.side_effect = (
            Exception("http error")
        )
        a = Asken("a@b.com", "pw")
        with pytest.raises(Exception):
            a.fetch_one_meal_log("2024-01-01", 1)

    @patch.object(Asken, "_scrape_food_log")
    def test_fetch_daily_food_log_success(self, mock_scrape, mock_session):
        mock_scrape.return_value = {"calories": 100}
        a = Asken("a@b.com", "pw")
        result = a.fetch_daily_food_log("2024-01-01")
        assert result is not None
        assert result.calories == 100
        assert result.logged

    def test_fetch_daily_food_log_no_record(self, mock_session):
        mock_session.return_value.get.return_value.text = (
            "食事記録が無いためアドバイスが計算できません"
        )
        a = Asken("a@b.com", "pw")
        result = a.fetch_daily_food_log("2024-01-01")
        assert result is None

    def test_fetch_daily_food_log_http_error(self, mock_session):
        mock_session.return_value.get.return_value.raise_for_status.side_effect = (
            Exception("http error")
        )
        a = Asken("a@b.com", "pw")
        with pytest.raises(Exception):
            a.fetch_daily_food_log("2024-01-01")

    @patch.object(Asken, "fetch_daily_food_log")
    @patch.object(Asken, "fetch_one_meal_log")
    @pytest.mark.parametrize(
        "calories, protein, fat, carbs",
        [
            (90, 10, 10, 10),
            (100, 9, 10, 10),
            (100, 10, 9, 10),
            (100, 10, 10, 9),
        ],
    )
    def test_fetch_snack_log_all_meals(
        self, mock_one, mock_daily, calories, protein, fat, carbs
    ):
        mock_daily.return_value.model_dump.return_value = {
            "calories": 300,
            "protein": 30,
            "fat": 30,
            "carbs": 30,
            "calcium": 3,
            "magnesium": 6,
            "iron": 9,
            "zinc": 12,
            "vitamin_a": 15,
            "vitamin_d": 18,
            "vitamin_b1": 21,
            "vitamin_b2": 24,
            "vitamin_b6": 27,
            "vitamin_c": 30,
            "fiber": 33,
            "saturatedFat": 36,
            "solt": 39,
            "meal_type_id": 5,
            "date": "2024-01-01",
        }
        mock_one.side_effect = [
            MagicMock(
                model_dump=MagicMock(
                    return_value={
                        "calories": calories,
                        "protein": protein,
                        "fat": fat,
                        "carbs": carbs,
                        "calcium": 1,
                        "magnesium": 2,
                        "iron": 3,
                        "zinc": 4,
                        "vitamin_a": 5,
                        "vitamin_d": 6,
                        "vitamin_b1": 7,
                        "vitamin_b2": 8,
                        "vitamin_b6": 9,
                        "vitamin_c": 10,
                        "fiber": 11,
                        "saturatedFat": 12,
                        "solt": 13,
                    }
                )
            ),
            MagicMock(
                model_dump=MagicMock(
                    return_value={
                        "calories": calories,
                        "protein": protein,
                        "fat": fat,
                        "carbs": carbs,
                        "calcium": 1,
                        "magnesium": 2,
                        "iron": 3,
                        "zinc": 4,
                        "vitamin_a": 5,
                        "vitamin_d": 6,
                        "vitamin_b1": 7,
                        "vitamin_b2": 8,
                        "vitamin_b6": 9,
                        "vitamin_c": 10,
                        "fiber": 11,
                        "saturatedFat": 12,
                        "solt": 13,
                    }
                )
            ),
            MagicMock(
                model_dump=MagicMock(
                    return_value={
                        "calories": calories,
                        "protein": protein,
                        "fat": fat,
                        "carbs": carbs,
                        "calcium": 1,
                        "magnesium": 2,
                        "iron": 3,
                        "zinc": 4,
                        "vitamin_a": 5,
                        "vitamin_d": 6,
                        "vitamin_b1": 7,
                        "vitamin_b2": 8,
                        "vitamin_b6": 9,
                        "vitamin_c": 10,
                        "fiber": 11,
                        "saturatedFat": 12,
                        "solt": 13,
                    }
                )
            ),
        ]
        a = Asken("a@b.com", "pw")
        result = a.fetch_snack_log("2024-01-01")
        assert result is not None

    @patch.object(Asken, "fetch_daily_food_log")
    @patch.object(Asken, "fetch_one_meal_log")
    @pytest.mark.parametrize("daily", [None, DAILY_MEAL_LOG_MOCK])
    @pytest.mark.parametrize(
        "breakfast",
        [None, ONE_MEAL_LOG_MOCK],
    )
    @pytest.mark.parametrize(
        "lunch",
        [None, ONE_MEAL_LOG_MOCK],
    )
    @pytest.mark.parametrize(
        "dinner",
        [None, ONE_MEAL_LOG_MOCK],
    )
    def test_fetch_snack_log_some_meals_none(
        self, mock_one, mock_daily, daily, breakfast, lunch, dinner
    ):
        mock_daily.return_value = daily
        mock_one.side_effect = [breakfast, lunch, dinner]
        asken = Asken("a@b.com", "pw")
        result = asken.fetch_snack_log("2024-01-01")

        if not daily:
            # 一日分の食事記録なし
            assert result is None
            mock_daily.assert_called_once_with("2024-01-01")
            mock_one.assert_not_called()
        else:
            nutritions = daily.model_dump()
            for log in [breakfast, lunch, dinner]:
                if not log:
                    continue

                log_nut = log.model_dump()
                for key in ["calories", "protein", "fat", "carbs"]:
                    nutritions[key] -= log_nut[key]

            if (
                nutritions["calories"]
                or nutritions["protein"]
                or nutritions["fat"]
                or nutritions["carbs"]
            ):
                # カロリー、PFCともに0の時
                assert result is not None
            else:
                assert result is None
                mock_daily.assert_called_once_with("2024-01-01")
                assert mock_one.call_count == 3

    @patch.object(Asken, "fetch_daily_food_log")
    @patch.object(Asken, "fetch_one_meal_log")
    def test_fetch_snack_log_no_snack(self, mock_one, mock_daily, mock_foodlog):
        """カロリーとPFCが0の時、間食ログがないことを確認"""
        mock_daily.return_value.model_dump.return_value = {
            "calories": 300,
            "protein": 30,
            "fat": 30,
            "carbs": 30,
            "calcium": 3,
            "magnesium": 6,
            "iron": 9,
            "zinc": 12,
            "vitamin_a": 15,
            "vitamin_d": 18,
            "vitamin_b1": 21,
            "vitamin_b2": 24,
            "vitamin_b6": 27,
            "vitamin_c": 30,
            "fiber": 33,
            "saturatedFat": 36,
            "solt": 39,
            "meal_type_id": 5,
            "date": "2024-01-01",
        }

        one_meal_mock = MagicMock(
            model_dump=MagicMock(
                return_value={
                    "calories": 100,
                    "protein": 10,
                    "fat": 10,
                    "carbs": 10,
                    "calcium": 1,
                    "magnesium": 2,
                    "iron": 3,
                    "zinc": 4,
                    "vitamin_a": 5,
                    "vitamin_d": 6,
                    "vitamin_b1": 7,
                    "vitamin_b2": 8,
                    "vitamin_b6": 9,
                    "vitamin_c": 10,
                    "fiber": 11,
                    "saturatedFat": 12,
                    "solt": 13,
                }
            )
        )
        mock_one.side_effect = [one_meal_mock, one_meal_mock, one_meal_mock]
        a = Asken("a@b.com", "pw")
        result = a.fetch_snack_log("2024-01-01")
        assert result is None and not mock_foodlog.called

    def test_scrape_food_log_parses_html(self):
        with open("tests/data/html/asken_food_log.html", "r", encoding="utf-8") as f:
            html = f.read()
            a = Asken("a@b.com", "pw")
            result = a._scrape_food_log(html)
            food_log = {
                "date": "",
                "calories": 942,
                "protein": 32.6,
                "fat": 33.1,
                "carbs": 135.2,
                "calcium": 271,
                "magnesium": 123,
                "iron": 6.9,
                "zinc": 3.2,
                "vitamin_a": 537,
                "vitamin_d": 1.9,
                "vitamin_b1": 0.7,
                "vitamin_b2": 0.55,
                "vitamin_b6": 1.16,
                "vitamin_c": 61,
                "fiber": 11.7,
                "saturatedFat": 10.94,
                "solt": 3.3,
            }
            assert result == food_log
