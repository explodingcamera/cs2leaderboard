const timestamp = new Date().toISOString().replace(/[:.-]/g, '_');
const day = new Date().toISOString().split('T')[0];

const url = 'https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=';

const currentSeason = 'official_leaderboard_premier_season1';
const regions = ['global', 'europe', 'africa', 'asia', "australia", "china", "northamerica", "southamerica"];

const fetchLeaderboard = async (region: string) => {
  const response = await fetch(`${url}${currentSeason}${region === "global" ? "" : "_"+region}`);
  const data = await response.json();
  return data;
}

const promises = regions.map(async (region) => {
  const data = await fetchLeaderboard(region);
  const filename = `./data/${region}_${timestamp}.json`;
  await Bun.write(filename, JSON.stringify(data));
  console.log(`Wrote ${filename}`);
});

await Promise.all(promises);