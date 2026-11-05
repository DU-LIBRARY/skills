#!/usr/bin/env node
// League data CLI.
//   node league.mjs add-week <week.json> [--root league] [--replace] [--add-players] [--dry-run]
//   node league.mjs snapshot [week] [--root league]      -> weeks/week-NN/snapshot.json (latest week if omitted)
//   node league.mjs status [--root league]
//   node league.mjs check [--root league]                -> validates the whole dataset
//   node league.mjs import <matches.json> <goals.json> [squads.json]
//                                                        -> take the dashboard's copy as the source of truth
//                                                           (keeps known weeks; new dates become new weeks)
import fs from 'node:fs';
import path from 'node:path';
import {
  loadLeague, saveLeague, resolveTeam, resolvePlayer, suggest, weeksOf, snapshot, writeJSON, weekDir, table, scorers, assists,
} from './lib.mjs';

const argv = process.argv.slice(2);
const flag = (name) => argv.includes(`--${name}`);
const opt = (name, d) => { const i = argv.indexOf(`--${name}`); return i >= 0 ? argv[i + 1] : d; };
const positional = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1] === '--root'));
const [cmd, arg] = positional;
const root = path.resolve(opt('root', 'league'));

const die = (msg) => { console.error(`✗ ${msg}`); process.exit(1); };

function parseScore(m) {
  if (m.score != null) {
    const s = String(m.score).match(/^\s*(\d+)\s*[-–:]\s*(\d+)\s*$/);
    if (!s) throw new Error(`can't read score "${m.score}" (use "3-1")`);
    return [Number(s[1]), Number(s[2])];
  }
  if (m.home_goals == null || m.away_goals == null) throw new Error('needs "score" or home_goals/away_goals');
  return [Number(m.home_goals), Number(m.away_goals)];
}

function addWeek(file) {
  if (!file) die('usage: add-week <week.json>');
  const input = JSON.parse(fs.readFileSync(file, 'utf8'));
  const L = loadLeague(root);
  const weeks = weeksOf(L);
  const week = Number(input.week ?? (weeks.length ? weeks[weeks.length - 1] + 1 : 1));
  if (!Number.isInteger(week) || week < 1) die(`bad week "${input.week}"`);
  if (weeks.includes(week) && !flag('replace')) die(`week ${week} already recorded; pass --replace to overwrite it`);
  if (!Array.isArray(input.matches) || !input.matches.length) die('no matches in the file');

  const errors = [], warnings = [], newPlayers = [];
  // drop the week being replaced before numbering
  if (flag('replace')) {
    const old = new Set(L.matches.filter((m) => Number(m.week) === week).map((m) => m.match));
    L.matches = L.matches.filter((m) => !old.has(m.match));
    L.goals = L.goals.filter((g) => !old.has(g.match));
  }
  let nextId = L.matches.reduce((mx, m) => Math.max(mx, Number(m.match) || 0), 0) + 1;

  const addedMatches = [], addedGoals = [];
  input.matches.forEach((m, i) => {
    const where = `match ${i + 1}`;
    const home = resolveTeam(L, m.home), away = resolveTeam(L, m.away);
    if (!home) errors.push(`${where}: unknown home team "${m.home}"`);
    if (!away) errors.push(`${where}: unknown away team "${m.away}"`);
    if (home && home === away) errors.push(`${where}: a team can't play itself`);
    let hg, ag;
    try { [hg, ag] = parseScore(m); } catch (e) { errors.push(`${where}: ${e.message}`); return; }
    const date = m.date ?? input.date;
    if (!date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) errors.push(`${where}: date must be YYYY-MM-DD (got "${date}")`);
    if (!home || !away) return;

    const id = nextId++;
    addedMatches.push({ match: id, week, date, home, away, home_goals: hg, away_goals: ag });

    const goals = m.goals ?? [];
    const tally = { [home]: 0, [away]: 0 };
    goals.forEach((g, j) => {
      const gw = `${where} goal ${j + 1}`;
      const team = resolveTeam(L, g.team);
      if (!team || (team !== home && team !== away)) { errors.push(`${gw}: team "${g.team}" isn't in ${home} v ${away}`); return; }
      tally[team]++;
      const og = !!g.own_goal;
      const scorerTeam = og ? (team === home ? away : home) : team;
      let scorer = g.scorer ? resolvePlayer(L, g.scorer, scorerTeam) : null;
      if (g.scorer && !scorer) {
        if (flag('add-players')) { scorer = g.scorer; newPlayers.push({ player: scorer, team: scorerTeam }); L.squads.push({ player: scorer, team: scorerTeam }); }
        else errors.push(`${gw}: "${g.scorer}" isn't in the ${scorerTeam} squad${suggest(L, g.scorer, scorerTeam).length ? ` (did you mean ${suggest(L, g.scorer, scorerTeam).join(', ')}?)` : ''}`);
      }
      if (!g.scorer && !og) warnings.push(`${gw}: no scorer named`);
      let assist = null;
      if (g.assist) {
        assist = resolvePlayer(L, g.assist, team);
        if (!assist) {
          if (flag('add-players')) { assist = g.assist; newPlayers.push({ player: assist, team }); L.squads.push({ player: assist, team }); }
          else errors.push(`${gw}: assist "${g.assist}" isn't in the ${team} squad${suggest(L, g.assist, team).length ? ` (did you mean ${suggest(L, g.assist, team).join(', ')}?)` : ''}`);
        }
        if (og) warnings.push(`${gw}: an assist on an own goal is unusual`);
      }
      addedGoals.push({ match: id, team, scorer: scorer ?? null, assist, own_goal: og });
    });
    if (goals.length) {
      if (tally[home] !== hg) errors.push(`${where}: ${home} scored ${hg} but ${tally[home]} goal(s) listed`);
      if (tally[away] !== ag) errors.push(`${where}: ${away} scored ${ag} but ${tally[away]} goal(s) listed`);
    } else if (hg + ag > 0) warnings.push(`${where}: no goal details; table updates but scorers/assists won't`);
  });

  warnings.forEach((w) => console.warn(`! ${w}`));
  if (errors.length) { errors.forEach((e) => console.error(`✗ ${e}`)); die(`${errors.length} problem(s); nothing saved`); }

  L.matches.push(...addedMatches);
  L.goals.push(...addedGoals);
  L.matches.sort((a, b) => a.week - b.week || String(a.date).localeCompare(String(b.date)) || a.match - b.match);
  if (flag('dry-run')) { console.log(JSON.stringify({ week, addedMatches, addedGoals, newPlayers }, null, 1)); return; }
  saveLeague(L);
  const snap = snapshot(L, week);
  writeJSON(path.join(weekDir(root, week), 'snapshot.json'), snap);
  console.log(`✓ week ${week}: ${addedMatches.length} match(es), ${addedGoals.length} goal(s) saved`);
  if (newPlayers.length) console.log(`✓ new players added to squads: ${newPlayers.map((p) => `${p.player} (${p.team})`).join(', ')}`);
  printTable(snap);
}

function printTable(snap) {
  console.log(`\nWeek ${snap.week} — ${snap.date}`);
  for (const r of snap.results) console.log(`  ${r.home} ${r.home_goals}-${r.away_goals} ${r.away}`);
  console.log('\n  #  Team           P  W  D  L  GF GA  GD Pts  Move');
  for (const r of snap.table) {
    const mv = r.prev_pos == null ? 'new' : r.move > 0 ? `▲${r.move}` : r.move < 0 ? `▼${-r.move}` : '–';
    console.log(`  ${r.pos}  ${r.team.padEnd(14)} ${[r.played, r.won, r.drawn, r.lost, r.gf, r.ga].map((n) => String(n).padStart(2)).join(' ')} ${String(r.gd).padStart(3)} ${String(r.points).padStart(3)}  ${mv}`);
  }
  if (snap.scorers.length) console.log(`\n  Top scorers: ${snap.scorers.slice(0, 5).map((s) => `${s.player} ${s.goals}`).join(' · ')}`);
  if (snap.assists.length) console.log(`  Top assists: ${snap.assists.slice(0, 5).map((s) => `${s.player} ${s.assists}`).join(' · ')}`);
}

function doSnapshot(w) {
  const L = loadLeague(root);
  const weeks = weeksOf(L);
  if (!weeks.length) die('no matches recorded yet');
  const targets = w === 'all' ? weeks : [Number(w ?? weeks[weeks.length - 1])];
  for (const week of targets) {
    const snap = snapshot(L, week);
    const out = path.join(weekDir(root, week), 'snapshot.json');
    writeJSON(out, snap);
    console.log(`✓ ${path.relative(process.cwd(), out)}`);
    if (targets.length === 1) printTable(snap);
  }
}

function status() {
  const L = loadLeague(root);
  const weeks = weeksOf(L);
  console.log(`${L.config.name} — ${L.squads.length} players, ${L.config.teams.length} teams, ${L.matches.length} matches, ${L.goals.length} goals, weeks: ${weeks.join(', ') || 'none'}`);
  if (weeks.length) printTable(snapshot(L, weeks[weeks.length - 1]));
}

function check() {
  const L = loadLeague(root);
  const problems = [];
  const ids = new Set();
  for (const m of L.matches) {
    if (ids.has(m.match)) problems.push(`duplicate match id ${m.match}`);
    ids.add(m.match);
    for (const side of ['home', 'away']) if (!resolveTeam(L, m[side])) problems.push(`match ${m.match}: unknown team ${m[side]}`);
    const gs = L.goals.filter((g) => g.match === m.match);
    if (gs.length) for (const [team, n] of [[m.home, m.home_goals], [m.away, m.away_goals]]) {
      const c = gs.filter((g) => g.team === team).length;
      if (c !== Number(n)) problems.push(`match ${m.match}: ${team} ${n} goals but ${c} listed`);
    }
  }
  for (const g of L.goals) if (!ids.has(g.match)) problems.push(`goal for missing match ${g.match}`);
  problems.forEach((p) => console.error(`✗ ${p}`));
  if (problems.length) process.exit(1);
  const t = table(L, L.matches);
  console.log(`✓ data consistent: ${L.matches.length} matches, ${L.goals.length} goals, leader ${t[0].team}, top scorer ${scorers(L.goals)[0]?.player ?? '—'}, top assists ${assists(L.goals)[0]?.player ?? '—'}`);
}

function importArtifact(mFile, gFile, sFile) {
  if (!mFile || !gFile) die('usage: import <matches.json> <goals.json> [squads.json]');
  const L = loadLeague(root);
  const am = JSON.parse(fs.readFileSync(mFile, 'utf8')), ag = JSON.parse(fs.readFileSync(gFile, 'utf8'));
  if (sFile) L.squads = JSON.parse(fs.readFileSync(sFile, 'utf8'));
  const known = Object.fromEntries(L.matches.map((m) => [m.match, Number(m.week)]));
  const weekOfDate = {};
  for (const m of L.matches) weekOfDate[m.date] ??= Number(m.week);
  let next = Math.max(0, ...Object.values(known)) + 1;
  const fresh = [...new Set(am.filter((m) => !known[m.match] && !weekOfDate[m.date]).map((m) => String(m.date)))].sort();
  for (const d of fresh) weekOfDate[d] = next++;
  L.matches = am.map((m) => ({ match: Number(m.match), week: Number(m.week ?? known[m.match] ?? weekOfDate[m.date]), date: String(m.date).slice(0, 10),
    home: resolveTeam(L, m.home) ?? m.home, away: resolveTeam(L, m.away) ?? m.away, home_goals: Number(m.home_goals), away_goals: Number(m.away_goals) }));
  L.goals = ag.map((g) => ({ match: Number(g.match), team: resolveTeam(L, g.team) ?? g.team, scorer: g.scorer || null, assist: g.assist || null, own_goal: !!g.own_goal && g.own_goal !== 'false' }));
  saveLeague(L);
  console.log(`✓ imported ${L.matches.length} matches, ${L.goals.length} goals; weeks ${weeksOf(L).join(', ') || 'none'}${fresh.length ? ` (new dates ${fresh.join(', ')} numbered as new weeks)` : ''}`);
  check();
}

try {
  if (cmd === 'add-week') addWeek(arg);
  else if (cmd === 'import') importArtifact(arg, positional[2], positional[3]);
  else if (cmd === 'snapshot') doSnapshot(arg);
  else if (cmd === 'status') status();
  else if (cmd === 'check') check();
  else die('commands: add-week <file> | snapshot [week|all] | status | check | import <matches> <goals> [squads]');
} catch (e) { die(e.message); }
