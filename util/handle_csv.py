from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import HTTPException


def read_csv(path: Path):
    if not path.exists():
        raise HTTPException(status_code=404, detail="location not found")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_aggrigation_func(agg: str):
    func_candidate = {
        "sum": np.sum,
        "min": np.min,
        "max": np.max,
        "mean": np.mean,
        "median": np.median
    }
    if agg not in func_candidate:
        candidate_str = ", ".join(func_candidate.keys())
        raise HTTPException(status_code=404, detail=f"aggregation func must be chosen from {candidate_str}")
    return func_candidate[agg]
