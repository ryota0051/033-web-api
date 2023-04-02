from pathlib import Path

import pandas as pd
from fastapi import FastAPI

from util.handle_csv import get_aggrigation_func, read_csv
from util.handle_date import (check_date_range, check_end_greater_than_start,
                              get_datetime_from_str)

CSV_ROOT = Path("./data")

app = FastAPI()


@app.get("/health")
def health_check():
    """ヘルスチェック用のエンドポイント"""
    return {"status": "success"}


@app.get("/locations")
def get_available_location_list():
    """利用可能な位置情報リストを返す"""
    location_list = [Path(csv_path).stem for csv_path in CSV_ROOT.iterdir()]
    return {"available_locations": location_list}


@app.get("/columns")
def get_available_column_list():
    """利用可能なカラム一覧を返す"""
    tmp_df = pd.read_csv(CSV_ROOT / "osaka.csv")
    columns = tmp_df.columns[tmp_df.columns != "date"].to_list()
    return {"available_columns": columns}


@app.get("/location/{location}/column/{column}/date/{date}")
def get_location_date_info(location: str, column: str, date: str):
    """指定されたlocationの日付がdateであるときのカラム情報を返す
    ex.
        - location: tokyo
        - columns: mean temperature
        - date: 2022-01-01
        => 東京の2022-01-01における平均気温を返す
    Args:
        location: 対象都市
        column: 取得したいカラム
        date: 取得対象日付
    Returns:
        {
            "location": 都市名,
            column(パラメータで与えたカラム名): 対応する値,
            "date": 日付
        }
    """
    target_path = CSV_ROOT / f"{location}.csv"
    date = get_datetime_from_str(date)
    df = read_csv(target_path)
    check_date_range(date, df["date"].min(), df["date"].max(), date_name="date")
    return_value = df[df["date"] == date].iloc[0][column]
    return {"location": location, column: return_value, "date": date}


@app.get("/location/{location}/column/{column}/start/{start}/end/{end}")
def get_location_start2end_info(
    location: str,
    column: str,
    start: str,
    end: str,
):
    """指定されたlocationの指定期間におけるカラム情報を返す
    ex.
        - location: tokyo
        - columns: mean temperature
        - start: 2022-01-01
        - end: 2022-01-05
        => 東京の2022-01-01~2022-01-05の気温を気温を返す
    Args:
        location: 対象都市
        column: 取得したいカラム
        start: 開始日付
        end: 終了日付
    Returns:
        {
            "location": 都市名,
            column(パラメータで与えたカラム名): {
                日付1: 対応値1,
                日付2: 対応値2,
                ...
            },
        }
    """
    df = read_csv(CSV_ROOT / f"{location}.csv")
    start, end = get_datetime_from_str(start), get_datetime_from_str(end)
    check_date_range(start, df["date"].min(), df["date"].max(), date_name="start")
    check_date_range(end, df["date"].min(), df["date"].max(), date_name="end")
    check_end_greater_than_start(start, end)
    df.set_index("date", inplace=True)
    target_series = df[column][start:end]
    return {"location": location, column: target_series.to_dict()}


@app.get("/location/{location}/column/{column}/start/{start}/end/{end}/agg/{agg}")
def get_location_start2end_aggregation_info(
    location: str,
    column: str,
    start: str,
    end: str,
    agg: str,
):
    """locationにおける指定期間のカラムの値を集約するAPI
    ex.
        - location: tokyo
        - column: mean temperature
        - start: 2022-01-01
        - end: 2022-01-31
        - agg: max
        => 東京の2022年1月1日~2022年1月31日の平均気温の最大値を返す
    Args:
        location: 対象都市
        column: 取得したいカラム
        start: 開始日付
        end: 終了日付
        agg: 集約関数名
    Returns:
        {
            "location": 都市名,
            {column}(パラメータで与えたカラム名)_{agg}: 集約値
        }
    """
    df = read_csv(CSV_ROOT / f"{location}.csv")
    start, end = get_datetime_from_str(start), get_datetime_from_str(end)
    check_date_range(start, df["date"].min(), df["date"].max(), date_name="start")
    check_date_range(end, df["date"].min(), df["date"].max(), date_name="end")
    check_end_greater_than_start(start, end)
    df.set_index("date", inplace=True)
    target_series = df[column][start:end]
    aggregation_val = get_aggrigation_func(agg)(target_series)
    return {"location": location, f"{column}_{agg}": aggregation_val}
