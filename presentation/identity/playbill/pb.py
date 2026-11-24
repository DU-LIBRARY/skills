exec(open('common.py', encoding='utf-8').read())
G, GL, CR, INK = '#17433A', '#E2C478', '#F2EBDC', '#10302A'
FACES = {"playfair-display": {"family": "Playfair Display", "href": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,900;1,500;1,700&display=swap"},
         "manrope": {"family": "Manrope", "href": "https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap"},
         "eb-garamond": {"family": "EB Garamond", "href": "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap"},
         "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}}
def rule(cls=''): return f'<div class="rule {cls}"></div>'
def chrome(right, cream=False): return f'<div class="frame"></div><p class="lab rh-l">OUR IDENTITY AS YOUNG MUSLIMS</p><p class="lab rh-r">{right}</p>'
S = {}
S['cover'] = (f'''<div class="frame"></div><p class="lab cv-k d1">THE IMAM MUHAMMAD ADAM INSTITUTE PRESENTS</p>{rule('cv-r1 d1')}
<p class="cv-a d2">OUR</p><p class="cv-b d2">IDENTITY</p><p class="cv-c d2">as Young Muslims</p>{rule('cv-r2 d3')}
<img class="cv-cal d3" src="{{{{CALL}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:560px;height:120px">''', 'green')
S['question'] = (f'''{chrome('WHO ARE WE?')}<p class="ar q-ar d1">مَنْ نَحْنُ؟</p>{rule('q-r d2')}<p class="disp q-t d2">WHO ARE WE?</p>
<p class="ital q-s d3">And what kind of Muslims do we want to become?</p>''', 'green')
verbs = [('ANCHOR', 'our faith'), ('PURSUE', 'knowledge'), ('BUILD', 'character'), ('PREPARE', 'to serve')]
S['grades'] = (f'''{chrome('WHO ARE WE?')}<p class="disp gr-t d1">MORE THAN GRADES</p><p class="body-c gr-s d1">We are here for more than exams, good grades or a good career.</p>
<div class="gr-row d2">{''.join(f'<div class="gr-c"><p class="gr-v">{v}</p><p class="ital gr-o">{o}</p></div>' for v, o in verbs)}</div>
<div class="inv gr-aim d3"><p class="inv-t">Our aim: Muslims whose knowledge, character and actions benefit the people around us.</p></div>''', 'cream')
stops = [('SPAIN & NORTH AFRICA', 'al-Andalus, Fez'), ('THE MIDDLE EAST', 'Baghdad, Cairo, Damascus'), ('INDONESIA & CHINA', 'trade, travel and scholarship')]
S['continents'] = (f'''{chrome('WHERE WE COME FROM')}<p class="disp ct-t d1">ACROSS THREE CONTINENTS</p>{rule('ct-r d1')}
<div class="ct-row d2">{('<p class="ct-arrow">→</p>').join(f'<div class="ct-c"><p class="ct-n">{n}</p><p class="ital ct-d">{d}</p></div>' for n, d in stops)}</div>
<p class="body-c ct-s d3">Muslim men and women of many backgrounds built on earlier discoveries, invented new things and pushed human knowledge further.</p>''', 'green')
S['overview'] = (f'''{chrome('THE SIX QUALITIES')}<p class="disp ov-t d1">SIX QUALITIES</p><p class="ital ov-s d1">describe who we are, and who we want to be</p>
<div class="ov-g d2">{''.join(f'<div class="ov-c"><p class="ov-n">{k+1}</p><p class="ov-nm">{t.upper()}</p><p class="ar ov-ar">{a}</p></div>' for k, (t, a) in enumerate(SIX))}</div>''', 'cream')
def quality(id_, alt):
    q = Q[id_]
    quote = (f'<p class="ar qq-ar">{q["ar"]}</p><p class="ital qq-tr">{q["tr"]}</p><p class="lab qq-ref">{q["ref"].upper() if q["ref"].isascii() else ""}</p>' + ('' if q["ref"].isascii() else f'<p class="body-c qq-ref2">{q["ref"]}</p>')
             if 'ar' in q else f'<p class="ital qq-lead">“{q["lead"]}”</p>')
    aims = ''.join(f'<p class="qa">{a}</p>' for a in AIMS[id_])
    cls = 'green' if alt else 'cream'
    return (f'''{chrome(q['title'].upper())}<p class="qn">{q['n']}</p>
<div class="qr"><div class="d1">{rule()}<p class="disp qt">{q['title'].upper()}</p>{rule()}<p class="ar qw">{q['word']}</p></div>
<div class="d2">{quote}</div><div class="qas d3">{aims}</div></div>''', cls)
for i, k in enumerate(Q): S[k] = quality(k, i % 2 == 0)
S['cabinet'] = (f'''{chrome('SEEKERS OF KNOWLEDGE')}<p class="disp cb-t d1">WHEN FAITH FUELLED CURIOSITY</p>
<p class="body-c cb-s d1">From the House of Wisdom in Baghdad to al-Qarawiyyīn in Fez, the world’s oldest university still operating</p>
<div class="cb-g d2">{''.join(f'<div class="cb-c"><p class="lab cb-h">{h.upper()}</p><p class="body cb-n">{n}</p></div>' for h, n in CAB)}</div>''', 'cream')
S['numbers'] = (f'''{chrome('SEEKERS OF KNOWLEDGE')}<p class="lab nm-k d1">WITH PARCHMENT, INK AND HARD WORK</p>
<div class="nm-row d2">{''.join(f'<div class="nm-c"><p class="nm-n">{n}</p><p class="ital nm-t">{t}</p><p class="body-c nm-w">{w}</p></div>' for n, t, w in NUMS)}</div>''', 'green')
S['room'] = (f'''<div class="half-cr"></div>{chrome('SEEKERS OF KNOWLEDGE')}<p class="ar rm-ar d1">اقْرَأْ</p><p class="lab rm-k d1">READ</p>
<div class="rm-r d2"><p class="disp rm-t">WHY NOT IN THIS ROOM?</p>{rule()}<p class="ital rm-s">Why shouldn’t the next great doctor, engineer, mathematician or scholar be sitting here?</p></div>''', 'green')
S['balance'] = (f'''{chrome('SEEKERS OF KNOWLEDGE')}<p class="disp bl-t d1">KNOWLEDGE NEEDS CHARACTER</p>
<div class="bl-row"><div class="bl-c d2"><p class="ital bl-h">Knowledge without character</p><p class="lab bl-m">LEADS TO</p><p class="disp bl-r dim">ARROGANCE</p></div>
<div class="bl-v"></div><div class="bl-c d3"><p class="ital bl-h">Knowledge guided by faith and humility</p><p class="lab bl-m">BENEFITS</p><p class="disp bl-r">EVERYONE</p></div></div>''', 'cream')
jr = [('MADINAH', 'Muslims and neighbours of other faiths, under agreed rights and justice'), ('THE TRADE ROUTES', 'ideas, navigation, citrus, rice and irrigation across Africa, Asia and Europe'), ('LONDON', 'Yemeni coffee reaches the coffeehouses, the “penny universities”')]
S['journey'] = (f'''{chrome('CONFIDENT IN SOCIETY')}<p class="disp jr-t d1">FROM MADINAH TO LONDON</p>{rule('jr-r d1')}
<div class="jr-row d2">{('<p class="ct-arrow">→</p>').join(f'<div class="jr-c"><p class="jr-n">{n}</p><p class="body-c jr-d">{d}</p></div>' for n, d in jr)}</div>''', 'cream')
S['chapter'] = (f'''<div class="half-cr"></div>{chrome('STRIVING FOR EXCELLENCE')}
<div class="ch-l d1"><p class="lab ch-k">THEIR CHAPTER</p><p class="ch-n">The Alhambra</p><p class="ch-n">The Süleymaniye</p><p class="body ch-b">Ibn Rushd · Ibn Khaldūn · Rūmī · Saʿdī</p></div>
<div class="ch-r d2"><p class="lab ch-k2">OUR CHAPTER</p><div class="ch-line"></div><div class="ch-line"></div><div class="ch-line"></div><p class="disp ch-q">IS OURS TO WRITE</p></div>''', 'green split')
S['heritage'] = (f'''{chrome('OUR HERITAGE')}<p class="disp hr-t d1">OUR HERITAGE, OUR RESPONSIBILITY</p>
<div class="hr-g d2">{''.join(f'<div class="hr-c"><p class="hr-a">{a}</p><p class="lab hr-w">WITHOUT</p><p class="ital hr-b">{b}</p></div>' for a, b in COUPLETS)}</div>
<div class="inv hr-band d3"><p class="inv-t">True greatness: faith with knowledge, knowledge with character, character with service.</p></div>''', 'cream')
S['six'] = (f'''{chrome('TO CARRY FORWARD')}<p class="disp sx-t d1">THE SIX QUALITIES</p>{rule('sx-r d1')}
<div class="sx-g d2">{''.join(f'<div class="sx-c"><p class="ar sx-ar">{a}</p><p class="lab sx-nm">{t.upper()}</p></div>' for t, a in SIX)}</div>''', 'green')
S['final'] = (f'''{chrome('A FINAL THOUGHT')}<p class="disp fn-t d1">WHAT WILL PEOPLE REMEMBER?</p>{rule('fn-r d1')}
<p class="ital fn-q d2">Not our grades or our prizes, but how we treated them, whether we kept our word, and whether we stood up for what was right.</p>
<p class="body-c fn-c d3">Let us be a generation firm in faith, rich in knowledge, noble in character, confident in our identity and devoted to serving others.</p>
<img class="fn-cal d3" src="{{{{CALL}}}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:520px;height:112px">''', 'green')
CSS = open('pb.css', encoding='utf-8').read()
write_deck('pb-out', 'Our Identity as Young Muslims — Playbill', S, CSS, FACES, SECTIONS,
           {'CALL': ('__CALL_BLOB__', '../../callig-light.png'), 'CALG': ('__CALG_BLOB__', '../callig-green.png')}, 'pb-prev')
print('ok')
