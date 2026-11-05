# Syncing the Football League dashboard

The user's **Darul Uloom Football League** dashboard is a Claude artifact (Dashboard type).
Its slug and URL are in `league/league.json → artifact`:

- slug `f34e41f1-25cf-4da0-853c-23c3639069be`
- https://claude.ai/artifact/X3aSihZoh87zLQ57WvfycH

It has three attached-file datasets. Its page computes the league table, top
scorers, top assists and goals conceded **from those files**, with the same
rules as `scripts/lib.mjs`. Syncing therefore just means replacing the files.

| Dataset doc | File | Repo file |
|---|---|---|
| `datasets/matches` | `matches.json` | `league/data/matches.json` |
| `datasets/goals` | `goals.json` | `league/data/goals.json` |
| `datasets/squads` | `squads.json` | `league/data/squads.json` |

The repo's files use the same columns as the dashboard. `matches.json` has one
extra column, `week`, which the dashboard ignores.

These steps use the claude-artifacts MCP tools (`upload_asset`, `db_get`,
`db_write`). Load them with ToolSearch if they're deferred. If they aren't
available in this session, say so: the data is still saved in the repo, and
the dashboard can be synced next time from a session with them.

## Repo → dashboard (every week)

1. `upload_asset` with `slug` and one file per changed dataset:
   `{name: "matches.json", path: "<abs>/league/data/matches.json"}`, same for
   `goals.json` (and `squads.json` if players changed). Keep each returned
   `url` (`/_blob/<id>`).
2. For each dataset, `db_get` `datasets/<id>` to get its current `version`.
3. `db_write`, one `update` op per dataset, with `ifVersion` from step 2:
   ```json
   {"op": "update", "path": "datasets/matches", "ifVersion": 1, "data": {
     "source": {"kind": "file", "url": "/_blob/<id>", "name": "matches.json"},
     "updated": {"at": "<UTC ISO now>", "by": "Ziyaad (via Claude)"},
     "edit": {"via": "claude", "at": "<UTC ISO now>"}
   }}
   ```
4. Check: `db_get` `data/users/<id from db_whoami>/check`. Re-read while it says
   `checking` (5 reads max). If it's `failed`, read what it names. A missing column
   means the JSON shape changed, so fix the repo file, not the page.
5. Don't change `files/index.html` unless the user asked for a page change.

Don't paste numbers into the page or the dataset docs. The dashboard always
computes from the files.

## Dashboard → repo (when they entered results on the dashboard)

1. `db_list` collection `datasets`. Take each source's `url` (`/_blob/<id>`).
2. `read_asset` with id `<id>` for matches, goals (and squads). Save each one to
   the scratchpad as JSON.
3. Import, which keeps known weeks and numbers new dates as new weeks:
   ```bash
   node higgsfield-football-league/scripts/league.mjs import am.json ag.json [as.json]
   ```
4. Check the printed week numbering with the user if a "week" spanned two
   dates. Fix it with `add-week --replace` if needed.
5. Render, push the data back up (above) so the dashboard gets the `week`
   column, and commit.

## The position-by-week chart

The dashboard's *Position by week* card is a `dash.calc('positions')` over `squads` and `matches`: it replays the table after each week, by the same rules. It uses the `week` column when present, and otherwise numbers the match dates in order. Syncing `matches.json` from the repo (which carries `week`) keeps it exact when a week spans two dates.

## Adding things to the dashboard

Before adding anything else, read the dashboard type's own instructions first
(`read_file` `SKILL.md` on the artifact). The page opens with
`<meta name="dash-one-writer">`, so also read
`artifact-type/reference/one-writer.md` before editing `files/index.html`.
Compute the chart's numbers with a `dash.calc` over the `matches` dataset (it
now carries `week`). Never hard-code values.
