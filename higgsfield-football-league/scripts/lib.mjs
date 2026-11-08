// Shared league logic. No dependencies. The maths here mirrors the league
// dashboard's own calcs (league_table, scorers, assists, defence) so the video, the
// cards and the dashboard always agree.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execSync, spawnSync } from 'node:child_process';

export const readJSON = (p, fallback) => {
  if (!fs.existsSync(p)) return fallback;
  return JSON.parse(fs.readFileSync(p, 'utf8'));
};
export const writeJSON = (p, v) => {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(v, null, 1) + '\n');
};

// "An Nasirun", "an-nāṣirūn", "AN-NASIRUN" all fold to the same key.
export const fold = (s) => String(s ?? '')
  .normalize('NFD').replace(/\p{M}/gu, '')
  .replace(/[ʾʿ'’`]/g, '').replace(/[^\p{L}\p{N}]+/gu, '').toLowerCase();

export function loadLeague(root) {
  const config = readJSON(path.join(root, 'league.json'));
  if (!config) throw new Error(`No league.json in ${root}`);
  const data = path.join(root, 'data');
  return {
    root, config,
    squads: readJSON(path.join(data, 'squads.json'), []),
    matches: readJSON(path.join(data, 'matches.json'), []),
    goals: readJSON(path.join(data, 'goals.json'), []),
  };
}

export function saveLeague(L) {
  const data = path.join(L.root, 'data');
  writeJSON(path.join(data, 'squads.json'), L.squads);
  writeJSON(path.join(data, 'matches.json'), L.matches);
  writeJSON(path.join(data, 'goals.json'), L.goals);
}

export const teamNames = (L) => L.config.teams.map((t) => t.name);

export function resolveTeam(L, name) {
  const k = fold(name);
  const t = L.config.teams.find((x) => fold(x.name) === k || fold(x.short) === k || fold(x.crest_text) === k);
  return t ? t.name : null;
}

export function resolvePlayer(L, name, team) {
  const k = fold(name);
  const pool = team ? L.squads.filter((p) => p.team === team) : L.squads;
  const exact = pool.find((p) => fold(p.player) === k);
  if (exact) return exact.player;
  // unique prefix match ("Hamza L" -> "Hamza Lakota")
  const pre = pool.filter((p) => fold(p.player).startsWith(k));
  return pre.length === 1 ? pre[0].player : null;
}

export const suggest = (L, name, team) => {
  const k = fold(name).slice(0, 3);
  return L.squads.filter((p) => (!team || p.team === team) && fold(p.player).includes(k)).map((p) => p.player);
};

export const weeksOf = (L) => [...new Set(L.matches.map((m) => Number(m.week)))].filter(Number.isFinite).sort((a, b) => a - b);

// ---- standings (same rules as the dashboard) ----
export function table(L, matches) {
  const pts = L.config.points;
  const t = {};
  for (const name of teamNames(L)) t[name] = { team: name, played: 0, won: 0, drawn: 0, lost: 0, gf: 0, ga: 0, gd: 0, points: 0, form: [] };
  const ordered = [...matches].sort((a, b) => String(a.date).localeCompare(String(b.date)) || a.match - b.match);
  for (const m of ordered) {
    const h = t[m.home], a = t[m.away], hg = Number(m.home_goals), ag = Number(m.away_goals);
    if (!h || !a) continue;
    h.played++; a.played++; h.gf += hg; h.ga += ag; a.gf += ag; a.ga += hg;
    if (hg > ag) { h.won++; a.lost++; h.points += pts.win; a.points += pts.loss; h.form.push('W'); a.form.push('L'); }
    else if (hg < ag) { a.won++; h.lost++; a.points += pts.win; h.points += pts.loss; a.form.push('W'); h.form.push('L'); }
    else { h.drawn++; a.drawn++; h.points += pts.draw; a.points += pts.draw; h.form.push('D'); a.form.push('D'); }
  }
  return Object.values(t).map((r) => ({ ...r, gd: r.gf - r.ga, form: r.form.slice(-5) }))
    .sort((x, y) => y.points - x.points || y.gd - x.gd || y.gf - x.gf || x.team.localeCompare(y.team))
    .map((r, i) => ({ pos: i + 1, ...r }));
}

export function scorers(goals) {
  const p = {};
  for (const g of goals) if (g.scorer && !g.own_goal) (p[g.scorer] ??= { player: g.scorer, team: g.team, goals: 0 }).goals++;
  return Object.values(p).sort((x, y) => y.goals - x.goals || x.player.localeCompare(y.player));
}

export function assists(goals) {
  const p = {};
  for (const g of goals) if (g.assist) (p[g.assist] ??= { player: g.assist, team: g.team, assists: 0 }).assists++;
  return Object.values(p).sort((x, y) => y.assists - x.assists || x.player.localeCompare(y.player));
}

export function defence(L, matches) {
  const t = {};
  for (const name of teamNames(L)) t[name] = { team: name, played: 0, conceded: 0, clean_sheets: 0 };
  for (const m of matches) for (const [side, against] of [[m.home, Number(m.away_goals)], [m.away, Number(m.home_goals)]]) {
    const r = t[side]; if (!r) continue;
    r.played++; r.conceded += against; if (against === 0) r.clean_sheets++;
  }
  return Object.values(t).sort((x, y) => x.conceded - y.conceded || y.clean_sheets - x.clean_sheets || x.team.localeCompare(y.team));
}

// Everything the video and cards need for one week: this week's standings, last week's
// standings (for the movement), the week's results and the talking points.
export function snapshot(L, week) {
  week = Number(week);
  const upTo = (w) => L.matches.filter((m) => Number(m.week) <= w);
  const ids = (ms) => new Set(ms.map((m) => m.match));
  const goalsIn = (ms) => { const s = ids(ms); return L.goals.filter((g) => s.has(g.match)); };

  const now = upTo(week), before = upTo(week - 1);
  const thisWeek = L.matches.filter((m) => Number(m.week) === week)
    .sort((a, b) => String(a.date).localeCompare(String(b.date)) || a.match - b.match);
  if (!thisWeek.length) throw new Error(`No matches recorded for week ${week}`);
  const weekGoals = goalsIn(thisWeek);

  const results = thisWeek.map((m) => ({
    ...m,
    goals: weekGoals.filter((g) => g.match === m.match),
  }));

  const tNow = table(L, now), tBefore = table(L, before);
  const prevPos = Object.fromEntries(tBefore.map((r) => [r.team, before.length ? r.pos : null]));
  const tableRows = tNow.map((r) => {
    const b = tBefore.find((x) => x.team === r.team);
    return { ...r, prev_pos: prevPos[r.team], prev_points: b ? b.points : 0, move: prevPos[r.team] ? prevPos[r.team] - r.pos : 0 };
  });

  const sNow = scorers(goalsIn(now)), sBefore = scorers(goalsIn(before));
  const aNow = assists(goalsIn(now)), aBefore = assists(goalsIn(before));
  const withPrev = (nowRows, beforeRows, key) => nowRows.map((r, i) => {
    const bi = beforeRows.findIndex((x) => x.player === r.player);
    return { rank: i + 1, ...r, prev: bi >= 0 ? beforeRows[bi][key] : 0, prev_rank: bi >= 0 ? bi + 1 : null };
  });

  // talking points
  // the week's top scorer(s): most goals across the gameweek (joint if tied)
  const wsc = scorers(weekGoals);
  const weekTop = wsc.length ? wsc.filter((s) => s.goals === wsc[0].goals) : [];
  // a hat-trick is 3+ goals in ONE match, never goals added up across the week's matches
  const hatTricks = [];
  for (const m of thisWeek) {
    for (const s of scorers(weekGoals.filter((g) => g.match === m.match))) {
      if (s.goals >= 3) hatTricks.push({ ...s, match: m.match, opponent: s.team === m.home ? m.away : m.home });
    }
  }
  let biggest = null;
  for (const m of thisWeek) {
    const margin = Math.abs(m.home_goals - m.away_goals);
    if (margin > 0 && (!biggest || margin > biggest.margin)) biggest = { match: m.match, margin, home: m.home, away: m.away, home_goals: m.home_goals, away_goals: m.away_goals };
  }
  const leaderChanged = before.length > 0 && tBefore[0].team !== tNow[0].team;

  return {
    league: L.config.name,
    title_lines: L.config.title_lines ?? null,
    arabic_name: L.config.arabic_name ?? null,
    season: L.config.season,
    week,
    date: thisWeek[thisWeek.length - 1].date,
    first_week: before.length === 0,
    stats: {
      matches_played: now.length,
      total_goals: now.reduce((s, m) => s + Number(m.home_goals) + Number(m.away_goals), 0),
      week_goals: thisWeek.reduce((s, m) => s + Number(m.home_goals) + Number(m.away_goals), 0),
      assists_recorded: goalsIn(now).some((g) => g.assist),
    },
    results,
    table: tableRows,
    scorers: withPrev(sNow, sBefore, 'goals'),
    assists: withPrev(aNow, aBefore, 'assists'),
    defence: defence(L, now),
    highlights: {
      leader: tNow[0].team,
      leader_changed: leaderChanged,
      previous_leader: before.length ? tBefore[0].team : null,
      top_scorer: sNow[0] || null,
      top_assist: aNow[0] || null,
      week_top_scorer: wsc[0] || null,
      week_top_scorers: weekTop,
      hat_tricks: hatTricks,
      biggest_win: biggest,
    },
    teams: L.config.teams,
    brand: L.config.brand,
  };
}

export const pad2 = (n) => String(n).padStart(2, '0');
export const weekDir = (root, week) => path.join(root, 'weeks', `week-${pad2(week)}`);

// Find Playwright wherever it is installed: local, global (`npm i -g playwright`) or preinstalled.
export function loadChromium() {
  const require = createRequire(import.meta.url);
  const paths = [process.cwd()];
  try { paths.push(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim()); } catch {}
  paths.push('/opt/node-tools/node_modules');
  for (const p of [null, ...paths]) {
    try { return (p ? require(require.resolve('playwright', { paths: [p] })) : require('playwright')).chromium; } catch {}
  }
  throw new Error('playwright not found — run `npm i -g playwright && npx playwright install chromium`');
}
export const launchChromium = () => loadChromium().launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
export const hasFfmpeg = () => spawnSync('ffmpeg', ['-version']).status === 0;

// The league logo as a data URL, for the faint background watermark. Added at render
// time only (never into snapshot.json) so snapshots stay small and comparable.
export function logoDataURL(L) {
  const rel = L.config.brand?.logo;
  if (!rel) return null;
  const p = path.resolve(L.root, rel);
  if (!fs.existsSync(p)) return null;
  const ext = path.extname(p).slice(1).toLowerCase().replace('jpg', 'jpeg');
  return `data:image/${ext};base64,${fs.readFileSync(p).toString('base64')}`;
}

// Weekly round-robin for 4 teams: every team plays every other once a week, two games at a
// time, so 3 rounds. The three possible pairings are cycled through all 6 orders, chosen so
// a week never opens with the pairing the previous week closed on; the two games swap
// pitches. No home/away.
const ROUNDS = [[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]];
const ORDERS = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 2, 1], [2, 1, 0], [1, 0, 2]];
export function weekFixtures(L, week) {
  const teams = L.config.teams.map((t) => t.name);
  if (teams.length !== 4) throw new Error(`the weekly schedule is for 4 teams (league.json has ${teams.length})`);
  const S = L.config.schedule ?? {};
  const pitches = S.pitches ?? ['Pitch 1', 'Pitch 2'];
  const kickoffs = S.kickoffs ?? [];
  const order = ORDERS[(week - 1) % ORDERS.length];
  const cycle = Math.floor((week - 1) / ORDERS.length);
  return order.map((r, slot) => {
    let games = ROUNDS[r];
    if ((week + slot + cycle) % 2) games = [games[1], games[0]];
    return { round: slot + 1, kickoff: kickoffs[slot] ?? null,
      games: games.map(([a, b], k) => ({ pitch: pitches[k] ?? `Pitch ${k + 1}`, teams: [teams[a], teams[b]] })) };
  });
}
