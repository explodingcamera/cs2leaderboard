from scoreboard_pb2 import ScoreLeaderboardData
import requests
from datetime import datetime
import json
import os

url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_"
current_season = "season1"

def fetch_all():
    regions = []
    for region in data["regions"].keys():
        regions.append(fetch_leaderboard(region))
    return regions

def fetch_global():
    return fetch_leaderboard('global')

def fetch_europe():
    return fetch_leaderboard('europe')

def fetch_africa():
    return fetch_leaderboard('africa')

def fetch_asia():
    return fetch_leaderboard('asia')

def fetch_australia():
    return fetch_leaderboard('australia')

def fetch_china():
    return fetch_leaderboard('china')

def fetch_northamerica():
    return fetch_leaderboard('northamerica')

def fetch_southamerica():
    return fetch_leaderboard('southamerica')

def fetch_leaderboard(region):
    response = requests.get(f"{url}{current_season}{'' if region == 'global' else '_' + region}")
    data = response.json()
    return data

def decode(data: bytes) -> ScoreLeaderboardData:
    message = ScoreLeaderboardData()
    message.ParseFromString(data)
    return message

maps = [
    "anubis",
    "inferno",
    "mirage",
    "vertigo",
    "overpass",
    "nuke",
    "ancient",
    None
]


def decode_data_details(data):
    data2 = data[2:].rstrip('00')
    uint8array = bytes.fromhex(data2)
    res = decode(uint8array)

    def get_tag(tag, fn=None):
        entry = next((entry for entry in res.matchentries if entry.tag == tag), None)
        val = entry.val if entry else None
        return fn(val) if fn and val else val

    return {
        'kills': get_tag(1),
        'assists': get_tag(2),
        'deaths': get_tag(3),
        'points': get_tag(4),
        'headshots': get_tag(5),
        'shots_fired': get_tag(6),
        'shots_on_target': get_tag(7),
        'damage_inflicted': get_tag(8),
        'damage_received': get_tag(9),
        'time_elapsed': get_tag(10),
        'time_remaining': get_tag(11),
        'rounds_played': get_tag(12),
        'bonus_pistol_only': get_tag(13),
        'bonus_hard_mode': get_tag(14),
        'bonus_challenge': get_tag(15),
        'matches_won': get_tag(16),
        'matches_tied': get_tag(17),
        'matches_lost': get_tag(18),
        'map_stats': get_tag(19, get_map_stats),
        'time_achieved': get_tag(20, lambda arg: datetime.fromtimestamp(arg).isoformat()),
        'region': get_tag(21, get_region)
    }

def get_region(region):
    region_map = {
        0: None,
        1: "northamerica",
        2: "southamerica",
        3: "europe",
        4: "asia",
        5: "australia",
        6: None,
        7: "africa",
        8: None,
        9: "china"
    }
    return region_map.get(region)


def get_map_stats(map_stats):
    result = [(map_stats >> i) & 0xf for i in range(0, 32, 4)]
    return dict(zip(maps, result))


if __name__ == "__main__":
    data = {
        "regions": {
            "global": "Global",
            "europe": "Europe",
            "africa": "Africa",
            "asia": "Asia",
            "australia": "Australia",
            "china": "China",
            "northamerica": "North America",
            "southamerica": "South America"
        },
        "seasons": {
            "season1": {
            "name": "Season 1",
            "start": "2023-09-27T00:00:00Z"
            }
        }
    }
    timestamp = datetime.now().isoformat().replace(':', '_').replace('.', '_')
    promises = [fetch_leaderboard(region) for region in data["regions"].keys()]

    for region, data in zip(data["regions"].keys(), promises):
        entries = data['result']['entries']
        res = [
            {
                'rank': entry['rank'],
                'rating': entry['score'] >> 15,
                'name': entry.get('name'),
                **decode_data_details(entry['detailData'])
            }
            for entry in entries
        ]

        filename = os.path.join('../data/historical', region, f"{timestamp}.json")
        filename_latest = os.path.join('../data/latest', f"{region}.json")
        directory = os.path.dirname(filename)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(filename, 'w') as f:
            json.dump(res, f)

        directory_latest = os.path.dirname(filename_latest)
        if not os.path.exists(directory_latest):
            os.makedirs(directory_latest)

        with open(filename_latest, 'w') as f:
            json.dump(res, f)