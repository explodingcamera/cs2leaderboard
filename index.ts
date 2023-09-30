import { regions } from './data/meta.json' assert { type: "json" };

const timestamp = new Date().toISOString().replace(/[:.-]/g, '_');
const url = 'https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_';
const currentSeason = 'season1';

const fetchLeaderboard = async (region: string) => {
  const response = await fetch(`${url}${currentSeason}${region === "global" ? "" : "_"+region}`);
  const data = await response.json();
  return data;
}

const promises = Object.keys(regions).map(async (region) => {
  const data = await fetchLeaderboard(region);
  const filename = `./data/historical/${region}/${timestamp}.json`;
  const filenameLatest = `./data/latest/${region}.json`;
  await Promise.all([
   Bun.write(filename, JSON.stringify(data)),
   Bun.write(filenameLatest, JSON.stringify(data)),
  ]);
});

await Promise.all(promises);
const datapoints = Bun.file("./data/timestamps.csv").writer();
await datapoints.write(`${timestamp}\n`);
await datapoints.flush();