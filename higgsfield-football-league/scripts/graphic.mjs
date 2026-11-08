#!/usr/bin/env node
// Matchday graphics in the league's own style.
//   node graphic.mjs fulltime     [--week N] [--match ID]           one poster per match of the week (or just ID)
//   node graphic.mjs potw         [--week N] [--player NAME] [--photo img.jpg] [--note "..."]
//   node graphic.mjs fixtures     --spec fixtures.json              {date, title?, fixtures:[{home, away, time?, venue?, date?}]}
//   node graphic.mjs announcement --title "..." [--body "..."] [--kicker "..."]
//   node graphic.mjs thumbnail    [--week N] [--title "..."] [--body "..."]   "Week N Recap" cover (also opens the weekly video)
// Common: [--root league] [--format feed|story|square]
// Week graphics go to <root>/weeks/week-NN/cards/, the rest to <root>/graphics/.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadLeague, weeksOf, snapshot, readJSON, resolveTeam, resolvePlayer, weekDir, fold, launchChromium, logoDataURL } from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };
const type = argv[0];
const FORMATS = { story: [1080, 1920], feed: [1080, 1350], square: [1080, 1080] };
const format = opt('format', 'feed');
if (!FORMATS[format]) die(`format must be one of ${Object.keys(FORMATS).join(', ')}`);

const root = path.resolve(opt('root', 'league'));
const L = loadLeague(root);
const base = { league: L.config.name, teams: L.config.teams, brand: L.config.brand, logo: logoDataURL(L) };
const weeks = weeksOf(L);
const week = () => { if (!weeks.length) die('no matches recorded yet'); return Number(opt('week', weeks[weeks.length - 1])); };
const slug = (s) => fold(s).slice(0, 40) || 'graphic';
const today = new Date().toISOString().slice(0, 10);

const jobs = []; // [data, outPath]
if (type === 'fulltime') {
  const w = week(), snap = snapshot(L, w);
  const only = opt('match');
  for (const m of snap.results.filter((r) => !only || String(r.match) === String(only)))
    jobs.push([{ ...base, type, week: w, match: m }, path.join(weekDir(root, w), 'cards', `fulltime-${m.match}-${slug(m.home)}-v-${slug(m.away)}-${format}.png`)]);
  if (!jobs.length) die(`no match ${only} in week ${w}`);
} else if (type === 'potw') {
  const w = week(), snap = snapshot(L, w);
  const goals = snap.results.flatMap((r) => r.goals);
  const tally = {};
  for (const g of goals) {
    if (g.scorer && !g.own_goal) (tally[g.scorer] ??= { player: g.scorer, team: g.team, goals: 0, assists: 0 }).goals++;
    if (g.assist) (tally[g.assist] ??= { player: g.assist, team: g.team, goals: 0, assists: 0 }).assists++;
  }
  let p;
  if (opt('player')) {
    const name = resolvePlayer(L, opt('player'));
    if (!name) die(`no player "${opt('player')}" in the squads`);
    const team = L.squads.find((s) => s.player === name).team;
    p = tally[name] ?? { player: name, team, goals: 0, assists: 0 };
  } else {
    // default pick: goals count double, then assists, then name
    p = Object.values(tally).sort((a, b) => (2 * b.goals + b.assists) - (2 * a.goals + a.assists) || b.goals - a.goals || a.player.localeCompare(b.player))[0];
    if (!p) die('no goals this week to pick a player of the week from; pass --player');
  }
  const photo = opt('photo');
  if (photo) {
    if (!fs.existsSync(photo)) die(`photo not found: ${photo}`);
    const ext = path.extname(photo).slice(1).toLowerCase().replace('jpg', 'jpeg');
    p = { ...p, photo: `data:image/${ext};base64,${fs.readFileSync(photo).toString('base64')}` };
  }
  if (opt('note')) p = { ...p, note: opt('note') };
  jobs.push([{ ...base, type, week: w, player: p }, path.join(weekDir(root, w), 'cards', `potw-${slug(p.player)}-${format}.png`)]);
} else if (type === 'fixtures') {
  const spec = readJSON(path.resolve(opt('spec', '')), null);
  if (!spec?.fixtures?.length) die('--spec must point at {date, fixtures:[{home, away, time?, venue?}]}');
  const fixtures = spec.fixtures.map((f, i) => {
    const home = resolveTeam(L, f.home), away = resolveTeam(L, f.away);
    if (!home || !away) die(`fixture ${i + 1}: unknown team (${f.home} v ${f.away})`);
    return { ...f, home, away };
  });
  jobs.push([{ ...base, type, ...spec, fixtures, band_right: spec.band_right || 'Fixtures' }, path.join(root, 'graphics', `${spec.date || today}-fixtures-${format}.png`)]);
} else if (type === 'announcement') {
  if (!opt('title')) die('--title is required');
  jobs.push([{ ...base, type, title: opt('title'), body: opt('body', '').replace(/\\n/g, '\n'), kicker: opt('kicker'), band_right: opt('band', 'Announcement') },
    path.join(root, 'graphics', `${today}-${slug(opt('title'))}-${format}.png`)]);
} else if (type === 'thumbnail') {
  // the week's recap cover: also the first second of the weekly video (render.mjs makes it itself)
  const w = week(), snap = snapshot(L, w);
  const goals = snap.results.reduce((n, r) => n + r.home_goals + r.away_goals, 0), games = snap.results.length;
  const top = snap.table[0]?.team;
  const body = [`${games} game${games === 1 ? '' : 's'} · ${goals} goal${goals === 1 ? '' : 's'}`, top ? `${top} top of the table` : ''].filter(Boolean).join('\n');
  jobs.push([{ ...base, type: 'announcement', title: opt('title', `Week ${w} Recap`), body: opt('body', body).replace(/\\n/g, '\n'),
    kicker: opt('kicker', L.config.name), band_right: `Matchweek ${w}` }, path.join(weekDir(root, w), 'cards', `thumbnail-${format}.png`)]);
} else die('types: fulltime | potw | fixtures | announcement | thumbnail');


let browser;
try { browser = await launchChromium(); } catch (e) { die(e.message); }
try {
  const [w, h] = FORMATS[format];
  for (const [data, out] of jobs) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    page.on('pageerror', (e) => console.error('page error:', e.message));
    await page.goto(pathToFileURL(path.join(here, '..', 'templates', 'graphic.html')).href);
    await page.evaluate(async (d) => { await document.fonts.ready; window.init(d); await document.fonts.ready; await window.assetsReady(); }, data);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out });
    await page.close();
    console.log(`✓ ${path.relative(process.cwd(), out)}`);
  }
} finally { await browser.close(); }
