import json, os, html, datetime
D = '/tmp/claude-0/-home-user-skills/b7070a4f-d2e5-5468-aac7-8aa9227121ce/scratchpad/part1/deck'
BLOB = {'LOGOG': ('/_blob/6a31a50d68b4f7e4d58ebb356511db3c', D + '/logo-green-c.png'),
        'LOGOY': ('/_blob/35a6b3f06228f3ff2da00582f721cf23', D + '/logo-gold-c.png'),
        'CALY': ('/_blob/8a274f387e726b42b354c33eb97f2d1b', D + '/callig-gold.png')}
FACES = {
 "eb-garamond": {"family": "EB Garamond", "href": "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap"},
 "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"},
 "cormorant-garamond": {"family": "Cormorant Garamond", "href": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&display=swap"},
 "manrope": {"family": "Manrope", "href": "https://fonts.googleapis.com/css2?family=Manrope:wght@700&display=swap"}}
CSS = """/* ==== Letterpress on cream paper, in the Institute's green and gold ==== */
:root { --paper: #EDE6D6; --ink: #1C1E24; --soft: #343843; --mute: #5E6170; --acc: #17433A; --gold: #A8823A; --gold-l: #E3C37E; --on: #DCE6E0; --rule: #B4AE9E; }
body { font-family: 'EB Garamond', 'Amiri', Georgia, serif; color: var(--ink); }
section { background: var(--paper); color: var(--ink); padding: 128px; font-family: 'EB Garamond', 'Amiri', Georgia, serif; }
section p, section h1, section h2 { margin: 0; }

/* ==== Page furniture ==== */
.grain { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; opacity: 0.3; }
.frame-o { position: absolute; left: 56px; top: 56px; width: 1808px; height: 968px; box-sizing: border-box; border: 5px solid var(--ink); }
.frame-i { position: absolute; left: 70px; top: 70px; width: 1780px; height: 940px; box-sizing: border-box; border: 2px solid var(--ink); }
.corner { position: absolute; width: 34px; height: 34px; }
.c1 { left: 41px; top: 41px; } .c2 { left: 1845px; top: 41px; } .c3 { left: 41px; top: 1005px; } .c4 { left: 1845px; top: 1005px; }
.hd-logo { position: absolute; left: 146px; top: 82px; width: 130px; height: 119px; }
.rh-l { position: absolute; left: 300px; top: 126px; width: 800px; font-size: 24px; letter-spacing: 4px; color: var(--acc); }
.rh-r { position: absolute; left: 1170px; top: 126px; width: 600px; text-align: right; font-size: 24px; letter-spacing: 4px; color: var(--mute); }
.folio { position: absolute; left: 860px; top: 950px; width: 200px; display: flex; justify-content: center; align-items: center; gap: 16px; }
.num { font-size: 26px; color: var(--mute); }

/* ==== Shared type ==== */
.kick { font-size: 24px; letter-spacing: 4px; color: var(--acc); margin-bottom: 16px; }
h2 { font-size: 76px; font-weight: 500; line-height: 1.08; color: var(--ink); }
h2 i { color: var(--acc); }
.lead { font-size: 36px; font-style: italic; line-height: 1.35; color: var(--soft); margin-top: 22px; }
.ar { font-family: 'Amiri', serif; direction: rtl; }
.ref { font-size: 24px; letter-spacing: 4px; color: var(--gold); margin-top: 18px; }
.band { position: absolute; left: 84px; top: 770px; width: 1752px; height: 150px; background: var(--acc); display: flex; align-items: center; justify-content: center; }
.band-t { font-size: 48px; color: var(--paper); text-align: center; }
.band-t i { color: var(--gold-l); }
.orn { display: flex; justify-content: center; align-items: center; gap: 22px; margin: 22px 0; }
.orn-r { width: 240px; height: 6px; border-top: 2px solid var(--ink); border-bottom: 2px solid var(--ink); }

/* ==== Three columns ==== */
.trio { position: absolute; left: 150px; width: 1620px; display: grid; grid-template-columns: 1fr 1fr 1fr; }
.cell { padding: 0 44px; text-align: center; border-left: 2px solid var(--rule); }
.cell.first { border-left: none; }
.who { font-size: 24px; letter-spacing: 4px; color: var(--acc); }
.cell-tx { font-size: 46px; line-height: 1.25; color: var(--ink); margin-top: 14px; }
.cell-tx i { color: var(--acc); }
.cen { position: absolute; left: 150px; width: 1620px; text-align: center; }

/* ==== Opening ==== */
.op-top { top: 200px; }
.op-trio { top: 500px; }

/* ==== The ayah, on its own ==== */
.ay { position: absolute; left: 210px; top: 190px; width: 1500px; height: 740px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
.ay-ar { width: 1500px; text-align: center; font-size: 92px; line-height: 1.85; color: var(--acc); }
.ay-tr { width: 1300px; font-size: 46px; font-style: italic; line-height: 1.35; color: var(--soft); }

/* ==== Youth ==== */
.yo-top { top: 190px; }
.yo-ar { font-size: 84px; line-height: 1.9; color: var(--acc); }
.yo-tr { font-size: 40px; font-style: italic; color: var(--soft); }
.yo-tr b { font-weight: 500; color: var(--acc); }
.yo-trio { top: 590px; }

/* ==== Education ==== */
.ed-left { position: absolute; left: 150px; top: 250px; width: 1040px; }
.vs { margin-top: 70px; display: grid; grid-template-columns: 1fr 1fr; }
.vs-c { padding: 0 40px 0 0; }
.vs-c.two { padding: 0 0 0 40px; border-left: 2px solid var(--rule); }
.vs-h { font-size: 24px; letter-spacing: 4px; color: var(--mute); margin-bottom: 18px; }
.vs-c.two .vs-h { color: var(--acc); }
.vs-l { font-size: 46px; line-height: 1.6; color: var(--mute); }
.vs-c.two .vs-l { color: var(--ink); }
.pill { position: absolute; left: 1240px; top: 84px; width: 596px; height: 912px; background: var(--acc); }
.pill-in { position: absolute; left: 1300px; top: 230px; width: 480px; }
.pill-k { font-size: 24px; letter-spacing: 4px; color: var(--gold-l); }
.big6 { font-size: 300px; font-weight: 500; line-height: 0.9; color: var(--gold-l); margin-top: 20px; }
.pill-t { font-size: 56px; line-height: 1.1; color: var(--paper); margin-top: 24px; }
.pill-s { font-size: 32px; font-style: italic; line-height: 1.35; color: var(--on); margin-top: 22px; }
.ed-rh { position: absolute; left: 1300px; top: 126px; width: 480px; text-align: right; font-size: 24px; letter-spacing: 4px; color: var(--gold-l); }
section.education .folio { left: 595px; }

/* ==== Six pillars: a ruled letterpress grid ==== */
.pl-head { position: absolute; left: 150px; top: 216px; width: 1620px; }
.pl-lead { font-size: 34px; font-style: italic; color: var(--soft); margin-top: 10px; }
.tiles { position: absolute; left: 150px; top: 440px; width: 1620px; display: grid; grid-template-columns: 1fr 1fr 1fr; border-top: 2px solid var(--ink); border-bottom: 2px solid var(--ink); }
.tile { position: relative; padding: 18px 40px 22px; box-sizing: border-box; border-left: 2px solid var(--rule); display: flex; flex-direction: column; align-items: center; text-align: center; }
.tile:nth-child(3n+1) { border-left: none; }
.tile:nth-child(n+4) { border-top: 2px solid var(--rule); }
.t-num { font-size: 30px; font-weight: 500; letter-spacing: 4px; color: var(--gold); }
.t-ar { font-size: 72px; font-weight: 700; line-height: 1.5; color: var(--acc); text-align: center; }
.t-en { font-size: 24px; letter-spacing: 4px; color: var(--ink); margin-top: 16px; }

/* ==== Cover ==== */
section.cover { background: #17433A; }
.cv-frame { position: absolute; left: 56px; top: 56px; width: 1808px; height: 968px; box-sizing: border-box; border: 2px solid #C9A85F; }
.cv-logo { position: absolute; left: 130px; top: 120px; width: 170px; height: 155px; }
.cv-ttl { position: absolute; left: 140px; top: 330px; width: 1600px; font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 176px; line-height: 1; letter-spacing: -1.5px; color: #F3EDE0; }
.cv-base { position: absolute; left: 130px; top: 838px; width: 1660px; height: 2px; background: #C9A85F; }
.cv-cal { position: absolute; left: 140px; top: 870px; width: 440px; height: 84px; }
.cv-slo { position: absolute; left: 1100px; top: 902px; width: 690px; text-align: right; font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 7px; color: #D4B26A; }

/* ==== Motion: three quick steps ==== */
.d1, .d2, .d3 { animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) both; }
.d2 { animation-delay: 0.2s; }
.d3 { animation-delay: 0.4s; }
@keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0px); } }
"""
GRAIN = '<svg class="grain" aria-label="" width="1920" height="1080" viewBox="0 0 1920 1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.3  0 0 0 0 0.3  0 0 0 0.5 0"/></filter><rect width="1920" height="1080" filter="url(#n)"/></svg>'
ROS = '<svg aria-label="" width="34" height="34" viewBox="-50 -50 100 100"><rect x="-50" y="-50" width="100" height="100" fill="#EDE6D6"/><g fill="#17433A"><rect x="-30" y="-30" width="60" height="60"/><rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/></g><circle r="11" fill="#E3C37E"/></svg>'
SM = '<svg aria-label="" width="22" height="22" viewBox="-50 -50 100 100"><g fill="#17433A"><rect x="-30" y="-30" width="60" height="60"/><rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/></g></svg>'
def furn(n, right, rh=True):
    s = GRAIN + '<div class="frame-o"></div><div class="frame-i"></div>' + ''.join(f'<div class="corner c{i}">{ROS}</div>' for i in (1, 2, 3, 4))
    s += '<img class="hd-logo" src="{{LOGOG}}" alt="Imam Muhammad Adam Institute logo">'
    s += '<p class="rh-l">The Imam Muhammad Adam Institute</p>'
    if rh: s += f'<p class="rh-r">{right}</p>'
    s += f'<div class="folio">{SM}<p class="num">{n}</p>{SM}</div>'
    return s

AYAH = 'وَمَنْ أَحْسَنُ قَوْلًا مِّمَّن دَعَآ إِلَى ٱللَّهِ وَعَمِلَ صَٰلِحًا وَقَالَ إِنَّنِى مِنَ ٱلْمُسْلِمِينَ'
HAD = 'اغْتَنِمْ خَمْسًا قَبْلَ خَمْسٍ: شَبَابَكَ قَبْلَ هَرَمِكَ'
SL = {}
SL['cover'] = ('cover', '''<div class="cv-frame"></div>
<img class="cv-logo d1" src="{{LOGOY}}" alt="Imam Muhammad Adam Institute logo">
<h1 class="cv-ttl d2">Our Identity<br>as Young Muslims</h1>
<div class="cv-base"></div>
<img class="cv-cal d3" src="{{CALY}}" alt="Maʿhad al-Imām Muḥammad Ādam al-Islāmī">
<p class="cv-slo d3">A TRADITION OF EXCELLENCE</p>''',
 "As-salāmu ʿalaykum wa raḥmatullāhi wa barakātuh.\n\nA very warm welcome to our respected teachers, honoured guests and fellow students. It is a pleasure to have you all with us today.")
SL['opening'] = ('paper', furn(2, 'Opening') + '''
<div class="cen op-top d1"><p class="kick">OPENING</p><h2>Who are we, and who should <i>we become</i>?</h2>
<p class="lead">A warm welcome to our respected teachers, honoured guests and fellow students.</p></div>
<div class="trio op-trio d2">
<div class="cell first"><p class="who">WHO</p><p class="cell-tx">Who are we as <i>young Muslims</i>?</p></div>
<div class="cell"><p class="who">WHAT</p><p class="cell-tx">What <i>values</i> should define us?</p></div>
<div class="cell"><p class="who">WHO NEXT</p><p class="cell-tx">Who should we <i>aspire</i> to become?</p></div>
</div>
<div class="band d3"><p class="band-t">A question at the heart of our education <i>and our future</i></p></div>''',
 "Today, I invite you to reflect with us on a question that lies at the heart of our education and our future: Who are we as young Muslims, what values should define us, and what kind of individuals should we aspire to become?")
SL['ayah'] = ('paper', furn(3, 'Opening · The Qurʾān') + f'''
<div class="ay">
<p class="kick d1">ALLAH TAʿĀLĀ SAYS</p>
<p class="ar ay-ar d1">{AYAH}</p>
<div class="orn d2"><div class="orn-r"></div>{SM}<div class="orn-r"></div></div>
<p class="ay-tr d2">“And who is better in speech than one who calls towards Allah, does righteous deeds, and says: Indeed, I am among the Muslims?”</p>
<p class="ref d3">SŪRAT FUṢṢILAT 41:33</p>
</div>''',
 "Allah Taʿālā tells us in the Noble Qurʾān: “And who is better in speech than one who calls towards Allah, does righteous deeds, and says: Indeed, I am among the Muslims?” (Sūrat Fuṣṣilat, 41:33)\n\nThis āyah beautifully captures the essence of what it means to be a Muslim. Our identity is not defined merely by our names, the clothes we wear, or the families we come from. It is rooted in our faith, reflected in our character, and demonstrated through our actions. It means living by the teachings of Islam, inviting others towards goodness with wisdom, and confidently embracing who we are as Muslims.\n\nOur faith should shape not only what we believe, but also how we think, how we behave, how we treat others, and the contributions we make to the world around us. Islam is not simply an identity we inherit, but a responsibility we must strive to live up to.\n\nSo, what does this mean for us as young Muslims today? What kind of individuals should we aspire to become, and how can we carry forward the remarkable legacy of those who came before us?")
SL['youth'] = ('paper', furn(4, 'The value of our youth') + f'''
<div class="cen yo-top d1"><p class="kick">THE VALUE OF OUR YOUTH</p>
<p class="ar yo-ar">{HAD}</p>
<p class="yo-tr">“Take advantage of five things before five: your <b>youth</b> before your old age.”</p>
<p class="ref">REPORTED BY AL-ḤĀKIM AND AL-BAYHAQĪ</p></div>
<div class="trio yo-trio d2">
<div class="cell first"><p class="who">A TIME OF</p><p class="cell-tx"><i>Opportunity</i></p></div>
<div class="cell"><p class="who">A TIME OF</p><p class="cell-tx"><i>Growth</i></p></div>
<div class="cell"><p class="who">A TIME OF</p><p class="cell-tx"><i>Responsibility</i></p></div>
</div>
<div class="band d3"><p class="band-t">The choices we make today <i>shape who we become tomorrow</i></p></div>''',
 "The Value of Our Youth\n\nThe Prophet Muhammad ﷺ gave us an important reminder about making the most of our youth: “Take advantage of five things before five: your youth before your old age.” (Reported by al-Ḥākim and al-Bayhaqī.)\n\nYouth is a precious blessing from Allah, a time of opportunity, growth and responsibility. The choices we make today will shape the individuals we become tomorrow.")
PILLARS = [('الإيمان','STRONG IN FAITH','t-green'),('العلم','SEEKERS OF KNOWLEDGE','t-lapis'),('الأخلاق','NOBLE IN CHARACTER','t-clay'),
           ('المجتمع','CONFIDENT IN SOCIETY','t-teal'),('الخدمة','COMMITTED TO SERVICE','t-olive'),('الإحسان','STRIVING FOR EXCELLENCE','t-gold')]
tiles = ''.join(f'<div class="tile {c}"><p class="t-num">{i+1}</p><p class="ar t-ar">{ar}</p><p class="t-en">{en}</p></div>' for i,(ar,en,c) in enumerate(PILLARS))
SL['pillars'] = ('paper', furn(5, 'Six pillars') + f'''
<div class="pl-head d1"><p class="kick">SO, WHAT KIND OF YOUNG MUSLIMS?</p><h2>Six foundational <i>pillars</i></h2>
<p class="pl-lead">to help us answer this question, and shape the identity we strive to embody</p></div>
<div class="tiles d2">{tiles}</div>''',
 "So, what kind of young Muslims should we aspire to become? Six foundational pillars will help us answer this question and shape the identity we strive to embody.\n\n1. Strong in Faith (al-Īmān)\n2. Seekers of Knowledge (al-ʿIlm)\n3. Noble in Character (al-Akhlāq)\n4. Confident in Society (al-Mujtamaʿ)\n5. Committed to Service (al-Khidmah)\n6. Striving for Excellence (al-Iḥsān)")
ORDER = list(SL)
os.makedirs('project/slides', exist_ok=True); os.makedirs('prev', exist_ok=True)
links = ''.join(f'<link rel="stylesheet" href="{f["href"]}">' for f in FACES.values())
for sid, (cls, body, notes) in SL.items():
    assert len(notes) <= 4000
    sec = f'<section id="{sid}" class="{cls}" data-transition="fade">\n{body}\n<aside>{html.escape(notes, quote=False)}</aside>\n</section>\n'
    a, p = sec, sec
    for k, (blob, loc) in BLOB.items(): a = a.replace('{{' + k + '}}', blob); p = p.replace('{{' + k + '}}', 'file://' + loc)
    open(f'project/slides/{sid}.html', 'w').write(a)
    open(f'prev/{sid}.html', 'w').write(f'<!DOCTYPE html><html><head><meta charset="utf-8">{links}<style>body{{margin:0}}section{{position:relative;display:block;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}}aside{{display:none}}*{{animation:none!important}}{CSS}</style></head><body>{p}</body></html>')
open('project/deck.css', 'w').write(CSS)
deck = {"v": 5, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}, "lists": "css",
        "format": {"v": 1, "shared": ["project/deck.css"]}, "title": "Our Identity as Young Muslims — Part 1", "cover": "cover", "order": ORDER,
        "sections": {"s1": {"description": "Welcome and the question: who are we as young Muslims?", "start": "cover"},
                     "s2": {"description": "The Qurʾān and the value of youth, leading into the six pillars.", "start": "ayah"}},
        "faces": FACES, "designSystems": []}
json.dump(deck, open('project/deck.json', 'w'), ensure_ascii=False, indent=1)
print(ORDER)
