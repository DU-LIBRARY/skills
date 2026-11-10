---
version: 0.13.0
name: higgsfield-football-league
description: |
  Run a weekly amateur football league: record the week's results, scorers
  and assists, update the league table, top scorers and top assists, render
  an animated recap video showing how the table and scorer/assist races
  moved, make matchday graphics (full time, player of the week, fixtures,
  announcements), sync the Darul Uloom Winter League dashboard artifact, and save
  everything to the repo. Use when: "here are this week's scores", "add
  the results", "update the league", "make the weekly video/animation",
  "who's top scorer", "player of the week", "make a fixtures poster",
  "post a league announcement", or "sync the dashboard". Chain: optional
  AI intro clips or hype art via higgsfield-generate. NOT for: real
  professional leagues' live data, betting odds, generic sports clips
  with no league data (use higgsfield-generate), or narrated explainers
  (use higgsfield-video-explainer).
argument-hint: "[this week's results as text] [--week N] [--format story|feed|square]"
allowed-tools: Bash, Read, Write, Edit
---

# Darul Uloom Winter League — weekly results, animation, graphics

The user runs the Darul Uloom Winter League (4 teams, 8-player squads) and sends results
every week. This skill turns that message into four things:
**saved data → updated standings → recap video + graphics → synced dashboard**,
and commits all of it to this repo.

Every number on screen is drawn by code from `league/data/`. **Never let an AI
image or video model render scores, names, tables or stats**: they get them
wrong. AI generation (`higgsfield`) is only for optional mood pieces. See
[references/ai-extras.md](references/ai-extras.md).

## Where things live

```
league/                         ← the league's data and outputs (repo root)
  league.json                   teams (name, Arabic name, crest shape), points rules, brand, dashboard slug
  data/squads.json              {player, team}: same rows as the dashboard's "Team sheet"
  data/matches.json             {match, week, date, home, away, home_goals, away_goals}
  data/goals.json               {match, team, scorer, assist, own_goal}: one row per goal
  weeks/week-NN/                snapshot.json, week-NN-story.mp4, cards/*.png
  graphics/                     fixtures posters and announcements (not tied to a week)
higgsfield-football-league/
  scripts/league.mjs            add-week | snapshot | status | check | import
  scripts/render.mjs            the recap video and still cards
  scripts/graphic.mjs           fulltime | potw | fixtures | announcement
  scripts/transfers.mjs         squad changes video (transfers, new signings)
  scripts/fixtures.mjs          weekly fixture list PDFs (rotating round-robin)
  templates/                    weekly.html, graphic.html, common.{css,js}: the house style
  assets/fonts/                 Barlow Condensed and Amiri (bundled, OFL)
```

Run scripts from the repo root (they default to `--root league`).
Requirements: Node 18+, `ffmpeg`, Playwright Chromium. Check with
`node higgsfield-football-league/scripts/league.mjs status`.

## The weekly flow

When the user sends results, do these stages in order. Don't stop to ask
questions you can settle from the data; ask only about real ambiguities
(see stage 1).

### 1. Parse the message → `week.json`

Turn whatever they wrote ("Nasirun 3-1 Faizun, Asjad x2 (Umar), Lorgat…")
into the input format in [references/weekly-input.md](references/weekly-input.md).
Write it to the scratchpad, not the repo. Team and player names can be loose
(no diacritics, first names, unique prefixes): the script resolves them.

Ask the user only when:
- A scorer's name matches several players or none ("Hamza": Hamza Y or Hamza Lakota?).
- The goals listed don't add up to the score and you can't tell which is wrong.
- It's unclear whether a goal was an own goal.

Missing assists are fine: leave `assist` out. Don't invent assists.

### 2. Save → `league.mjs add-week`

```bash
node higgsfield-football-league/scripts/league.mjs add-week /path/to/week.json
```

It validates everything (teams, squads, goals vs score), saves only if all
is well, writes `weeks/week-NN/snapshot.json`, and prints the new table
with movement arrows and the top scorers and assists. On `✗` errors, fix the
JSON (the messages say what's wrong, e.g. `did you mean Asjad?`) and re-run.
Nothing is saved on error. Flags: `--replace` (correct a week already
saved), `--add-players` (guest or new players: confirm with the user first),
`--dry-run`.

### 3. Render → video + cards + graphics

```bash
node higgsfield-football-league/scripts/render.mjs                 # latest week: 60fps 9:16 video + 4:5 cards (~3½ min)
node higgsfield-football-league/scripts/graphic.mjs fulltime       # a Full Time poster per match
node higgsfield-football-league/scripts/graphic.mjs potw           # Player of the Week (auto-picked, or --player)
```

Video scenes: thumbnail ("Week N Recap", 1s, also the file's cover) → results (with scorers and assists) → league table
(rows glide from last week's positions, points count up, ▲▼ arrows) → top
goalscorers race → top assists race (skipped until assists are recorded) →
talking points (leader, the week’s top scorer, golden boot, single-match hat-tricks, biggest win) → outro.

Before you hand it over, spot-check: `render.mjs --preview` writes one still
per scene as `preview-*.jpg` (git-ignored). Read two or three of them as images.
Animation rules (keep it smooth: transforms only, eased, no instant switches), formats, flags, the other graphic types and troubleshooting are in
[references/video-and-graphics.md](references/video-and-graphics.md).

### 4. Sync the dashboard artifact

Upload the new `matches.json` and `goals.json` (plus `squads.json` if
players changed) to the Darul Uloom Winter League dashboard and point its datasets at
them. Exact steps are in [references/dashboard-sync.md](references/dashboard-sync.md).
The dashboard computes its own table from these files, so after syncing it
matches the video exactly.

### 5. Auto-save → commit and push

Always finish by saving to the repo:

```bash
git add league && git commit -m "League: matchweek N results, video and graphics" && git push -u origin <current-branch>
```

The repo's `Football weekly render` GitHub Action also watches
`league/data/**`: if data is pushed without outputs (e.g. edited on GitHub),
it renders the video and graphics and commits them back. A week already
rendered locally is skipped (`--if-changed`).

### 6. Hand over

Tell the user, briefly: the results saved, the new top 3 and any movement
worth noting, the top scorer and top assister, and the files (video path, card
paths). Send the MP4 and the table card with SendUserFile when that tool is
available. Mention anything you assumed (e.g. "no assists given for the 2nd goal").

## Other requests

| User says | Do |
|---|---|
| "Fix last week: it was 2-2 not 2-1" | Edit the week JSON, `add-week --replace`, re-render that week **and every later week** (`--week N` each), then sync and commit. |
| "Make a launch/intro video" / "introduce the teams" | `render.mjs --launch [--date YYYY-MM-DD]`: logo (frame 0), opening hadith, title, each team with crest, Arabic name, squad and manager, Matchweek 1 fixtures, closing hadith (~46s). Output `league/launch/launch-story.mp4` |
| "Make this week's fixtures" / "fixture list PDF" | `fixtures.mjs [--week N] [--weeks K] [--date YYYY-MM-DD]`: A4 PDF in `league/fixtures/`, 3 rounds of 2 simultaneous games, order rotates every week, no home/away ([video-and-graphics.md](references/video-and-graphics.md)) |
| "Make a fixtures poster for Saturday" | `graphic.mjs fixtures --spec fx.json` ([video-and-graphics.md](references/video-and-graphics.md)) |
| "Post that the games are off" | `graphic.mjs announcement --title … --body …` |
| "Player of the week is X" | `graphic.mjs potw --player X [--photo path] [--note …]` |
| "It looks bad on WhatsApp" | Re-render with `--whatsapp` (still background, 30fps, 720p) and send `*-whatsapp.mp4`; tell them about HD / send as Document |
| "Make it square / for the feed" | `render.mjs --format square` or `feed` |
| "Add music" / "add an AI intro" | `render.mjs --music track.mp3` / `--intro clip.mp4`; see [ai-extras.md](references/ai-extras.md) |
| "I entered the results on the dashboard" | Pull them into the repo: [dashboard-sync.md](references/dashboard-sync.md) → "Dashboard → repo", then render, commit. |
| "New player joined X" / "the teams have changed" | Diff the new team sheet against `data/squads.json`. Mid-season, give each moved or new row `from_week: N` (first week it applies) and, for a move, `before: "<old team>"`, so earlier weeks keep their old line-ups in the fantasy app. Mirror it in the fantasy repo's `players.json` (team, plus pos/price for new players), sync squads to the dashboard, commit with `[skip render]`. |
| "Make a video of the team change" | `transfers.mjs --spec changes.json` (+ `--whatsapp`): ~5s "Squad changes" story video and a feed card in `league/graphics/` ([video-and-graphics.md](references/video-and-graphics.md)) |
| "Show the table" | `league.mjs status` |

## Rules

- `league/data/*.json` is the source of truth; the dashboard mirrors it. Never
  hand-edit standings: they are always computed.
- Table order: points, then goal difference, then goals scored, then name (same
  as the dashboard). Own goals count for the team, not for any player's
  scoring. An assist is credited to the team the goal counted for.
- Team names keep their transliteration marks (An-Nāṣirūn, Al-Fāʾizūn,
  Al-Mufliḥūn, As-Sābiqūn) in data. Templates only swap ʾ for ’ when drawing.
  Arabic names are written **without harakat** everywhere: vowel marks spill
  onto neighbouring text.
- The house style (cream, ink, crimson, Barlow Condensed, Amiri, the bismillah, the four crest
  shapes, a very faint field of tiny Darul Uloom logos behind everything) comes from the user's dashboard and logo. Keep new graphics in it. Colours live in
  `league.json → brand`.
- Commit outputs every week; this repo is the archive.
- Talking points (user's instruction, from Week 2 on): show only **the gameweek's top
  scorer**, the player with the most goals that week. Never call it a "hat-trick" when the
  goals came across different matches: a hat-trick means 3+ goals in **one** match.
  (`lib.mjs` and `templates/weekly.html` follow this; the Week 1 video predates it.)
