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
| `--fps N` | 30 | Frame rate. |
| `--only video\|cards` | both | Skip one half. |
| `--preview` | off | One JPEG per scene (`preview-<scene>.jpg`, git-ignored), no encoding. Use it to check layout in a few seconds. |
| `--intro clip.mp4` | — | Put a clip in front (scaled and cropped to fit). For AI intros, see ai-extras.md. |
| `--music track.mp3` | — | Background audio with fade in and out. Use only tracks the user has the rights to. |
| `--if-changed` | off | Skip if the MP4 exists and the numbers haven't changed (the Action uses this). |
| `--root dir` | `league` | League folder. |

Outputs in `league/weeks/week-NN/`:
- `week-NN-<format>.mp4`: about 35–40s, H.264, ~3 MB.
- `cards/{results,table,scorers,assists,talking}-feed.png`: 1080×1350 stills of each scene's final state.
- `snapshot.json`: the exact numbers drawn.

Rendering takes about 2 seconds per second of video. A 37s video is about 70s of work.

### Scenes and timing

| Scene | Length | What moves |
|---|---|---|
| intro | 3.4s | Bismillah, title, matchweek and date, the four crests pop in |
| results | 2.2s + 1.1s per match + 1.6s | Match cards slide in, scores count up, scorers and assists listed |
| table | 6.6s | Rows start in last week's order (alphabetical in week 1) and glide to the new order. Risers lift over fallers. Points count up, ▲▼ arrows pop |
| scorers | 6.2s | Top 6 bar race from last week's totals to this week's |
| assists | 6.2s | Same. Skipped until any assist is recorded |
| talking | ~4–6s | Leader (or "New leaders"), golden boot, hat-tricks or star of the week, most assists, biggest win |
| outro | 3s | Crests, totals so far |

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
`league.json → brand`, Barlow Condensed for type, Amiri for Arabic, the
bismillah, the star rule and the four crest shapes (`shield`, `roundel`,
`octagon`, `arch`) with each team's Arabic name on the band. A new team needs
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
