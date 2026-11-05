#!/usr/bin/env node
// Render the weekly animation and still cards from the league data.
//   node render.mjs [--week N] [--root league] [--format story|feed|square] [--fps 30]
//                   [--only video|cards] [--intro intro.mp4] [--music track.mp3] [--preview] [--if-changed]
// Output: <root>/weeks/week-NN/
//   week-NN-<format>.mp4            the animated recap (table movement, scorer and assist races)
//   cards/<scene>-feed.png           still graphics for posting (results, table, scorers, assists, talking points)
//   snapshot.json                    the numbers every frame was drawn from
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadLeague, weeksOf, snapshot, writeJSON, weekDir, pad2, launchChromium, hasFfmpeg } from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const flag = (n) => argv.includes(`--${n}`);
const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };

const FORMATS = { story: [1080, 1920], feed: [1080, 1350], square: [1080, 1080] };
const root = path.resolve(opt('root', 'league'));
const format = opt('format', 'story');
if (!FORMATS[format]) die(`format must be one of ${Object.keys(FORMATS).join(', ')}`);
const fps = Number(opt('fps', 30));
const only = opt('only');
const L = loadLeague(root);
const weeks = weeksOf(L);
if (!weeks.length) die('no matches recorded yet — add a week first');
const week = Number(opt('week', weeks[weeks.length - 1]));
const snap = snapshot(L, week);
const outDir = weekDir(root, week);
const snapPath = path.join(outDir, 'snapshot.json');
// --if-changed: skip when this week's video already exists and its numbers haven't moved
// (used by the GitHub Action so a local render isn't redone).
if (flag('if-changed') && fs.existsSync(path.join(outDir, `week-${pad2(week)}-${format}.mp4`)) && fs.existsSync(snapPath)
  && fs.readFileSync(snapPath, 'utf8') === JSON.stringify(snap, null, 1) + '\n') {
  console.log(`= week ${week} unchanged and already rendered; skipping`); process.exit(0);
}
fs.mkdirSync(path.join(outDir, 'cards'), { recursive: true });
writeJSON(snapPath, snap);

if (!hasFfmpeg()) die('ffmpeg not found — install it (brew install ffmpeg / apt-get install ffmpeg)');

const template = pathToFileURL(path.join(here, '..', 'templates', 'weekly.html')).href;

async function openPage(browser, [w, h], opts) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('page error:', e.message); });
  await page.goto(template);
  const info = await page.evaluate(async ([d, o]) => { await document.fonts.ready; const r = window.init(d, o); await document.fonts.ready; return r; }, [snap, opts]);
  return { page, info };
}

async function renderVideo(browser) {
  const size = FORMATS[format];
  const { page, info } = await openPage(browser, size, {});
  const frames = flag('preview') ? 0 : Math.ceil(info.duration * fps);
  const base = path.join(outDir, `week-${pad2(week)}-${format}`);
  const silent = `${base}.silent.mp4`, final = `${base}.mp4`;

  if (flag('preview')) {
    // a contact sheet of stills, for a quick look without encoding
    for (const s of info.scenes) {
      await page.evaluate((t) => window.renderAt(t), s.start + (s.still ?? s.dur / 2));
      await page.screenshot({ path: path.join(outDir, `preview-${s.id}.jpg`), type: 'jpeg', quality: 80 });
    }
    console.log(`✓ previews in ${path.relative(process.cwd(), outDir)}`);
    await page.close(); return;
  }

  console.log(`rendering ${frames} frames (${info.duration.toFixed(1)}s @ ${fps}fps, ${size.join('×')})…`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '18', '-movflags', '+faststart', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error(`ffmpeg exited ${c}`)))));
  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.renderAt(t), i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % (fps * 5) === 0) process.stdout.write(`  ${Math.round((100 * i) / frames)}%\r`);
  }
  ff.stdin.end();
  await done;
  await page.close();
  console.log(`  frames done in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  finish(silent, final, info.duration, size);
  console.log(`✓ ${path.relative(process.cwd(), final)}`);
}

// Optional: put an AI-generated intro clip (e.g. from `higgsfield generate`) in front,
// and/or lay a music track under the whole thing.
function finish(silent, final, duration, [w, h]) {
  const intro = opt('intro'), music = opt('music');
  let video = silent;
  if (intro) {
    if (!fs.existsSync(intro)) die(`intro clip not found: ${intro}`);
    const joined = silent.replace('.silent.mp4', '.joined.mp4');
    const fit = `scale=${w}:${h}:force_original_aspect_ratio=increase,crop=${w}:${h},fps=${fps},format=yuv420p,setsar=1`;
    run(['-y', '-loglevel', 'error', '-i', intro, '-i', silent, '-filter_complex', `[0:v]${fit}[a];[1:v]${fit}[b];[a][b]concat=n=2:v=1:a=0[v]`, '-map', '[v]', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', joined]);
    fs.rmSync(silent); video = joined;
    duration += Number(spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', intro]).stdout.toString()) || 0;
  }
  if (music) {
    if (!fs.existsSync(music)) die(`music not found: ${music}`);
    run(['-y', '-loglevel', 'error', '-i', video, '-i', music, '-filter_complex', `[1:a]afade=t=in:d=0.5,afade=t=out:st=${Math.max(0, duration - 1.5)}:d=1.5[a]`,
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final]);
    fs.rmSync(video);
  } else fs.renameSync(video, final);
}
function run(args) { const r = spawnSync('ffmpeg', args, { stdio: 'inherit' }); if (r.status !== 0) die(`ffmpeg failed: ${args.join(' ')}`); }

async function renderCards(browser) {
  const ids = ['results', 'table', 'scorers', 'assists', 'talking'];
  for (const id of ids) {
    let res;
    try { res = await openPage(browser, FORMATS.feed, { still: true, only: id }); } catch { continue; } // scene not in this week (e.g. no assists recorded)
    await res.page.evaluate((i) => window.renderAt(window.stillTime(i)), id);
    const out = path.join(outDir, 'cards', `${id}-feed.png`);
    await res.page.screenshot({ path: out });
    await res.page.close();
    console.log(`✓ ${path.relative(process.cwd(), out)}`);
  }
}

let browser;
try { browser = await launchChromium(); } catch (e) { die(e.message); }
try {
  if (only !== 'cards') await renderVideo(browser);
  if (only !== 'video' && !flag('preview')) await renderCards(browser);
} finally { await browser.close(); }
