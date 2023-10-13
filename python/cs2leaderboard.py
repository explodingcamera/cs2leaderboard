from scoreboard_pb2 import ScoreLeaderboardData
import requests
from datetime import datetime

class cs2leaderboard:
    def __init__(self):
        self.url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_"
        self.current_season = "season1"
        self.maps = [
            "anubis",
            "inferno",
            "mirage",
            "vertigo",
            "overpass",
            "nuke",
            "ancient",
            None
        ]

    def fetch_all(self):
        regions = [
            "global",
            "europe",
            "africa",
            "asia",
            "australia",
            "china",
            "northamerica",
            "southamerica"
        ]
        return {region: self.fetch_leaderboard(region) for region in regions}

    def fetch_global(self):
        return self.fetch_leaderboard('global')

    def fetch_europe(self):
        return self.fetch_leaderboard('europe')

    def fetch_africa(self):
        return self.fetch_leaderboard('africa')

    def fetch_asia(self):
        return self.fetch_leaderboard('asia')

    def fetch_australia(self):
        return self.fetch_leaderboard('australia')

    def fetch_china(self):
        return self.fetch_leaderboard('china')

    def fetch_northamerica(self):
        return self.fetch_leaderboard('northamerica')

    def fetch_southamerica(self):
        return self.fetch_leaderboard('southamerica')

    def fetch_leaderboard(self, region):
        response = requests.get(f"{self.url}{self.current_season}{'' if region == 'global' else '_' + region}")
        data = response.json()
        entries = data['result']['entries']
        return [
            {
                'rank': entry['rank'],
                'rating': entry['score'] >> 15,
                'name': entry.get('name'),
                **self.decode_data_details(entry['detailData'])
            }
            for entry in entries
        ]

    def decode(self, data: bytes) -> ScoreLeaderboardData:
        message = ScoreLeaderboardData()
        message.ParseFromString(data)
        return message

    def decode_data_details(self, data):
        data2 = data[2:].rstrip('00')
        uint8array = bytes.fromhex(data2)
        res = self.decode(uint8array)

        def get_tag(tag, fn=None):
            entry = next((entry for entry in res.matchentries if entry.tag == tag), None)
            val = entry.val if entry else None
            return fn(val) if fn and val else val

        return {
            'matches_won': get_tag(16),
            'matches_tied': get_tag(17),
            'matches_lost': get_tag(18),
            'map_stats': get_tag(19, self.get_map_stats),
            'time_achieved': get_tag(20, lambda arg: datetime.fromtimestamp(arg).isoformat()),
            'region': get_tag(21, self.get_region)
        }

    def get_region(self, region):
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

    def get_map_stats(self, map_stats):
        result = [(map_stats >> i) & 0xf for i in range(0, 32, 4)]
        return dict(zip(self.maps, result))

# external methods for pure use
_instance = cs2leaderboard()

def fetch_all():
    return _instance.fetch_all()

def fetch_global():
    return _instance.fetch_global()

def fetch_europe():
    return _instance.fetch_europe()

def fetch_africa():
    return _instance.fetch_africa()

def fetch_asia():
    return _instance.fetch_asia()

def fetch_australia():
    return _instance.fetch_australia()

def fetch_china():
    return _instance.fetch_china()

def fetch_northamerica():
    return _instance.fetch_northamerica()

def fetch_southamerica():
    return _instance.fetch_southamerica()

if __name__ == "__main__":
    leaderboard = cs2leaderboard()
    data = leaderboard.fetch_all()
    print(data)