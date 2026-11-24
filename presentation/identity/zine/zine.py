import math, random
exec(open('common.py', encoding='utf-8').read())
BLUE, ORANGE, PAPER, DARK, YEL = '#2B54C4', '#FF6A3D', '#F4EFE4', '#26244A', '#FFC93C'
FACES = {"bricolage-grotesque": {"family": "Bricolage Grotesque", "href": "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap"},
         "noto-sans": {"family": "Noto Sans", "href": "https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap"},
         "lalezar": {"family": "Lalezar", "href": "https://fonts.googleapis.com/css2?family=Lalezar&display=swap"},
         "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}}
def halftone(w, h, col, cls, step=26, seed=1, fade='br'):
    random.seed(seed); c = ''
    for y in range(0, h, step):
        for x in range(0, w, step):
            fx, fy = x / w, y / h
            t = {'br': (fx + fy) / 2, 'bl': ((1 - fx) + fy) / 2, 'c': 1 - min(1, math.hypot(fx - .5, fy - .5) * 2)}[fade]
            r = step * 0.46 * t
            if r > 1: c += f'<circle cx="{x}" cy="{y}" r="{r:.1f}"/>'
    return f'<svg class="ht {cls}" aria-label="" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g fill="{col}">{c}</g></svg>'
def arrow(w, h, cls, col=BLUE, d=None):
    d = d or f'M10 {h-20} C {w*0.35} {h*0.1}, {w*0.65} {h*0.1}, {w-30} {h*0.45}'
    return (f'<svg class="arw {cls}" aria-label="" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{d}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{w-62} {h*0.45-30} L{w-28} {h*0.45} L{w-66} {h*0.45+22}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
def scrib(w, cls, col=ORANGE):
    pts = ' '.join(f'{x},{(14 if (x // 30) % 2 else 4)}' for x in range(0, w + 1, 30))
    return f'<svg class="scr {cls}" aria-label="" width="{w}" height="20" viewBox="0 0 {w} 20"><polyline points="{pts}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def tick(s=44): return f'<svg aria-label="" width="{s}" height="{s}" viewBox="0 0 44 44"><rect x="3" y="3" width="38" height="38" fill="none" stroke="{BLUE}" stroke-width="4"/><path d="M10 22 L19 31 L38 6" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def foot(right): return f'<p class="mono pf-l">OUR IDENTITY AS YOUNG MUSLIMS</p><p class="mono pf-r">{right}</p>'
S = {}
S['cover'] = (f'''{halftone(760, 520, ORANGE, "cv-ht", seed=2)}<p class="mono cv-k d1">THE IMAM MUHAMMAD ADAM INSTITUTE · ZINE NO. 1</p>
<h1 class="mis cv-t d1">OUR<br>IDENTITY</h1><p class="lz cv-ar d2">هويتنا</p>
<div class="tape cv-tape d2"><p class="cv-tt">as young Muslims</p></div>
<div class="sticker cv-st d3"><p class="st-n">6</p><p class="st-t">QUALITIES</p></div>
<img class="cv-cal d3" src="{{{{CALB}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:520px;height:112px">''', 'paper')
S['question'] = (f'''{foot('WHO ARE WE?')}<div class="q-dot"></div>{halftone(700, 700, BLUE, "q-ht", seed=3, fade='c')}<p class="q-mark">?</p>
<p class="lz q-ar d1">من نحن؟</p><h2 class="mis q-t d2">WHO<br>ARE WE?</h2><p class="body q-s d3">And what kind of Muslims do we want to become?</p>''', 'paper')
verbs = [('ANCHOR', 'our faith'), ('PURSUE', 'knowledge'), ('BUILD', 'character'), ('PREPARE', 'to serve')]
S['grades'] = (f'''{foot('WHO ARE WE?')}<h2 class="mis gr-t d1">MORE THAN <span class="strike">GRADES</span></h2>{scrib(520, "gr-x d1", ORANGE)}
<p class="body gr-s d1">We are here for more than exams, good grades or a good career.</p>
<div class="gr-row d2">{''.join(f'<div class="sticker gs{i}"><p class="st-v">{v}</p><p class="st-o">{o}</p></div>' for i, (v, o) in enumerate(verbs))}</div>
<div class="tape gr-tape d3"><p class="gr-aim">Our aim: Muslims whose knowledge, character and actions benefit the people around us.</p></div>''', 'paper')
route = f'<svg class="route" aria-label="" width="1600" height="420" viewBox="0 0 1600 420"><path d="M120 330 C 420 40, 640 60, 800 170 S 1220 420, 1480 120" fill="none" stroke="{BLUE}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/></svg>'
S['continents'] = (f'''{foot('WHERE WE COME FROM')}<h2 class="mis ct-t d1">THREE CONTINENTS</h2>{route.replace('class="route"', 'class="route d2"')}
<div class="sticker cs1 d2"><p class="st-n">1</p></div><div class="sticker cs2 d2"><p class="st-n">2</p></div><div class="sticker cs3 d2"><p class="st-n">3</p></div>
<div class="lbl l1 d2"><p class="lbl-h">SPAIN & NORTH AFRICA</p><p class="body lbl-d">al-Andalus and Fez</p></div>
<div class="lbl l2 d2"><p class="lbl-h">THE MIDDLE EAST</p><p class="body lbl-d">Baghdad, Cairo and Damascus</p></div>
<div class="lbl l3 d2"><p class="lbl-h">INDONESIA & CHINA</p><p class="body lbl-d">trade, travel and scholarship</p></div>
<p class="body ct-s d3">Men and women of many backgrounds built on earlier discoveries and pushed knowledge further.</p>''', 'paper')
rots = [-5, 4, -3, 5, -4, 3]
S['overview'] = (f'''{foot('THE SIX QUALITIES')}<h2 class="mis ov-t d1">SIX QUALITIES</h2>{halftone(600, 400, ORANGE, "ov-ht", seed=5, fade='bl')}
<div class="ov d2">{''.join(f'<div class="card" style="transform:rotate({rots[k]}deg)"><p class="card-n">{k + 1}</p><p class="lz card-ar">{a}</p><p class="card-t">{t.upper()}</p></div>' for k, (t, a) in enumerate(SIX))}</div>''', 'paper')
def quality(id_, flip):
    q = Q[id_]
    quote = (f'<p class="ar qq-ar">{q["ar"]}</p><p class="body qq-tr">{q["tr"]}</p><p class="mono qq-ref">{q["ref"]}</p>' if 'ar' in q else f'<p class="body qq-lead">“{q["lead"]}”</p>')
    aims = ''.join(f'<div class="aim">{tick(44)}<p class="aim-t">{a}</p></div>' for a in AIMS[id_])
    side = 'qf' if flip else 'qn'
    return (f'''{foot(q['title'].upper())}<p class="qnum {side}">{q['n']}</p>{halftone(560, 560, ORANGE if flip else BLUE, "qht " + side, seed=q['n'], fade='c')}
<div class="qhead {side} d1"><p class="lz qw">{q['word']}</p><h2 class="mis qt">{q['title'].upper()}</h2><p class="body qsub">{q['sub']}</p></div>
<div class="note {side} d2"><div class="tape nt"></div>{quote}</div>
<div class="aims {side} d3">{aims}</div>
<div class="sticker qst {side} d3"><p class="body qst-t">{q['foot']}</p></div>''', 'paper')
for i, k in enumerate(Q): S[k] = quality(k, i % 2 == 1)
crot = [-3, 2, -2, 3, -2, 2]
S['cabinet'] = (f'''{foot('SEEKERS OF KNOWLEDGE')}<h2 class="mis cb-t d1">WHEN FAITH FUELLED CURIOSITY</h2>
<div class="cab d2">{''.join(f'<div class="spec" style="transform:rotate({crot[i]}deg)"><div class="tape st"></div><p class="spec-h">{h.upper()}</p><p class="body spec-n">{n}</p></div>' for i, (h, n) in enumerate(CAB))}</div>
<p class="body cb-s d3">From the House of Wisdom in Baghdad to al-Qarawiyyīn in Fez, the world’s oldest university still operating.</p>''', 'paper')
S['numbers'] = (f'''{foot('SEEKERS OF KNOWLEDGE')}<p class="mono nm-k d1">WITH PARCHMENT, INK AND HARD WORK</p>
<div class="nm d2"><div class="nmc"><div class="blob b1"></div><p class="mis nm-n">200+</p><p class="nm-t">surgical instruments</p><p class="body nm-w">al-Zahrāwī</p></div>
<div class="nmc"><div class="blob b2"></div><p class="mis nm-n">75,000</p><p class="nm-t">miles travelled</p><p class="body nm-w">Ibn Baṭṭūṭa</p></div>
<div class="nmc"><div class="blob b3"></div><p class="mis nm-n">44</p><p class="nm-t">of today’s countries</p><p class="body nm-w">Ibn Baṭṭūṭa</p></div></div>''', 'paper')
S['room'] = (f'''{foot('SEEKERS OF KNOWLEDGE')}{halftone(820, 820, ORANGE, "rm-ht", seed=7, fade='c')}<p class="lz rm-ar d1">اقرأ</p><p class="mono rm-k d1">READ</p>
<h2 class="mis rm-t d2">WHY NOT<br>IN THIS ROOM?</h2><p class="body rm-s d2">Why shouldn’t the next great doctor, engineer, mathematician or scholar be sitting here?</p>
{arrow(380, 220, "rm-arw d3", ORANGE)}<div class="sticker rm-st d3"><p class="st-t">YOU?</p></div>''', 'paper')
scale = (f'<svg class="scale" aria-label="A balance tipping towards faith and humility" width="1300" height="560" viewBox="0 0 1300 560">'
         f'<path d="M650 326 L585 450 L715 450 Z" fill="{BLUE}"/><line x1="170" y1="250" x2="1130" y2="380" stroke="{DARK}" stroke-width="10" stroke-linecap="round" transform="rotate(0)"/>'
         f'<circle cx="650" cy="318" r="18" fill="{ORANGE}"/></svg>')
S['balance'] = (f'''{foot('SEEKERS OF KNOWLEDGE')}<h2 class="mis bl-t d1">KNOWLEDGE NEEDS CHARACTER</h2>{scale.replace('class="scale"', 'class="scale d2"')}
<div class="pan p1 d2"><p class="body pan-h">knowledge without character</p><p class="pan-r dim">ARROGANCE</p></div>
<div class="pan p2 d3"><p class="body pan-h">knowledge with faith and humility</p><p class="pan-r">BENEFITS<br>EVERYONE</p></div>''', 'paper')
S['journey'] = (f'''{foot('CONFIDENT IN SOCIETY')}<h2 class="mis ct-t d1">FROM MADĪNAH TO LONDON</h2>{route.replace('class="route"', 'class="route d2"')}
<div class="sticker cs1 d2"><p class="st-n">1</p></div><div class="sticker cs2 d2"><p class="st-n">2</p></div><div class="sticker cs3 d2"><p class="st-n">3</p></div>
<div class="lbl l1 d2"><p class="body lbl-h2">Madīnah</p><p class="body lbl-d">neighbours of other faiths, under agreed rights and justice</p></div>
<div class="lbl l2 d2"><p class="lbl-h">THE TRADE ROUTES</p><p class="body lbl-d">ideas, navigation, citrus, rice and irrigation</p></div>
<div class="lbl l3 d2"><p class="lbl-h">LONDON</p><p class="body lbl-d">Yemeni coffee reaches the “penny universities”</p></div>''', 'paper')
S['chapter'] = (f'''{foot('STRIVING FOR EXCELLENCE')}<div class="page pl d1"><p class="mono pg-k">THEIR CHAPTER</p><p class="pg-n">The Alhambra</p><p class="pg-n">The Süleymaniye</p><p class="body pg-b">Ibn Rushd · Ibn Khaldūn · Rūmī · Saʿdī</p></div>
<div class="page pr d2"><p class="mono pg-k">OUR CHAPTER</p><div class="pg-ln"></div><div class="pg-ln"></div><div class="pg-ln"></div><div class="pg-ln"></div><p class="pg-q">your name here</p></div>
{arrow(300, 180, "ch-arw d3", ORANGE)}''', 'paper')
S['heritage'] = (f'''{foot('OUR HERITAGE')}<h2 class="mis hr-t d1">OUR HERITAGE, OUR RESPONSIBILITY</h2>
<div class="hr d2">{''.join(f'<div class="hr-c"><p class="hr-a">{a}</p><p class="mono hr-w">— WITHOUT —</p><p class="body hr-b">{b}</p></div>' for a, b in COUPLETS)}</div>
<div class="tape hr-tape d3"><p class="hr-g">True greatness: faith with knowledge, knowledge with character, character with service.</p></div>''', 'paper')
S['six'] = (f'''{foot('TO CARRY FORWARD')}<h2 class="mis sx-t d1">TAKE THESE WITH YOU</h2>{halftone(560, 560, BLUE, "sx-ht", seed=9, fade='br')}
<div class="chk d2">{''.join(f'<div class="ck">{tick(64)}<p class="ck-t">{t}</p><p class="lz ck-ar">{a}</p></div>' for t, a in SIX)}</div>''', 'paper')
S['final'] = (f'''{foot('A FINAL THOUGHT')}{halftone(900, 600, ORANGE, "fn-ht", seed=11, fade='bl')}<h2 class="mis fn-t d1">WHAT WILL PEOPLE REMEMBER?</h2>{scrib(700, "fn-x d1", ORANGE)}
<p class="body fn-q d2">Not our grades or our prizes, but how we treated them, whether we kept our word, and whether we stood up for what was right.</p>
<div class="tape fn-tape d3"><p class="fn-c">Let us be a generation firm in faith, rich in knowledge, noble in character, confident in our identity and devoted to serving others.</p></div>
<div class="sticker fn-st d3"><p class="st-t">YOUR<br>QUESTIONS</p></div>
<img class="fn-cal d3" src="{{{{CALB}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:460px;height:99px">''', 'paper')
write_deck('zin-out', 'Our Identity as Young Muslims — Zine', S, open('zine.css', encoding='utf-8').read(), FACES, SECTIONS,
           {'CALB': ('__CALB_BLOB__', '../callig-blue.png')}, 'zin-prev')
print('ok')
