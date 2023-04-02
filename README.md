## 環境構築

1. `docker build -t web-api .`を入力して Docker イメージを build する

2. `docker run -v <本ディレクトリへのパス>:/app -p 8000:8000 -it --rm web-api`にてアプリケーションを起動

## エンドポイント

以下のエンドポイントが存在している。

- /health: アプリケーション生存確認用エンドポイント

- /locations: 使用可能な都市名一覧取得用エンドポイント

- /columns: 使用可能なカラム一覧エンドポイント

- /location/{location}/column/{column}/date/{date}: 都市の指定日付のカラム値を返す

- /location/{location}/column/{column}/start/{start}/end/{end}: 都市の指定期間のカラム値を返す

- /location/{location}/column/{column}/start/{start}/end/{end}/agg/{agg}: 都市の指定期間のカラム値の集約値を返す

詳しくは、`localhost:8000/docs`にアクセスすると確認可能

## 各エンドポイントに対するアクセス

下記にエンドポイント, コマンド, 返り値を示す。なお、curl を用いずに「ブラウザに URL を打ち込む」, 「`localhost:8000/docs`の対話型 API ドキュメントを使用する」などでも動作確認は可能である。

- /health

  - コマンド: `curl http://localhost:8000/health`

  - 返り値: 下記

  ```json
  { "statis": "success" }
  ```

- /locations

  - コマンド: `curl http://localhost:8000/locations`

  - 返り値: 下記
    ```json
    { "available_locations": ["tokyo", "fukuoka", "osaka"] }
    ```

- /columns

  - コマンド: `curl http://localhost:8000/columns`

  - 返り値: 下記

  ```json
  {
    "available_columns": [
      "mean temperature",
      "maximum temperature",
      "minimum temperature",
      "rainfall",
      "daylight",
      "steam pressure",
      "cloudiness",
      "wind spped",
      "fallen snow"
    ]
  }
  ```

- /location/{location}/column/{column}/date/{date}

  - コマンド: `curl http://localhost:8000/location/tokyo/column/mean%20temperature/date/2022-01-01`

  - 返り値: 下記

  ```json
  {
    "location": "tokyo",
    "mean temperature": 3.4,
    "date": "2022-01-01T00:00:00"
  }
  ```

- /location/{location}/column/{column}/start/{start}/end/{end}

  - コマンド: `curl http://localhost:8000/location/tokyo/column/mean%20temperature/start/2022-01-01/end/2022-01-05`

  - 返り値: 下記

  ```json
  {
    "location": "tokyo",
    "mean temperature": {
      "2022-01-01T00:00:00": 3.4,
      "2022-01-02T00:00:00": 3.5,
      "2022-01-03T00:00:00": 5.5,
      "2022-01-04T00:00:00": 5.2,
      "2022-01-05T00:00:00": 4.1
    }
  }
  ```

- /location/{location}/column/{column}/start/{start}/end/{end}/agg/{agg}

  - コマンド: `curl http://localhost:8000/location/tokyo/column/daylight/start/2022-01-01/end/2022-01-31/agg/min`

  - 返り値: 下記

  ```json
  {
    "location": "tokyo",
    "daylight_min": 0
  }
  ```
