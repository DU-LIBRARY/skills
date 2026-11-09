#!/usr/bin/env node
// The league standings as an A4 PDF: league table, every score so far (with scorers and
// assists), the full top scorers list and the full top assists list.
//   node report.mjs [--week N] [--root league]
// Default: after the latest week. Output: <root>/weeks/week-NN/week-NN-standings.pdf
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadLeague, weeksOf, snapshot, weekDir, pad2, launchChromium, logoDataURL } from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };

const root = path.resolve(opt('root', 'league'));
const L = loadLeague(root);
const weeks = weeksOf(L);
if (!weeks.length) die('no matches recorded yet — add a week first');
const week = Number(opt('week', weeks.at(-1)));
const snap = snapshot(L, week);

// every match up to this week, oldest first, each with its goals in the order recorded
const matches = L.matches.filter((m) => Number(m.week) <= week)
  .sort((a, b) => Number(a.week) - Number(b.week) || String(a.date).localeCompare(String(b.date)) || a.match - b.match)
  .map((m) => ({ ...m, goals: L.goals.filter((g) => g.match === m.match) }));

const data = { league: L.config.name, title_lines: L.config.title_lines, teams: L.config.teams, brand: L.config.brand, logo: logoDataURL(L),
  week, first_week: snap.first_week, table: snap.table, scorers: snap.scorers, assists: snap.assists, assists_recorded: snap.stats.assists_recorded,
  matches, totals: { matches: matches.length, goals: matches.reduce((n, m) => n + Number(m.home_goals) + Number(m.away_goals), 0) } };

const browser = await launchChromium();
try {
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  page.on('pageerror', (e) => console.error('page error:', e.message));
  await page.goto(pathToFileURL(path.join(here, '..', 'templates', 'report.html')).href);
  await page.evaluate(async (d) => { await document.fonts.ready; window.init(d); await window.assetsReady(); }, data);
  const outDir = weekDir(root, week);
  fs.mkdirSync(outDir, { recursive: true });
  const out = path.join(outDir, `week-${pad2(week)}-standings.pdf`);
  await page.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await page.close();
  console.log(`✓ ${path.relative(process.cwd(), out)}`);
} finally { await browser.close(); }
