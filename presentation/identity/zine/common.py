import json, html, datetime, os
exec(open('content.py', encoding='utf-8').read())
E = lambda t: html.escape(t, quote=False)
AR = '٠١٢٣٤٥٦٧٨٩'
def write_deck(outdir, title, slides, css, faces, sections, img_map, preview_dir):
    os.makedirs(f'{outdir}/project/slides', exist_ok=True); os.makedirs(preview_dir, exist_ok=True)
    for sid in ORDER:
        body, cls = slides[sid]
        sec = f'<section id="{sid}" class="{cls}" data-transition="fade">\n{body}\n<aside>{E(NOTES[sid])}</aside>\n</section>\n'
        art = sec
        for k, (blob, local) in img_map.items(): art = art.replace('{{' + k + '}}', blob)
        open(f'{outdir}/project/slides/{sid}.html', 'w', encoding='utf-8').write(art)
        prev = sec
        for k, (blob, local) in img_map.items(): prev = prev.replace('{{' + k + '}}', local)
        links = ''.join(f'<link rel="stylesheet" href="{f["href"]}">' for f in faces.values())
        open(f'{preview_dir}/prev-{sid}.html', 'w', encoding='utf-8').write(f'<!DOCTYPE html><html><head><meta charset="utf-8">{links}<style>body{{margin:0}}section{{position:relative;display:block;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}}aside{{display:none}}*{{animation:none!important}}{css}</style></head><body>{prev}</body></html>')
    open(f'{outdir}/project/deck.css', 'w', encoding='utf-8').write(css)
    deck = {"v": 5, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}, "lists": "css",
            "format": {"v": 1, "shared": ["project/deck.css"]}, "title": title, "cover": "cover", "order": ORDER, "sections": sections, "faces": faces, "designSystems": []}
    json.dump(deck, open(f'{outdir}/project/deck.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(ORDER, open(f'{preview_dir}/order.json', 'w'))
SECTIONS = {"s1": {"description": "Opening: who are we, and where do we come from?", "start": "cover"},
            "s2": {"description": "The six qualities, with the stories behind them.", "start": "faith"},
            "s3": {"description": "Heritage, the six together, and a final thought.", "start": "chapter"}}
