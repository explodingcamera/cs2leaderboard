# cs2leaderboard

Historical data for the CS2 leaderboard, updated daily.

# API

## `GET https://explodingcamera.github.io/cs2leaderboard/data/meta.json`

Returns metadata about the leaderboard data.

```json
{
  "regions": {
    "global": "Global",
    ...
  },
  "seasons": {
    "season1": {
      "name": "Season 1",
      "start": "2023-09-27T00:00:00Z"
    }
  }
}
```

## `GET https://explodingcamera.github.io/cs2leaderboard/data/latest/{region}.json`

Returns the latest leaderboard data for the given region.

```json
{
  "result": {
    "entries": [
      {
        "rank": 1,
        "score": 1000,
        "detailData": "...",
        "name": "Player"
      }
    ]
  }
}
```

## `GET https://explodingcamera.github.io/cs2leaderboard/data/historical/{region}/{date}.json`

Returns the leaderboard data for the given region on the given date.

## `GET https://explodingcamera.github.io/cs2leaderboard/data/timestamps.csv`

Returns a text file containing the timestamps of all the historical data files.
