#!/usr/bin/env node
// Weekly fixture lists as A4 PDFs.
//   node fixtures.mjs [--week N] [--weeks K] [--date YYYY-MM-DD] [--root league]
// Default: the week after the last one recorded. --weeks makes K weeks in a row (one PDF each).
// Output: <root>/fixtures/week-NN-fixtures.pdf and week-NN.json (the fixture data).
//
// Format: every team plays every other team once a week (4 teams = 6 matches), two matches
// at a time on two pitches, so a week is 3 rounds and nobody sits out. The order rotates
// week to week: which pairings open and which pitch each match is on. No home/away.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadLeague, weeksOf, writeJSON, pad2, launchChromium, logoDataURL } from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };

const root = path.resolve(opt('root', 'league'));
const L = loadLeague(root);
const teams = L.config.teams.map((t) => t.name);
if (teams.length !== 4) die(`this schedule is for 4 teams (league.json has ${teams.length})`);
const S = L.config.schedule ?? {};
const pitches = S.pitches ?? ['Pitch 1', 'Pitch 2'];
const kickoffs = S.kickoffs ?? [];            // e.g. ["10:00", "10:40", "11:20"]; optional
const venue = S.venue ?? null;

// The three ways to split 4 teams into 2 games: each is one round.
const ROUNDS = [[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]];
// Round orders, cycled week by week. Chosen so a week never opens with the pairing the
// previous week closed on: nobody meets the same team twice in a row across weeks.
const ORDERS = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 2, 1], [2, 1, 0], [1, 0, 2]];

export function weekFixtures(week) {
  const order = ORDERS[(week - 1) % ORDERS.length];
  const cycle = Math.floor((week - 1) / ORDERS.length);
  return order.map((r, slot) => {
    let games = ROUNDS[r];
    if ((week + slot + cycle) % 2) games = [games[1], games[0]]; // swap pitches
    return {
      round: slot + 1,
      kickoff: kickoffs[slot] ?? null,
      games: games.map(([a, b], k) => ({ pitch: pitches[k] ?? `Pitch ${k + 1}`, teams: [teams[a], teams[b]] })),
    };
  });
}

const addDays = (d, n) => { const x = new Date(`${d}T12:00:00Z`); x.setUTCDate(x.getUTCDate() + n); return x.toISOString().slice(0, 10); };
const lastWeek = weeksOf(L).at(-1) ?? 0;
const first = Number(opt('week', lastWeek + 1));
const count = Math.max(1, Number(opt('weeks', 1)));
// date: given, else a week after the last recorded match day, else left off
const lastDate = L.matches.map((m) => m.date).sort().at(-1);
const dateFor = (w) => {
  if (opt('date')) return addDays(opt('date'), 7 * (w - first));
  if (lastDate && lastWeek) return addDays(lastDate, 7 * (w - lastWeek));
  return null;
};

const browser = await launchChromium();
try {
  for (let w = first; w < first + count; w++) {
    const data = { league: L.config.name, title_lines: L.config.title_lines, arabic_name: L.config.arabic_name, teams: L.config.teams, brand: L.config.brand,
      logo: logoDataURL(L), week: w, date: dateFor(w), venue, rounds: weekFixtures(w) };
    const outDir = path.join(root, 'fixtures');
    writeJSON(path.join(outDir, `week-${pad2(w)}.json`), { week: w, date: data.date, venue, rounds: data.rounds });
    const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
    page.on('pageerror', (e) => console.error('page error:', e.message));
    await page.goto(pathToFileURL(path.join(here, '..', 'templates', 'fixtures.html')).href);
    await page.evaluate(async (d) => { await document.fonts.ready; window.init(d); await window.assetsReady(); }, data);
    const out = path.join(outDir, `week-${pad2(w)}-fixtures.pdf`);
    await page.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await page.close();
    console.log(`✓ ${path.relative(process.cwd(), out)}`);
    for (const r of data.rounds) console.log(`   R${r.round}${r.kickoff ? ` ${r.kickoff}` : ''}: ${r.games.map((g) => `${g.teams[0]} v ${g.teams[1]} (${g.pitch})`).join('  |  ')}`);
  }
} finally { await browser.close(); }
