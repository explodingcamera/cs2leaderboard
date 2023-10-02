import fs from "node:fs/promises";
import { regions } from "./data/meta.json" assert { type: "json" };

import { ScoreLeaderboardData } from "./proto/scoreboard";

const timestamp = new Date().toISOString().replace(/[:.-]/g, "_");
const url =
  "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_";
const currentSeason = "season1";

const fetchLeaderboard = async (region: string): Promise<{
  result: {
    entries: {
      rank: number;
      score: number;
      name?: string;
      detailData: string;
    }[]
  }
}> => {
  const response = await fetch(
    `${url}${currentSeason}${region === "global" ? "" : "_" + region}`
  );
  const data = await response.json();
  return data;
};

const promises = Object.keys(regions).map(async (region) => {
  console.log(`Fetching ${region}...`);

  const data = await fetchLeaderboard(region);
  const res = data.result.entries.map((entry) => ({
    rank: entry.rank,
    rating: entry.score >> 15,
    name: entry.name,
    ...decodeDataDetails(entry.detailData),
  }));

  const filename = `./data/historical/${region}/${timestamp}.json`;
  const filenameLatest = `./data/latest/${region}.json`;
  await Promise.all([
    Bun.write(filename, JSON.stringify(res)),
    Bun.write(filenameLatest, JSON.stringify(res)),
  ]);
});

await fs.appendFile("./data/timestamps.csv", `${timestamp}\n`);

const maps = [
  "anubis",
  "inferno",
  "mirage",
  "vertigo",
  "overpass",
  "nuke",
  "ancient",
  undefined,
]

const decodeDataDetails = (data: string) => {
  const data2 = data.slice(2).replace(/(00)+$/, "");
  const uint8array = new Uint8Array(
    data2.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16))
  );
  const res = ScoreLeaderboardData.decode(uint8array);

  const getTag = <T>(tag: number, fn?: (arg: number) => T) => {
    let val = res.matchentries.find((entry) => entry.tag === tag)?.val;
    if (fn && val) return fn(val);
    return val;
  };

  return {
    kills: getTag(1),
    assists: getTag(2),
    deaths: getTag(3),
    points: getTag(4),
    headshots: getTag(5),
    shots_fired: getTag(6),
    shots_on_target: getTag(7),
    damage_inflicted: getTag(8),
    damage_received: getTag(9),
    time_elapsed: getTag(10),
    time_remaining: getTag(11),
    rounds_played: getTag(12),
    bonus_pistol_only: getTag(13),
    bonus_hard_mode: getTag(14),
    bonus_challenge: getTag(15),
    matches_won: getTag(16),
    matches_tied: getTag(17),
    matches_lost: getTag(18),
    map_stats: getTag(19, getMapStats),
    time_achieved: getTag(20, (arg) => new Date(arg * 1000)),
    region: getTag(21, getRegion),
  };
};

const getRegion = (region: number): keyof typeof regions | undefined => {
  switch (region) {
    case 0:
      return undefined;
    case 1:
      return "northamerica";
    case 2:
      return "southamerica";
    case 3:
      return "europe";
    case 4:
      return "asia";
    case 5:
      return "australia";
    case 6:
      return undefined;
    case 7:
      return "africa";
    case 8:
      return undefined;
    case 9:
      return "china";
    default:
      throw new Error(`Unknown region: ${region}`);
  }
};

const getMapStats = (mapStats: number) => {
  const result = [];

  for (let i = 0; i < 32; i += 4) {
    result.push((mapStats >> i) & 0xf);
  }

  return Object.fromEntries(result.map((v, i) => [maps[i], v]));
};

await Promise.all(promises);