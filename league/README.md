# Darul Uloom Football League: data and weekly outputs

This folder is the league's archive. It's maintained by the
[`higgsfield-football-league`](../higgsfield-football-league/SKILL.md) skill.

| Path | What |
|---|---|
| `league.json` | Teams (with Arabic names and crest shapes), points rules, brand colours, the dashboard artifact link |
| `assets/logo.jpg` | The Darul Uloom logo, used as a faint background pattern in every video and graphic |
| `data/squads.json` | One row per player: `{player, team}` |
| `data/matches.json` | One row per match: `{match, week, date, home, away, home_goals, away_goals}` |
| `data/goals.json` | One row per goal: `{match, team, scorer, assist, own_goal}` |
| `weeks/week-NN/` | That week's `snapshot.json`, recap video `week-NN-story.mp4` and `cards/*.png` |
| `graphics/` | Fixtures posters and announcements |
| `fixtures/` | Weekly fixture list PDFs (`week-NN-fixtures.pdf`) and the fixtures as data |

**Weekly:** send the results to Claude. It saves them, renders the video and
graphics, syncs the [Darul Uloom Football League dashboard](https://claude.ai/artifact/X3aSihZoh87zLQ57WvfycH)
and commits everything here.

**By hand:** edit `data/*.json` on GitHub and commit. The *Football weekly render*
Action checks the data, renders the latest week and commits the outputs back.

Standings, top scorers and top assists are never stored by hand. They're
always computed from these three files, by the same rules as the dashboard.
