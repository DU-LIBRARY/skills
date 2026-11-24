import json, os, re, sys, shutil
R = '/home/user/skills/presentation/identity'; S = '/tmp/claude-0/-home-user-skills/b7070a4f-d2e5-5468-aac7-8aa9227121ce/scratchpad/identity'
IMG = {'playbill': S + '/callig-light.png', 'workshop': S + '/new/callig-green.png', 'mosaic': S + '/new/callig-green.png', 'zine': S + '/new/callig-blue.png'}
for d, img in IMG.items():
    out = f'{os.getcwd()}/{d}'; shutil.rmtree(out, ignore_errors=True); shutil.copytree(f'{R}/{d}/project', f'{out}/project')
    deck = json.load(open(f'{out}/project/deck.json')); css = open(f'{out}/project/deck.css').read()
    links = ''.join(f'<link rel="stylesheet" href="{f["href"]}">' for f in deck['faces'].values())
    for sid in deck['order']:
        sec = open(f'{out}/project/slides/{sid}.html').read()
        sec = re.sub(r'/_blob/[0-9a-f]+', 'file://' + img, sec)
        open(f'{out}/prev-{sid}.html', 'w').write(f'<!DOCTYPE html><html><head><meta charset="utf-8">{links}<style>body{{margin:0}}section{{position:relative;display:block;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}}aside{{display:none}}*{{animation:none!important;transition:none!important}}{css}</style></head><body>{sec}</body></html>')
    print(d, len(deck['order']))
