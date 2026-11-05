# Weekly input format

`league.mjs add-week <file>` takes one JSON file per week:

```json
{
  "week": 3,
  "date": "2026-11-22",
  "matches": [
    {
      "home": "An Nasirun", "away": "Al Faizun", "score": "3-1",
      "goals": [
        { "team": "An Nasirun", "scorer": "Asjad", "assist": "Umar" },
        { "team": "An Nasirun", "scorer": "Asjad" },
        { "team": "An Nasirun", "scorer": "Ahmed Lorgat", "assist": "Hamza Lakota" },
        { "team": "Al Faizun",  "scorer": "AbuBakar", "assist": "Adam" }
      ]
    },
    {
      "home": "Al Muflihun", "away": "As Sabiqun", "home_goals": 1, "away_goals": 1,
      "date": "2026-11-23",
      "goals": [
        { "team": "Al Muflihun", "scorer": "Ilyaas" },
        { "team": "As Sabiqun", "scorer": "Haitham", "own_goal": true }
      ]
    }
  ]
}
```

| Field | Rules |
|---|---|
| `week` | Optional. Defaults to the last saved week + 1. |
| `date` | `YYYY-MM-DD`. Week-level default; a match can override it with its own `date`. |
| `home`, `away` | Any spelling that folds to a team: diacritics, hyphens, case and ʾ are ignored. The 3-letter `short` code from `league.json` works too. |
| `score` or `home_goals`/`away_goals` | `"3-1"`, `"3–1"`, `"3:1"`, or two numbers. Home first. |
| `goals[].team` | The team the goal **counted for**. |
| `goals[].scorer` | Must be in that team's squad. For an own goal, the scorer is from the **other** team. |
| `goals[].assist` | Optional, same squad as `team`. Leave it out when unknown. |
| `goals[].own_goal` | `true` for own goals. These count in the table but not for any player. |
| `goals` | Optional. If you leave it out, the table updates but the scorer and assist races don't, and a warning prints. If present, the counts must match the score. |

Player names resolve within the squad by exact folded match, then by a unique
prefix ("Hamza L" → Hamza Lakota). A name that's ambiguous or unknown is an
error with suggestions: ask the user, don't guess.

## Reading the user's message

Users write results loosely. Typical shapes and how to read them:

```
Week 3
Nasirun 3 - 1 Faizun
Asjad 2 (1 assist Umar), Lorgat (Hamza L) | AbuBakar (Adam)
Muflihun 1-1 Sabiqun — Ilyaas; OG Haitham
```

- `X 2` or `X x2` or `X (2)` = two goals for X. An assist in brackets applies to one goal.
  If they write "Asjad 2 (Umar)", ask whether Umar assisted one goal or both,
  unless they said.
- `|` or a new line usually separates home scorers from away scorers. If it's
  not clear, use the squad: each player belongs to exactly one team.
- `OG`/`o.g.`: an own goal. The named player is from the side that conceded.
- "no assists" / nothing in brackets: omit `assist`.
- A bare date like "Sat" or "22/11": convert to `YYYY-MM-DD` (UK day/month order),
  using the current year and the nearest past date.

## Corrections and special cases

- **Correcting a saved week**: rebuild that week's whole JSON and run
  `add-week --replace` with the same `week`. Match ids for that week are
  reassigned, so re-render that week and every later week, then sync.
- **Postponed or abandoned match**: leave it out. Add it in the week it's
  actually played.
- **Guest or new player**: confirm with the user, then `--add-players` (adds
  them to `squads.json` under the team they scored for). Sync squads to the dashboard too.
- **Walkover**: record the agreed score (e.g. `"3-0"`) with no `goals`.
- **Two matches between the same teams in one week**: fine. Each match gets its own id.
