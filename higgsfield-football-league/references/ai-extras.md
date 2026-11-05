# Optional AI extras (Higgsfield)

The recap video and graphics are complete without AI. These extras add mood
on top. Keep two rules:

1. **No numbers, names or text from a model.** Scores, tables and names come
   only from the templates. Prompts below ask for no text. Discard any output
   that has lettering in it.
2. **No real people's likeness** unless the user supplies the photos and asks
   for it. Keep figures anonymous, in silhouette or from behind.

All generation goes through the `higgsfield` CLI (`higgsfield auth login`
first). Never call the API with curl. Pick models from the live catalog with
`higgsfield model list`. Don't hard-code model names from memory.

## AI intro clip → `render.mjs --intro`

A 3–5s establishing shot in front of the recap.

```bash
higgsfield model list                       # choose a text-to-video model
higgsfield generate create <video_model> \
  --prompt "Cinematic slow push-in on an empty five-a-side football pitch at dusk, floodlights flickering on, warm cream and deep crimson colour grade, light mist, a single ball on the centre spot, no people, no text, no logos" \
  --aspect-ratio 9:16 --wait --json
```

Download the result URL to the scratchpad, then:

```bash
node higgsfield-football-league/scripts/render.mjs --intro /path/to/intro.mp4
```

Keep one good intro and reuse it every week. Save it as `league/assets/intro.mp4`
and commit it, so the series looks consistent and costs nothing more.

## Hype poster background → composite under a graphic

For a cup final or derby, generate a textured background, then lay the real
fixture graphic over it yourself (e.g. ffmpeg `overlay`). The model's image never
carries the text.

```bash
higgsfield generate create <image_model> \
  --prompt "Dramatic football stadium tunnel, crimson and cream light, geometric Islamic star pattern subtly embossed on the walls, shallow depth of field, empty, no text, no people" \
  --aspect-ratio 4:5 --wait --json
```

## Team crest concepts

If the user wants new crests, generate concept art for inspiration only. Then
redraw the chosen idea as an SVG shape in `templates/common.js → SHAPES` so it stays
crisp and keeps the Arabic band. Never ship a raster AI crest.

## Cost and confirmation

Generation spends Higgsfield credits. Ask the user before generating, and
quote the cost when the CLI offers one (`higgsfield generate cost …`). The
weekly flow never generates anything by default.
