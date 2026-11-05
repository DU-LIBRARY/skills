# Video and graphics reference

All rendering is deterministic: an HTML template in the house style, drawn
frame by frame in headless Chromium from `weeks/week-NN/snapshot.json`, then
encoded with ffmpeg. The same data always gives the same video.

## render.mjs: weekly recap video + still cards

```bash
node higgsfield-football-league/scripts/render.mjs [flags]
```

| Flag | Default | Meaning |
|---|---|---|
| `--week N` | latest | Which week to render. |
| `--format story\|feed\|square` | `story` | 1080×1920 (Reels, Shorts, Status), 1080×1350 (feed), 1080×1080. |
| `--fps N` | 60 | Frame rate. 60 is what makes the moves look fluid on phones. |
| `--blur N` | 2 | Motion blur: sub-frames averaged per frame over a 180° shutter. `1` = off and twice as fast to render (good for drafts). |
| `--workers N` | min(4, CPUs) | Parallel browsers rendering frames, all feeding one encoder in order (no joins in the video). |
| `--only video\|cards` | both | Skip one half. |
| `--preview` | off | One JPEG per scene (`preview-<scene>.jpg`, git-ignored), no encoding. Use it to check layout in a few seconds. |
| `--intro clip.mp4` | — | Put a clip in front (scaled and cropped to fit). For AI intros, see ai-extras.md. |
| `--music track.mp3` | — | Background audio with fade in and out. Use only tracks the user has the rights to. |
| `--if-changed` | off | Skip if the MP4 exists and the numbers haven't changed (the Action uses this). |
| `--root dir` | `league` | League folder. |

Outputs in `league/weeks/week-NN/`:
- `week-NN-<format>.mp4`: about 35–40s, 60fps H.264, ~10 MB.
- `cards/{results,table,scorers,assists,talking}-feed.png`: 1080×1350 stills of each scene's final state.
- `snapshot.json`: the exact numbers drawn.

With the defaults on 4 CPUs, a 36s video takes about 3½ minutes (`--blur 1`: about 1¾). Use `--preview` while iterating.

### Scenes and timing

| Scene | Length | What moves |
|---|---|---|
| intro | 4.6s | Bismillah and دار العلوم fade up, "Darul Uloom / Football League" slide up out of masks, the star rule draws, crests settle in |
| results | 0.45s + 1.25s per match + 2.8s | Match cards sweep in from alternate sides, scores roll up like a scoreboard, scorer lines stagger in |
| table | 7.4s | Rows start in last week's order (alphabetical in week 1) and glide to the new order. Risers lift over fallers, the dark leader band follows whoever reaches the top, points roll, ▲▼ arrows settle in |
| scorers | 7.0s | Top 6 bar race: bars sweep in, then grow and re-rank from last week's totals. Numbers roll. Each bar's end band shows its medal live (gold, silver, bronze in flat colour; crimson for no medal), and the leader's bar fades to crimson as the race settles: from the start it reflects last week, and medals change hands as the counts tick over (0.3s blend) |
| assists | 7.0s | Same. Skipped until any assist is recorded |
| talking | ~5s | Leader (or "New leaders"), golden boot, hat-tricks or star of the week, most assists, biggest win |
| outro | 3.8s | Crests, title, totals so far |

Medal look and tie rule are settings in `league.json → brand`: `medal_style` (`tab` default; also `disc`, `bar`, `podium`, `badge`, combinable like `"disc tab"`) and `medal_ties` (`dense` default as above; `shared` = Olympic, `strict` = by list position).

Assists are shown the way match centres do: muted, after or under the scorer, with a small boxed **A** tag (`assistLine()` in `common.js`). Scenes too tall for the frame (e.g. two result cards in a 4:5 post) scale themselves down to fit.

Behind everything, a field of tiny Darul Uloom logos (`league/assets/logo.jpg`, set in `league.json → brand.logo`) drifts slowly; its strength is `brand.watermark_opacity` (0.07, very faint). The same field sits behind every graphic. Keep it faint: it's texture, not content.

Scenes hand over with a 0.9s overlap: the old scene lifts away, then the new one rises in, so the frame is never blank and text never sits on text.
How it's built, so it stays smooth when edited:
- Move things only with `transform`, `opacity` or `clip-path` (helper `tf(x, y, scale)` in vw). Animating `top`, `left` or `width` snaps to whole pixels and judders.
- Ease with `smooth` (quintic), `expoOut` for arrivals, or `settle` for a soft overshoot (`common.js`). Never switch a style instantly mid-move; blend it (`color-mix`).
- Numbers that change use `roller(from, to)`, which slides digits instead of swapping them.
- Fixed things (rank numbers, slot positions) stay put while the rows move past them.
- A colour that depends on a changing number (the medal band) is computed from the number shown at that instant and blended over 0.3s, so it changes live without a hard flip.

Change timing or layout in `templates/weekly.html` (each `build*` function
returns `{dur, still, draw(t)}`). Test it with `--preview` before a full render.

## graphic.mjs: matchday graphics

```bash
node higgsfield-football-league/scripts/graphic.mjs <type> [flags] [--format feed|story|square]
```

| Type | Flags | Output |
|---|---|---|
| `fulltime` | `--week N`, `--match ID` (default: every match that week) | `weeks/week-NN/cards/fulltime-<id>-<home>-v-<away>-<format>.png` |
| `potw` | `--week N`, `--player NAME` (default: most goals×2 + assists that week), `--photo img.jpg`, `--note "…"` | `weeks/week-NN/cards/potw-<player>-<format>.png` |
| `fixtures` | `--spec fx.json` | `graphics/<date>-fixtures-<format>.png` |
| `announcement` | `--title "…"`, `--body "…"` (`\n` for line breaks), `--kicker "…"`, `--band "…"` | `graphics/<today>-<title>-<format>.png` |

Fixtures spec:

```json
{ "date": "2026-11-29", "title": "Matchweek 4",
  "fixtures": [ { "home": "An Nasirun", "away": "As Sabiqun", "time": "10:00", "venue": "Main pitch" } ] }
```

A Player of the Week photo goes into a circular crop. Only use a photo the user
provides of that player. Without one, the team crest is used.

## Style

`templates/common.css` + `common.js` hold the shared style: colours from
`league.json → brand`, the faint logo field (`logoField()`), Barlow Condensed for type, Amiri for Arabic, the
bismillah, the star rule and the four crest shapes (`shield`, `roundel`,
`octagon`, `arch`) with each team's Arabic name on the band. Arabic is always shown without harakat (`plainAr()`), because vowel marks collide with lines above and below at display sizes. A new team needs
an entry in `league.json → teams` with `crest` set to one of those shapes.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `playwright not found` | `npm i -g playwright && npx playwright install chromium`. Set `CHROMIUM_PATH` to use a specific browser. |
| `ffmpeg not found` | `brew install ffmpeg` / `sudo apt-get install ffmpeg` |
| Boxes instead of letters | A font file is missing from `assets/fonts/`. Restore it from git. |
| Text overflows a card | Long names: check with `--preview`. Sizes are in `vw` in the templates. |
| `No matches recorded for week N` | That week has no saved matches. Run `league.mjs status`. |
| Video plays but numbers look wrong | Check `snapshot.json`, then `league.mjs check`. The renderer only draws what's there. |
