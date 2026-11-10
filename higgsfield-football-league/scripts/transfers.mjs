#!/usr/bin/env node
// A very short "Squad changes" video (and a still card) for team news: transfers and new signings.
//   node transfers.mjs --spec changes.json [--root league] [--format story|feed|square] [--fps 60] [--whatsapp] [--preview]
// changes.json: { week, title?, changes: [{ player, from?, to, fee?, note? }] }
//   fee is free text ("100 dinaar"). League videos never show fantasy data: no fantasy prices or positions.
//   from omitted = a new signing. Names are checked against the teams in league.json.
// Output: <root>/graphics/<YYYY-MM-DD>-squad-changes-<format>.mp4 and ...-feed.png
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadLeague, readJSON, resolveTeam, launchChromium, hasFfmpeg, logoDataURL } from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const flag = (n) => argv.includes(`--${n}`);
const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };
const FORMATS = { story: [1080, 1920], feed: [1080, 1350], square: [1080, 1080] };
const format = opt('format', 'story');
if (!FORMATS[format]) die(`format must be one of ${Object.keys(FORMATS).join(', ')}`);
const WHATSAPP = flag('whatsapp');
const fps = Number(opt('fps', WHATSAPP ? 30 : 60));

const root = path.resolve(opt('root', 'league'));
const L = loadLeague(root);
const spec = readJSON(path.resolve(opt('spec', '')), null);
if (!spec?.changes?.length) die('--spec must point at {week, changes:[{player, from?, to, fee?, note?}]}');
const changes = spec.changes.map((c, i) => {
  const to = resolveTeam(L, c.to), from = c.from ? resolveTeam(L, c.from) : null;
  if (!to || (c.from && !from)) die(`change ${i + 1}: unknown team (${c.from ?? 'new'} → ${c.to})`);
  return { ...c, to, from };
});
const data = { league: L.config.name, teams: L.config.teams, brand: L.config.brand, logo: logoDataURL(L), week: spec.week, title: spec.title, changes };
const date = spec.date || new Date().toISOString().slice(0, 10);
const outDir = path.join(root, 'graphics');
fs.mkdirSync(outDir, { recursive: true });
const base = path.join(outDir, `${date}-squad-changes`);
const template = pathToFileURL(path.join(here, '..', 'templates', 'transfers.html')).href;

async function open(browser, [w, h]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('page error:', e.message));
  await page.goto(template);
  const info = await page.evaluate(async (d) => { await document.fonts.ready; const r = window.init(d); await window.assetsReady(); return r; }, data);
  return { page, info };
}

let browser;
try { browser = await launchChromium(); } catch (e) { die(e.message); }
try {
  // still card (feed size), drawn at the end state
  { const { page, info } = await open(browser, FORMATS.feed);
    await page.evaluate((t) => window.renderAt(t), info.duration);
    await page.screenshot({ path: `${base}-feed.png` }); await page.close(); console.log(`✓ ${path.relative(process.cwd(), base)}-feed.png`); }
  const { page, info } = await open(browser, FORMATS[format]);
  if (flag('preview')) {
    for (const t of [0.6, 1.4, info.duration - 0.5]) { await page.evaluate((x) => window.renderAt(x), t); await page.screenshot({ path: `${base}-preview-${t.toFixed(1)}.jpg`, type: 'jpeg', quality: 80 }); }
    console.log('✓ previews written'); process.exit(0);
  }
  if (!hasFfmpeg()) die('ffmpeg not found');
  const [w, h] = FORMATS[format];
  const vw = WHATSAPP ? Math.round((w * 1280) / Math.max(w, h) / 2) * 2 : w, vh = WHATSAPP ? Math.round((h * 1280) / Math.max(w, h) / 2) * 2 : h;
  const out = `${base}-${format}${WHATSAPP ? '-whatsapp' : ''}.mp4`;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-vf', `scale=${vw}:${vh}:flags=lanczos`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '19', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error(`ffmpeg exited ${c}`)))));
  const frames = Math.ceil(info.duration * fps);
  for (let i = 0; i < frames; i++) {
    await page.evaluate((x) => window.renderAt(x), i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await done;
  console.log(`✓ ${path.relative(process.cwd(), out)} (${info.duration.toFixed(1)}s)`);
} finally { await browser.close(); }
