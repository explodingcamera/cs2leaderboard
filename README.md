# cs2leaderboard

A free-to-use API for the CS2 leaderboard data. Includes daily snapshots of the leaderboard and useful metadata, such as game stats and ratings. Feel free to use this data for your own projects, but please link back to this repository if you do.

# API Endpoints

> **Data for a specific region or 'global'**\
> [https://explodingcamera.github.io/cs2leaderboard/data/latest/{region}.json](https://explodingcamera.github.io/cs2leaderboard/data/latest/{region}.json)

> **Historical data for a specific region or 'global'**\
> [https://explodingcamera.github.io/cs2leaderboard/data/historical/{region}/{date}.json](https://explodingcamera.github.io/cs2leaderboard/data/historical/{region}/{date}.json)

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `region` | `string` | A list of all regions can be found [here](https://explodingcamera.github.io/cs2leaderboard/data/meta.json) |
| `date` | `string` | A list of all captured dates can be found [here](https://explodingcamera.github.io/cs2leaderboard/data/timestamps.csv) |

Returns the leaderboard data for the given region on the given date.
Returns the latest leaderboard data for the given region.

## Example Response
```json
[
  {
    "rank": 1,
    "rating": 18302,
    "name": "uDEADSHOT",
    "matches_won": 45,
    "matches_lost": 4,
    "map_stats": {
      "anubis": 1,
      "inferno": 0,
      "mirage": 3,
      "vertigo": 3,
      "overpass": 0,
      "nuke": 0,
      "ancient": 3,
      "undefined": 0
    },
    "time_achieved": "2023-10-02T17:38:41.000Z",
    "region": "africa"
  },
  [...]
]
```
