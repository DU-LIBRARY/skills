exec(open('common.py', encoding='utf-8').read())
FACES = {"stardos-stencil": {"family": "Stardos Stencil", "href": "https://fonts.googleapis.com/css2?family=Stardos+Stencil:wght@400;700&display=swap"},
         "barlow-condensed": {"family": "Barlow Condensed", "href": "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;800&display=swap"},
         "noto-sans": {"family": "Noto Sans", "href": "https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,600;1,400&display=swap"},
         "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}}
QC = {'faith': 'tg', 'knowledge': 'tn', 'character': 'ts', 'society': 'tt', 'service': 'to', 'excellence': 'tgold'}
SIXC = ['tg', 'tn', 'ts', 'tt', 'to', 'tgold']
def top(right): return f'<p class="lab rh-l">OUR IDENTITY AS YOUNG MUSLIMS</p><p class="lab rh-r">{right}</p>'
S = {}
S['cover'] = (f'''<div class="tab tg cv-a d1"><p class="lab cv-k">THE IMAM MUHAMMAD ADAM INSTITUTE</p><p class="st cv-t">OUR<br>IDENTITY</p></div>
<div class="tab tgold cv-b d2"><p class="st cv-as">AS YOUNG<br>MUSLIMS</p><p class="lab cv-s">6 QUALITIES · 1 FOUNDATION</p></div>
<img class="cv-cal d3" src="{{{{CALG}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:640px;height:137px">''', 'bone')
S['question'] = (f'''{top('WHO ARE WE?')}<p class="st q-t d1">WHO<br>ARE WE?</p>
<div class="tab tg q-tab d2"><p class="ar q-ar">مَنْ نَحْنُ؟</p></div>
<p class="body q-s d3">And what kind of Muslims do we want to become?</p>''', 'bone')
verbs = [('ANCHOR', 'our faith', 'tg'), ('PURSUE', 'knowledge', 'tn'), ('BUILD', 'character', 'ts'), ('PREPARE', 'to serve', 'tt')]
S['grades'] = (f'''{top('WHO ARE WE?')}<p class="st h1 d1">MORE THAN GRADES</p>
<div class="gr-row d2">{''.join(f'<div class="tab {c} gr-c"><p class="gr-n">{i+1}</p><p class="st gr-v">{v}</p><p class="lab gr-o">{o.upper()}</p></div>' for i, (v, o, c) in enumerate(verbs))}</div>
<p class="body gr-aim d3">Our aim: Muslims whose knowledge, character and actions benefit the people around us.</p>''', 'bone')
stops = [('SPAIN & NORTH AFRICA', 'al-Andalus and Fez', 'ts'), ('THE MIDDLE EAST', 'Baghdad, Cairo and Damascus', 'tgold'), ('INDONESIA & CHINA', 'trade, travel and scholarship', 'tt')]
S['continents'] = (f'''{top('WHERE WE COME FROM')}<p class="st h1 d1">THREE CONTINENTS</p>
<div class="ct-row d2">{''.join(f'<div class="tab {c} ct-c"><p class="gr-n">{i+1}</p><p class="lab ct-n">{n}</p><p class="body ct-d">{d}</p></div>' for i, (n, d, c) in enumerate(stops))}</div>
<p class="body ct-s d3">Muslim men and women of many backgrounds built on earlier discoveries, invented new things and pushed human knowledge further.</p>''', 'bone')
S['overview'] = (f'''{top('THE SIX QUALITIES')}<p class="st h1 d1">SIX QUALITIES</p>
<div class="six d2">{''.join(f'<div class="tab {c} sx-c"><p class="sx-n">{i+1}</p><p class="ar sx-ar">{a}</p><p class="lab sx-t">{t.upper()}</p></div>' for i, ((t, a), c) in enumerate(zip(SIX, SIXC)))}</div>''', 'bone')
def quality(id_):
    q = Q[id_]; c = QC[id_]
    quote = (f'<p class="ar qq-ar">{q["ar"]}</p><p class="body qq-tr">{q["tr"]}</p><p class="body qq-ref">{q["ref"]}</p>' if 'ar' in q else f'<p class="body qq-lead">“{q["lead"]}”</p>')
    return (f'''{top(q['title'].upper())}<div class="tab {c} qt-tab d1"><p class="qt-n">{q['n']}</p><p class="ar qt-w">{q['word']}</p><p class="st qt-t">{q['title'].upper()}</p></div>
<div class="qr"><div class="d2">{quote}</div><p class="lab qr-k d3">WE TRY TO</p><div class="pills d3">{''.join(f'<p class="pill">{a.upper()}</p>' for a in AIMS[id_])}</div>
<p class="body qr-f d3">{q['foot']}</p></div>''', 'bone')
for k in Q: S[k] = quality(k)
S['cabinet'] = (f'''{top('SEEKERS OF KNOWLEDGE')}<p class="st h1 h1s d1">WHEN FAITH FUELLED CURIOSITY</p>
<div class="cab d2">{''.join(f'<div class="tab {c} cb-c"><p class="lab cb-h">{h.upper()}</p><p class="body cb-n">{n}</p></div>' for (h, n), c in zip(CAB, SIXC))}</div>
<p class="body cb-s d3">From the House of Wisdom in Baghdad to al-Qarawiyyīn in Fez, the world’s oldest university still operating.</p>''', 'bone')
S['numbers'] = (f'''{top('SEEKERS OF KNOWLEDGE')}<p class="st h1 d1">PARCHMENT, INK, HARD WORK</p>
<div class="nm d2">{''.join(f'<div class="tab {c} nm-c"><p class="st nm-n">{n}</p><p class="lab nm-t">{t.upper()}</p><p class="body nm-w">{w}</p></div>' for (n, t, w), c in zip(NUMS, ['tg', 'ts', 'tn']))}</div>''', 'bone')
S['room'] = (f'''{top('SEEKERS OF KNOWLEDGE')}<div class="tab tg rm-tab d1"><p class="ar rm-ar">اقْرَأْ</p><p class="lab rm-k">READ</p></div>
<div class="rm-r d2"><p class="st rm-t">WHY NOT IN THIS ROOM?</p><p class="body rm-s">Why shouldn’t the next great doctor, engineer, mathematician or scholar be sitting here?</p></div>''', 'bone')
S['balance'] = (f'''{top('SEEKERS OF KNOWLEDGE')}<p class="st h1 h1s d1">KNOWLEDGE NEEDS CHARACTER</p>
<div class="bl d2"><div class="tab tgrey bl-c"><p class="body bl-h">Knowledge without character</p><p class="lab bl-m">LEADS TO</p><p class="st bl-r">ARROGANCE</p></div>
<div class="tab tg bl-c"><p class="body bl-h">Knowledge guided by faith and humility</p><p class="lab bl-m">BENEFITS</p><p class="st bl-r">EVERYONE</p></div></div>''', 'bone')
jr = [('MADINAH', 'Muslims and neighbours of other faiths, under agreed rights and justice', 'tg'), ('TRADE ROUTES', 'Ideas, navigation, citrus, rice and irrigation across Africa, Asia and Europe', 'tgold'), ('LONDON', 'Yemeni coffee reaches the coffeehouses, the “penny universities”', 'tn')]
S['journey'] = (f'''{top('CONFIDENT IN SOCIETY')}<p class="st h1 d1">FROM MADINAH TO LONDON</p>
<div class="ct-row d2">{''.join(f'<div class="tab {c} ct-c"><p class="gr-n">{i+1}</p><p class="st jr-n">{n}</p><p class="body ct-d">{d}</p></div>' for i, (n, d, c) in enumerate(jr))}</div>''', 'bone')
S['chapter'] = (f'''{top('STRIVING FOR EXCELLENCE')}<div class="tab tgold ch-a d1"><p class="lab ch-k">THEIR CHAPTER</p><p class="st ch-n">THE ALHAMBRA<br>THE SÜLEYMANIYE</p><p class="body ch-b">Ibn Rushd · Ibn Khaldūn · Rūmī · Saʿdī</p></div>
<div class="tab tg ch-b2 d2"><p class="lab ch-k">OUR CHAPTER</p><div class="ch-line"></div><div class="ch-line"></div><div class="ch-line"></div><p class="st ch-q">IS OURS TO WRITE</p></div>''', 'bone')
S['heritage'] = (f'''{top('OUR HERITAGE')}<p class="st h1 h1s d1">OUR HERITAGE, OUR RESPONSIBILITY</p>
<div class="hr d2">{''.join(f'<div class="tab {c} hr-c"><p class="st hr-a">{a.upper()}</p><p class="lab hr-w">WITHOUT</p><p class="body hr-b">{b}</p></div>' for (a, b), c in zip(COUPLETS, ['ts', 'tt', 'tn']))}</div>
<div class="tab tg hr-band d3"><p class="body hr-bt">True greatness: faith with knowledge, knowledge with character, character with service.</p></div>''', 'bone')
S['six'] = (f'''{top('TO CARRY FORWARD')}<p class="st h1 d1">THE SIX QUALITIES</p>
<div class="six d2">{''.join(f'<div class="tab {c} sx-c"><p class="sx-n">{i+1}</p><p class="ar sx-ar">{a}</p><p class="lab sx-t">{t.upper()}</p></div>' for i, ((t, a), c) in enumerate(zip(SIX, SIXC)))}</div>''', 'bone')
S['final'] = (f'''<div class="tab tg fn-tab d1"><p class="lab fn-k">A FINAL THOUGHT</p><p class="st fn-t">WHAT WILL PEOPLE REMEMBER?</p>
<p class="body fn-q">Not our grades or our prizes, but how we treated them, whether we kept our word, and whether we stood up for what was right.</p></div>
<div class="tab tgold fn-b d2"><p class="body fn-c">Let us be a generation firm in faith, rich in knowledge, noble in character, confident in our identity and devoted to serving others.</p></div>
<img class="fn-cal d3" src="{{{{CALG}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:560px;height:120px">''', 'bone')
write_deck('ws-out', 'Our Identity as Young Muslims — Workshop', S, open('ws.css', encoding='utf-8').read(), FACES, SECTIONS,
           {'CALG': ('__CALG_BLOB__', '../callig-green.png')}, 'ws-prev')
print('ok')
