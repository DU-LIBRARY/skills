// Shared by weekly.html and graphic.html: helpers, crests, brand.
// ---------- helpers ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const ease = (p) => (p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
const easeOut = (p) => 1 - Math.pow(1 - p, 3);
// quintic ease-in-out: zero velocity AND acceleration at both ends, so motion never jerks
const smooth = (p) => { p = clamp(p); return p * p * p * (p * (p * 6 - 15) + 10); };
const expoOut = (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p));
// gentle settle with a little overshoot, for things arriving on screen
const settle = (p) => { p = clamp(p); return p >= 1 ? 1 : 1 - Math.exp(-6.5 * p) * Math.cos(5.2 * p); };
const back = (p) => { const c = 1.4, d = c + 1; return 1 + d * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
const prog = (t, start, dur) => clamp((t - start) / dur);
const disp = (x) => String(x).replace(/ʾ/g, '’').replace(/ʿ/g, '‘');
// Arabic without harakat: the vowel marks collide with neighbouring lines at display sizes
const plainAr = (x) => String(x ?? '').replace(/[\u064B-\u065F\u0670\u06D6-\u06ED]/g, '');
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = disp(text); return e; };
const fmtDate = (d) => { const x = new Date(d + 'T12:00:00Z'); return isNaN(x) ? d : x.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }); };
let uid = 0;
// Make crossings readable: risers lift over the top, fallers sink back and fade a touch.
// Returns the parts so callers can fold them into one transform.
function overtake(rise, p) {
  const k = Math.sin(Math.PI * clamp(p));
  if (rise > 0) return { x: -1.2 * k, s: 1 + .04 * k, o: 1, z: 30 + rise, shadow: `0 ${2 * k}vw ${4 * k}vw rgba(23,20,18,${(.3 * k).toFixed(3)})` };
  if (rise < 0) return { x: 1.6 * k, s: 1 - .05 * k, o: 1 - .4 * k, z: 10, shadow: 'none' };
  return { x: 0, s: 1, o: 1, z: 20, shadow: 'none' };
}

// A rolling number, like a stadium scoreboard: a column of digits slides, so a
// count from 1 to 4 moves continuously instead of stepping.
function roller(from, to, cls = '') {
  const lo = Math.min(from, to), hi = Math.max(from, to);
  const box = el('span', `roller ${cls}`), col = el('span', 'roller-col');
  for (let v = lo; v <= hi; v++) col.append(el('span', null, String(v)));
  box.append(col);
  return { node: box, set(v) { col.style.transform = `translate3d(0, ${-(clamp(v, lo, hi) - lo)}em, 0)`; } };
}

// The four crest shapes from the dashboard's team sheets.
const SHAPES = {
  shield:  { outer: 'M50 3 L94 15 V58 C94 86 74 104 50 115 C26 104 6 86 6 58 V15 Z', inner: 'M50 11 L86 21 V58 C86 81 70 96 50 106 C30 96 14 81 14 58 V21 Z', band: 47,
             pattern: '<pattern id="P" width="14" height="14" patternUnits="userSpaceOnUse"><g fill="none" stroke="#d75b6e" stroke-width="0.9" stroke-opacity=".55"><rect x="3.5" y="3.5" width="7" height="7"/><rect x="3.5" y="3.5" width="7" height="7" transform="rotate(45 7 7)"/></g></pattern>' },
  roundel: { outer: 'M50 13 A46 46 0 1 1 49.99 13 Z', inner: 'M50 20 A39 39 0 1 1 49.99 20 Z', band: 47,
             pattern: '<pattern id="P" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><g fill="none" stroke="#d75b6e" stroke-width="0.9" stroke-opacity=".55"><path d="M0 0 H10 M0 0 V10"/></g></pattern>' },
  octagon: { outer: 'M93.4,77.0 L68.0,102.4 L32.0,102.4 L6.6,77.0 L6.6,41.0 L32.0,15.6 L68.0,15.6 L93.4,41.0 Z', inner: 'M87.4,74.5 L65.5,96.4 L34.5,96.4 L12.6,74.5 L12.6,43.5 L34.5,21.6 L65.5,21.6 L87.4,43.5 Z', band: 47,
             pattern: '<pattern id="P" width="18" height="10.392" patternUnits="userSpaceOnUse"><g fill="none" stroke="#d75b6e" stroke-width="0.9" stroke-opacity=".55"><path d="M0 5.196 L3 0 H9 L12 5.196 L9 10.392 H3 Z M12 5.196 H18"/></g></pattern>' },
  arch:    { outer: 'M8 113 V54 C8 30 28 14 50 4 C72 14 92 30 92 54 V113 Z', inner: 'M15 106 V55 C15 35 32 21 50 12 C68 21 85 35 85 55 V106 Z', band: 51,
             pattern: '<pattern id="P" width="12" height="12" patternUnits="userSpaceOnUse"><g fill="none" stroke="#d75b6e" stroke-width="0.9" stroke-opacity=".55"><path d="M0 6 H6 V0 M6 12 V6 H12"/><rect x="1.5" y="1.5" width="3" height="3"/><rect x="7.5" y="7.5" width="3" height="3"/></g></pattern>' },
};
function crest(team) {
  const s = SHAPES[team.crest] || SHAPES.shield, id = `c${++uid}`;
  const wrap = document.createElement('div');
  wrap.innerHTML = `<svg viewBox="0 0 100 118"><defs>${s.pattern.replace('id="P"', `id="p${id}"`)}<clipPath id="k${id}"><path d="${s.inner}"/></clipPath></defs>
    <path d="${s.outer}" fill="url(#crestfill)" stroke="#f2ebdd" stroke-width="3"/>
    <g clip-path="url(#k${id})"><rect width="100" height="118" fill="url(#p${id})"/><rect x="0" y="${s.band}" width="100" height="24" fill="#141110"/><path d="M0 ${s.band} H100 M0 ${s.band + 24} H100" stroke="#d75b6e" stroke-width="1"/></g>
    <path d="${s.inner}" fill="none" stroke="#d75b6e" stroke-width="1.2"/>
    <text x="50" y="${s.band + 17}" text-anchor="middle" font-family="Amiri" font-weight="700" font-size="15" fill="#f2ebdd" textLength="46" lengthAdjust="spacingAndGlyphs">${plainAr(team.crest_text)}</text></svg>`;
  return wrap.firstElementChild;
}
const starRule = () => { const r = el('div', 'rule'); r.innerHTML = '<span></span><svg class="star"><use href="#star"/></svg><span></span>'; return r; };
function header(kicker, title) { const f = document.createDocumentFragment(); f.append(el('div', 'kicker', kicker), el('div', 'title', title), starRule()); return f; }


// shared SVG defs (crest gradient, star)
document.body.insertAdjacentHTML('afterbegin', `<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="crestfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2522"/><stop offset="1" stop-color="#0e0c0b"/></linearGradient>
    <symbol id="star" viewBox="0 0 20 20"><g fill="currentColor"><rect x="5" y="5" width="10" height="10"/><rect x="5" y="5" width="10" height="10" transform="rotate(45 10 10)"/></g></symbol>
  </defs>
</svg>`);

// brand colours from league.json override the defaults
function applyBrand(brand = {}) {
  const VARS = { cream: '--cream', paper: '--paper', ink: '--ink', ink2: '--ink2', crimson: '--crimson', crimsonLight: '--crimson-lt', up: '--up', down: '--down' };
  for (const [k, v] of Object.entries(brand)) if (VARS[k]) document.documentElement.style.setProperty(VARS[k], v);
}
const teamOf = (teams, name) => teams.find((t) => t.name === name) || { name, crest: 'shield', crest_text: '' };
