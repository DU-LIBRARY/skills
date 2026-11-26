# Slides 2-5 in the Muttahida Qawmiyyah letterpress language, in the Institute's green.
CSS = """
:root { --paper:#EDE6D6; --ink:#1C1E24; --soft:#343843; --mute:#5E6170; --acc:#17433A; --gold:#A8823A; --gold-l:#E3C37E; --on:#DCE6E0; --rule:#B4AE9E; }
body { margin:0; }
section { position:relative; width:1920px; height:1080px; overflow:hidden; background:var(--paper); color:var(--ink); font-family:'EB Garamond','Amiri',Georgia,serif; }
p, h2, h3 { margin:0; }
.grain { position:absolute; left:0; top:0; width:1920px; height:1080px; background:url(grain.png); background-size:256px 256px; opacity:.55; }
.frame-o { position:absolute; left:56px; top:56px; width:1808px; height:968px; box-sizing:border-box; border:5px solid var(--ink); }
.frame-i { position:absolute; left:70px; top:70px; width:1780px; height:940px; box-sizing:border-box; border:2px solid var(--ink); }
.corner { position:absolute; width:34px; height:34px; }
.c1 { left:41px; top:41px; } .c2 { left:1845px; top:41px; } .c3 { left:41px; top:1005px; } .c4 { left:1845px; top:1005px; }
.rh { position:absolute; left:150px; top:100px; width:1620px; display:flex; justify-content:space-between; }
.rh p { font-size:24px; letter-spacing:4px; } .rh-l { color:var(--acc); } .rh-r { color:var(--mute); }
.folio { position:absolute; left:860px; top:950px; width:200px; display:flex; justify-content:center; align-items:center; gap:16px; }
.num { font-size:26px; color:var(--mute); }
.kick { font-size:24px; letter-spacing:4px; color:var(--acc); margin-bottom:16px; }
h2 { font-size:76px; font-weight:500; line-height:1.08; color:var(--ink); }
h2 i { color:var(--acc); }
.lead { font-size:36px; font-style:italic; line-height:1.35; color:var(--soft); margin-top:22px; }
.ar { font-family:'Amiri',serif; direction:rtl; }
.ref { font-size:24px; letter-spacing:4px; color:var(--gold); }
.band { position:absolute; left:84px; top:770px; width:1752px; height:150px; background:var(--acc); display:flex; align-items:center; justify-content:center; }
.band p { font-size:48px; color:var(--paper); text-align:center; } .band i { color:var(--gold-l); }
/* trio */
.trio { position:absolute; left:150px; display:grid; grid-template-columns:1fr 1fr 1fr; width:1620px; }
.cell { padding:0 44px; text-align:center; border-left:2px solid var(--rule); } .cell.first { border-left:none; }
.who { font-size:24px; letter-spacing:4px; color:var(--acc); }
.cell-tx { font-size:46px; line-height:1.25; color:var(--ink); margin-top:14px; }
.cell-tx i { color:var(--acc); }
/* split with a green panel */
.panel { position:absolute; left:84px; top:84px; width:840px; height:912px; background:var(--acc); }
.panel-in { position:absolute; left:150px; top:270px; width:700px; }
.p-ar { font-size:58px; line-height:2; color:var(--gold-l); text-align:right; }
.p-tr { font-size:34px; font-style:italic; line-height:1.38; color:var(--on); margin-top:18px; }
.p-ref { font-size:24px; letter-spacing:4px; color:var(--gold-l); margin-top:18px; }
.right { position:absolute; left:1010px; top:190px; width:760px; }
.rows { margin-top:40px; }
.row { display:grid; grid-template-columns:300px 1fr; align-items:baseline; padding:20px 0; border-top:2px solid var(--rule); }
.row:last-child { border-bottom:2px solid var(--rule); }
.row-k { font-size:24px; letter-spacing:4px; color:var(--acc); }
.row-v { font-size:44px; color:var(--ink); }
.row-v i { color:var(--acc); }
section.split .rh { left:1010px; width:760px; }
section.split .rh-l { color:var(--gold-l); position:absolute; left:-860px; }
section.split .folio { left:1290px; }
/* centred hadith */
.cen { position:absolute; left:150px; top:170px; width:1620px; text-align:center; }
.h-ar { font-size:84px; line-height:1.9; color:var(--acc); }
.h-tr { font-size:40px; font-style:italic; color:var(--soft); }
.orn { display:flex; justify-content:center; align-items:center; gap:22px; margin:18px 0; }
.orn-r { width:240px; height:6px; border-top:2px solid var(--ink); border-bottom:2px solid var(--ink); }
/* more than grades */
.left { position:absolute; left:150px; top:250px; width:1040px; }
.vs { margin-top:70px; display:grid; grid-template-columns:1fr 1fr; gap:0; }
.vs-c { padding:0 40px 0 0; } .vs-c + .vs-c { padding:0 0 0 40px; border-left:2px solid var(--rule); }
.vs-h { font-size:24px; letter-spacing:4px; color:var(--mute); margin-bottom:18px; }
.vs-c + .vs-c .vs-h { color:var(--acc); }
.vs-l { font-size:46px; line-height:1.6; color:var(--mute); }
.vs-l s { text-decoration-thickness:2px; text-decoration-color:var(--rule); }
.vs-c + .vs-c .vs-l { color:var(--ink); }
.pill { position:absolute; left:1240px; top:84px; width:596px; height:912px; background:var(--acc); }
.pill-in { position:absolute; left:1300px; top:230px; width:480px; }
.big6 { font-family:'EB Garamond',serif; font-weight:500; font-size:300px; line-height:.9; color:var(--gold-l); }
.pill-t { font-size:56px; line-height:1.1; color:var(--paper); margin-top:24px; }
.pill-s { font-size:32px; font-style:italic; line-height:1.35; color:var(--on); margin-top:22px; }
section.grades .rh { width:1010px; } section.grades .rh-r { display:none; } .rh2 { position:absolute; left:1300px; top:100px; width:480px; text-align:right; font-size:24px; letter-spacing:4px; color:var(--gold-l); }
section.grades .folio { left:595px; }
"""
FACES = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Amiri:wght@400;700&family=IM+Fell+English&display=swap">'
GRAIN = '<div class="grain"></div>'
def rosette(size=34, fill='#17433A'):
    return f'<svg width="{size}" height="{size}" viewBox="-50 -50 100 100"><rect x="-50" y="-50" width="100" height="100" fill="#EDE6D6"/><g fill="{fill}"><rect x="-30" y="-30" width="60" height="60"/><rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/></g><circle r="11" fill="#E3C37E"/></svg>'
def small(fill='#17433A'):
    return f'<svg width="22" height="22" viewBox="-50 -50 100 100"><g fill="{fill}"><rect x="-30" y="-30" width="60" height="60"/><rect x="-30" y="-30" width="60" height="60" transform="rotate(45)"/></g></svg>'
def furniture(n, right):
    c = ''.join(f'<div class="corner c{i}">{rosette()}</div>' for i in (1, 2, 3, 4))
    return (GRAIN + '<div class="frame-o"></div><div class="frame-i"></div>' + c +
            f'<div class="rh"><p class="rh-l">The Imam Muhammad Adam Institute</p><p class="rh-r">{right}</p></div>' +
            f'<div class="folio">{small()}<p class="num">{n}</p>{small()}</div>')
def page(cls, body):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8">{FACES}<style>{CSS}</style></head><body><section class="{cls}">{body}</section></body></html>'

S = {}
S['s02'] = page('', furniture(2, 'Opening') + '''
<div style="position:absolute;left:150px;top:190px;width:1620px;text-align:center">
  <p class="kick">OPENING</p>
  <h2>Who are we, and who should <i>we become</i>?</h2>
  <p class="lead">A warm welcome to our respected teachers, honoured guests and fellow students.</p>
</div>
<div class="trio" style="top:500px">
  <div class="cell first"><p class="who">WHO</p><p class="cell-tx">Who are we as <i>young Muslims</i>?</p></div>
  <div class="cell"><p class="who">WHAT</p><p class="cell-tx">What <i>values</i> should define us?</p></div>
  <div class="cell"><p class="who">WHO NEXT</p><p class="cell-tx">Who should we <i>aspire</i> to become?</p></div>
</div>
<div class="band"><p>A question at the heart of our education <i>and our future</i></p></div>
''')
S['s03'] = page('split', furniture(3, 'Opening · The essence') + '''
<div class="panel"></div>
<div class="panel-in">
  <p class="kick" style="color:#E3C37E">ALLAH TAʿĀLĀ SAYS</p>
  <p class="ar p-ar">وَمَنْ أَحْسَنُ قَوْلًا مِّمَّن دَعَآ إِلَى ٱللَّهِ وَعَمِلَ صَٰلِحًا وَقَالَ إِنَّنِى مِنَ ٱلْمُسْلِمِينَ</p>
  <p class="p-tr">“And who is better in speech than one who calls towards Allah, does righteous deeds, and says: Indeed, I am among the Muslims?”</p>
  <p class="p-ref">SŪRAT FUṢṢILAT 41:33</p>
</div>
<div class="right">
  <p class="kick">THE ESSENCE OF BEING MUSLIM</p>
  <h2>Not our names, clothes or families, but <i>our faith</i></h2>
  <div class="rows">
    <div class="row"><p class="row-k">ROOTED IN</p><p class="row-v">our <i>faith</i></p></div>
    <div class="row"><p class="row-k">REFLECTED IN</p><p class="row-v">our <i>character</i></p></div>
    <div class="row"><p class="row-k">SHOWN THROUGH</p><p class="row-v">our <i>actions</i></p></div>
  </div>
  <p class="lead">Islam is not simply an identity we inherit, but a responsibility we strive to live up to.</p>
</div>
''')
S['s04'] = page('', furniture(4, 'The value of our youth') + '''
<div class="cen">
  <p class="kick">THE VALUE OF OUR YOUTH</p>
  <p class="ar h-ar">اغْتَنِمْ خَمْسًا قَبْلَ خَمْسٍ: شَبَابَكَ قَبْلَ هَرَمِكَ</p>
  <p class="h-tr">“Take advantage of five things before five: your <span style="color:#17433A">youth</span> before your old age.”</p>
  <p class="ref" style="margin-top:16px">REPORTED BY AL-ḤĀKIM AND AL-BAYHAQĪ</p>
</div>
<div class="trio" style="top:590px">
  <div class="cell first"><p class="who">A TIME OF</p><p class="cell-tx"><i>Opportunity</i></p></div>
  <div class="cell"><p class="who">A TIME OF</p><p class="cell-tx"><i>Growth</i></p></div>
  <div class="cell"><p class="who">A TIME OF</p><p class="cell-tx"><i>Responsibility</i></p></div>
</div>
<div class="band"><p>The choices we make today <i>shape who we become tomorrow</i></p></div>
''')
S['s05'] = page('grades', furniture(5, 'Six pillars') + '''
<div class="left">
  <p class="kick">AS STUDENTS OF THE INSTITUTE</p>
  <h2>Our education is about <i>far more</i></h2>
  <div class="vs">
    <div class="vs-c"><p class="vs-h">MORE THAN</p>
      <p class="vs-l">Examinations<br>Qualifications<br>Careers</p></div>
    <div class="vs-c"><p class="vs-h">IT IS ABOUT</p>
      <p class="vs-l">Nurturing our faith<br>Enriching our minds<br>Refining our character<br>Preparing to contribute</p></div>
  </div>
</div>
<div class="pill"></div><p class="rh2">Six pillars</p>
<div class="pill-in">
  <p class="kick" style="color:#E3C37E">SO WHAT KIND OF YOUNG MUSLIMS?</p>
  <p class="big6">6</p>
  <p class="pill-t">foundational pillars</p>
  <p class="pill-s">to shape the identity we strive to embody</p>
</div>
''')
for k, v in S.items(): open(k + '.html', 'w').write(v)
print('ok')
