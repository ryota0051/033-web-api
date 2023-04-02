from datetime import datetime

from fastapi import HTTPException


def get_datetime_from_str(str_date: str):
    try:
        date = datetime.strptime(str_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="date must be %Y-%m-%d")
    return date


def check_end_greater_than_start(start: datetime, end: datetime):
    if end <= start:
        raise HTTPException(400, detail="end must be greater than end")


def check_date_range(
    date: datetime,
    min_date: datetime,
    max_date: datetime,
    date_name: str,
):
    if not (min_date <= date <= max_date):
        raise HTTPException(
            400, detail=f"{date_name} must be between {min_date} and {max_date}"
        )
