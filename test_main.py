from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from main import app


AVAILABLE_COLUMNS = [
    "mean temperature",
    "maximum temperature",
    "minimum temperature",
    "rainfall",
    "daylight",
    "steam pressure",
    "cloudiness",
    "wind spped",
    "fallen snow",
]


@pytest.fixture(scope="function", autouse=True)
def init_csv(tmpdir, mocker):
    dst_dir = Path(tmpdir / "csv_root")
    dst_dir.mkdir(parents=True, exist_ok=True)
    mocker.patch("main.CSV_ROOT", dst_dir)
    init_df = pd.DataFrame(
        data=[
            ["2022/01/01"] + [1.0] * len(AVAILABLE_COLUMNS),
            ["2022/01/02"] + [2.0] * len(AVAILABLE_COLUMNS),
            ["2022/01/03"] + [3.0] * len(AVAILABLE_COLUMNS),
        ],
        columns=["date"] + AVAILABLE_COLUMNS,
    )
    init_df.to_csv(dst_dir / "fukuoka.csv", index=False)
    init_df.to_csv(dst_dir / "tokyo.csv", index=False)
    init_df.to_csv(dst_dir / "osaka.csv", index=False)


client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "success"}


def test_locations():
    res = client.get("/locations")
    assert res.status_code == 200
    assert sorted(res.json()["available_locations"]) == ["fukuoka", "osaka", "tokyo"]


def test_columns():
    res = client.get("/columns")
    assert res.status_code == 200
    assert res.json()["available_columns"] == AVAILABLE_COLUMNS


def test_get_location_date_info():
    res = client.get("/location/tokyo/column/daylight/date/2022-01-01")
    assert res.status_code == 200
    assert res.json() == {
        "location": "tokyo",
        "date": "2022-01-01T00:00:00",
        "daylight": 1.0,
    }


def test_get_location_start2end_info():
    res = client.get("/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03")
    assert res.status_code == 200
    assert res.json() == {
        "location": "tokyo",
        "daylight": {
            "2022-01-01T00:00:00": 1.0,
            "2022-01-02T00:00:00": 2.0,
            "2022-01-03T00:00:00": 3.0,
        },
    }


class TestGetLocationStart2EndAggregationInfo:
    def test_max_info(self):
        res = client.get(
            "/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03/agg/max"
        )
        assert res.status_code == 200
        assert res.json() == {"location": "tokyo", "daylight_max": 3.0}

    def test_min_info(self):
        res = client.get(
            "/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03/agg/min"
        )
        assert res.status_code == 200
        assert res.json() == {"location": "tokyo", "daylight_min": 1.0}

    def test_median_info(self):
        res = client.get(
            "/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03/agg/median"
        )
        assert res.status_code == 200
        assert res.json() == {"location": "tokyo", "daylight_median": 2.0}

    def test_mean_info(self):
        res = client.get(
            "/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03/agg/mean"
        )
        assert res.status_code == 200
        assert res.json() == {"location": "tokyo", "daylight_mean": 2.0}

    def test_sum_info(self):
        res = client.get(
            "/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-03/agg/sum"
        )
        assert res.status_code == 200
        assert res.json() == {"location": "tokyo", "daylight_sum": 6.0}
