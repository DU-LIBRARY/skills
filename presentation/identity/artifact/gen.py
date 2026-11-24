import json, re, html, datetime, sys
IMG = json.load(open('images.json'))          # {"logo": src, "callig": src, "calligL": src}
md = open('/home/user/skills/presentation/identity/script.md', encoding='utf-8').read()
secs = re.findall(r'^## (\d+)\. .*?\n(.*?)(?=^## |\Z)', md, re.S | re.M)
NOTES = {int(n): re.sub(r'\*\*', '', b).strip() for n, b in secs}
PAPER, GREEN, GOLD, GOLDL = '#F2EBDC', '#17433A', '#B8913F', '#E2C478'
E = lambda t: html.escape(t, quote=False)
def star(size, fill, hole, back=None):
    bg = f'<rect x="-50" y="-50" width="100" height="100" fill="{back}"/>' if back else ''
    return (f'<svg aria-label="" width="{size}" height="{size}" viewBox="-50 -50 100 100">{bg}<g fill="{fill}"><rect x="-30" y="-30" width="60" height="60"/>'
            f'<rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/></g><circle r="11" fill="{hole}"/></svg>')
GRAIN = ('<svg class="grain" aria-label="" width="1920" height="1080" viewBox="0 0 1920 1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 0.4  0 0 0 0 0.35  0 0 0 0 0.2  0 0 0 0.45 0"/></filter><rect width="1920" height="1080" filter="url(#n)"/></svg>')
C = star(34, GOLD, PAPER, PAPER)
FRAME = '<div class="frame-o"></div><div class="frame-i"></div>' + ''.join(f'<div class="corner c{i}">{C}</div>' for i in range(1, 5))
AR = '٠١٢٣٤٥٦٧٨٩'
def chrome(right, n):
    s = star(22, GOLD, PAPER)
    return f'<div class="rh"><p class="rh-l">Our Identity as Young Muslims</p><p class="rh-r">{right}</p></div><div class="folio">{s}<p class="num">{n}</p>{s}</div>'
def slide(id_, cls, body, notes, pre=''):
    return f'<section id="{id_}" class="{cls}" data-transition="fade">\n{GRAIN}\n{pre}{FRAME}\n{body}\n<aside>{E(notes)}</aside>\n</section>\n'
S = {}
ORN = lambda n=None: (f'<div class="orn"><div class="orn-r"></div>{star(22, GOLD, PAPER)}' + (f'<p class="orn-n">{AR[n]}</p>{star(22, GOLD, PAPER)}' if n else '') + '<div class="orn-r"></div></div>')
SEP = star(20, GOLD, PAPER)
S['cover'] = slide('cover', 'paper cover', f"""<img class="cv-callig d1" src="{IMG['callig']}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:960px;height:206px">
<div class="cv-orn d2"><div class="cv-rule"></div>{star(28, GOLD, PAPER)}<div class="cv-rule"></div></div>
<h1 class="cv-title d2">Our Identity as Young Muslims</h1>
<p class="cv-sub d2">Six qualities that form the foundation of who we are</p>
<img class="cv-logo d3" src="{IMG['logo']}" alt="The Imam Muhammad Adam Institute logo" style="width:150px;height:148px">
<p class="cv-foot d3">MAʿHAD AL-IMĀM MUḤAMMAD ĀDAM AL-ISLĀMĪ · A TRADITION OF EXCELLENCE</p>""", NOTES[1])

verbs = [('Anchor', 'our faith'), ('Pursue', 'knowledge'), ('Build', 'character'), ('Prepare', 'to serve')]
vb = SEP.join(f'<div class="vb"><p class="vb-v">{v}</p><p class="vb-o">{o}</p></div>' for v, o in verbs)
S['grades'] = slide('grades', 'paper', f"""{chrome('Who are we?', 2)}
<div class="cen d1"><h2 class="disp">More than grades</h2><p class="cen-sub">Our education is about far more than exams, top grades or a good career.</p></div>
<div class="verbs d2">{vb}</div>
<div class="colo d3"><div class="dbl"></div><p class="colo-t">Our aim: Muslims whose faith, intellect and character benefit Britain and humanity.</p><div class="dbl"></div></div>""", NOTES[2])

Q = [
 dict(id='faith', n=1, lay='A', word='الإيمان', title='Strong in Faith', sub='Our Islamic identity',
      lead='Knowing Allah, loving His Messenger ﷺ, and living by His guidance.',
      aims=['Anchor in worship', 'Understand our beliefs', 'Live the Sunnah', 'Stand firm'],
      foot=('', 'Never apologetic about being Muslim.')),
 dict(id='knowledge', n=2, lay='B', word='العلم', title='Seekers of Knowledge', sub='Our scholarly identity',
      ar='اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ', tr='“Read in the name of your Lord Who created.”', ref='SŪRAT AL-ʿALAQ: 1',
      aims=['Love all useful learning', 'Question and reflect', 'Honour our heritage'],
      foot=('ON THEIR SHOULDERS', 'Ibn Sīnā · al-Zahrāwī · al-Khwārizmī · al-Kindī · Ibn al-Haytham · Fāṭimah al-Fihrī')),
 dict(id='character', n=3, lay='A', word='الأخلاق', title='Noble in Character', sub='Our identity of adab and akhlāq',
      ar='وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ', tr='“And indeed, you are upon an outstanding standard of character.”', ref='SŪRAT AL-QALAM: 4',
      aims=['Respect everyone', 'Live with integrity', 'Choose humility', 'Control ourselves'],
      foot=('', 'Grades win applause. Character earns respect.')),
 dict(id='society', n=4, lay='B', word='المجتمع', title='Confident in Society', sub='Our identity as British Muslims',
      lead='Being a committed Muslim and contributing to British life support each other.',
      aims=['Walk with quiet confidence', 'Build bridges', 'Stand up for justice', 'Lead by example'],
      foot=('ON THEIR SHOULDERS', 'The Madīnah covenant · trade routes · paper and libraries · coffee, chess and the miswāk')),
 dict(id='service', n=5, lay='B', word='الخدمة', title='A Life of Service', sub='Our identity of khidmah',
      ar='وَأَحْسِنْ كَمَا أَحْسَنَ اللَّهُ إِلَيْكَ', tr='“And do good as Allah has done good to you.”', ref='SŪRAT AL-QAṢAṢ: 77',
      aims=['Care deeply', 'Serve first', 'Solve real problems', 'Lead by serving'],
      foot=('ON THEIR SHOULDERS', 'Free bīmāristān hospitals · windmills and irrigation · al-Jazarī’s machines')),
 dict(id='excellence', n=6, lay='A', word='الإحسان', title='Striving for Excellence', sub='Our identity of iḥsān',
      ar='إِنَّ اللَّهَ كَتَبَ الْإِحْسَانَ عَلَىٰ كُلِّ شَيْءٍ', tr='“Indeed, Allah has prescribed excellence in all things.”', ref='ṢAḤĪḤ MUSLIM',
      aims=['Give our best', 'Refuse to coast', 'Learn from setbacks', 'Stay grateful'],
      foot=('ON THEIR SHOULDERS', 'The Alhambra · the Süleymaniye · Rūmī · Saʿdī · Ibn Rushd · Ibn Khaldūn')),
]
for i, q in enumerate(Q):
    flab, ftxt = q['foot']
    if q['lay'] == 'A':     # centred title page
        quote = (f'<p class="ar a-ar">{q["ar"]}</p><p class="a-tr">{q["tr"]} <span class="ref-i">{q["ref"].title().replace("Al-", "al-")}</span></p>' if 'ar' in q
                 else f'<p class="a-lead">“{q["lead"]}”</p>')
        aims = SEP.join(f'<p class="aim">{a}</p>' for a in q['aims'])
        foot = f'<p class="a-foot d3">{(flab.title() + ": ") if flab else ""}{ftxt}</p>'
        body = f"""{chrome(q['title'], i + 3)}
<div class="a-col"><div class="d1">{ORN(q['n']).replace('class="orn"', 'class="orn a-orn"')}
<p class="ar a-word">{q['word']}</p>
<h2 class="a-title">{q['title']}</h2></div>
<div class="a-quote d2">{quote}</div></div>
<div class="aims d3"><div class="dbl"></div><div class="aims-row">{aims}</div><div class="dbl"></div></div>
{foot}"""
        S[q['id']] = slide(q['id'], 'paper qa', body, NOTES[i + 3])
    else:                    # split: the word on a green panel
        quote = (f'<p class="ar b-ar">{q["ar"]}</p><p class="b-tr">{q["tr"]}</p><p class="b-ref">{q["ref"]}</p>' if 'ar' in q
                 else f'<p class="b-lead">“{q["lead"]}”</p>')
        aims = ''.join(f'<div class="b-aim"><p class="b-aim-n">{AR[k + 1]}</p><p class="b-aim-t">{a}</p></div>' for k, a in enumerate(q['aims']))
        body = f"""{chrome(q['title'], i + 3)}
<div class="b-panel-in d1"><p class="b-num">{AR[q['n']]}</p><p class="ar b-word">{q['word']}</p><h2 class="b-title">{q['title']}</h2><p class="b-sub">{q['sub']}</p></div>
<div class="b-right"><div class="d2">{quote}</div><div class="b-aims d3">{aims}</div></div>
<div class="b-foot d3"><p class="b-foot-l">{flab}</p><p class="b-foot-t">{ftxt}</p></div>"""
        S[q['id']] = slide(q['id'], 'paper qb', body, NOTES[i + 3], '<div class="b-panel"></div>\n')

rows = [('Proud of our history', 'living in the past'), ('Confident in our beliefs', 'falling into arrogance'), ('Ambitious in our goals', 'forgetting Allah and His creation')]
cp = f'<div class="cp-sep">{SEP}</div>'.join(f'<div class="cp"><p class="cp-a">{a}</p><p class="cp-w">without</p><p class="cp-b">{b}</p></div>' for a, b in rows)
S['heritage'] = slide('heritage', 'paper', f"""{chrome('Our heritage', 9)}
<div class="cen d1"><h2 class="disp">Our Heritage, Our Responsibility</h2><p class="cen-sub">Knowledge and power must be guided by faith, justice and moral responsibility.</p></div>
<div class="couplets d2">{cp}</div>
<div class="colo d3"><div class="dbl"></div><p class="colo-t">True greatness: faith with knowledge, knowledge with character, character with service.</p><div class="dbl"></div></div>""", NOTES[9])

six = [('Strong in Faith', 'الإيمان'), ('Seekers of Knowledge', 'العلم'), ('Noble in Character', 'الأخلاق'),
       ('Confident in Society', 'المجتمع'), ('Committed to Service', 'الخدمة'), ('Striving for Excellence', 'الإحسان')]
toc = ''.join(f'<div class="toc-r"><p class="toc-n">{AR[k + 1]}</p><p class="toc-t">{t}</p><div class="toc-dots"></div><p class="ar toc-ar">{a}</p></div>' for k, (t, a) in enumerate(six))
S['six'] = slide('six', 'paper', f"""{chrome('To carry forward', 10)}
<div class="cen d1"><h2 class="disp">The Six Qualities</h2><p class="cen-sub">to carry forward</p></div>
{ORN().replace('class="orn"', 'class="orn toc-orn d1"')}
<div class="toc d2">{toc}</div>""", NOTES[10])

S['final'] = slide('final', 'paper', f"""{chrome('A final thought', 11)}
{ORN().replace('class="orn"', 'class="orn f-orn d1"')}
<p class="f-quote d1">People may not remember our grades or prizes. They will remember how we treated them.</p>
<p class="f-close d2">Let us be a generation firm in faith, rich in knowledge, noble in character, confident in our identity and devoted to serving others.</p>
<img class="f-callig d3" src="{IMG['callig']}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:700px;height:150px">""", NOTES[11])

order = ['cover', 'grades'] + [q['id'] for q in Q] + ['heritage', 'six', 'final']
for k in order: open(f'project/slides/{k}.html', 'w', encoding='utf-8').write(S[k])
deck = {"v": 5, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
        "lists": "css", "format": {"v": 1, "shared": ["project/deck.css"]}, "title": "Our Identity as Young Muslims", "cover": "cover", "order": order,
        "sections": {"s1": {"description": "Opening: who are we?", "start": "cover"},
                     "s2": {"description": "The six qualities, one by one.", "start": "faith"},
                     "s3": {"description": "Heritage, the six qualities together, and a final thought.", "start": "heritage"}},
        "faces": {"eb-garamond": {"family": "EB Garamond", "href": "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap"},
                  "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"},
                  "im-fell-english": {"family": "IM Fell English", "href": "https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&display=swap"}},
        "designSystems": []}
json.dump(deck, open('project/deck.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(order), {k: len(NOTES[i]) for i, k in enumerate(order, 1)})
