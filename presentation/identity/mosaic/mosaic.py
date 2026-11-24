exec(open('common.py', encoding='utf-8').read())
FACES = {"anton": {"family": "Anton", "href": "https://fonts.googleapis.com/css2?family=Anton&display=swap"},
         "noto-sans": {"family": "Noto Sans", "href": "https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap"},
         "reem-kufi": {"family": "Reem Kufi", "href": "https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&display=swap"},
         "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}}
def mot(size=240, cls='mot', op='w'):
    return (f'<svg class="{cls} {op}" aria-label="" width="{size}" height="{size}" viewBox="-50 -50 100 100"><g fill="none" stroke-width="3">'
            '<rect x="-32" y="-32" width="64" height="64"/><rect x="-32" y="-32" width="64" height="64" transform="rotate(45)"/><circle r="15"/></g></svg>')
def T(col, cs, rs, inner, cls='', d=''):
    return f'<div class="tile {col} {cls} {d}" style="grid-column:{cs};grid-row:{rs}">{inner}</div>'
def grid(*tiles): return '<div class="grid">' + ''.join(tiles) + '</div>'
S = {}
S['cover'] = (grid(
  T('green', '1 / 8', '1 / 6', f'{mot(420, "mot big")}<p class="k gold-t">THE IMAM MUHAMMAD ADAM INSTITUTE</p><div><p class="dsp cv-t">OUR<br>IDENTITY</p><p class="dsp cv-s">AS YOUNG MUSLIMS</p></div>', 'col', 'd1'),
  T('gold', '8 / 13', '1 / 4', '<p class="kufi cv-ar">هويتنا</p><p class="k">OUR IDENTITY</p>', 'col center', 'd2'),
  T('teal', '8 / 11', '4 / 6', '<p class="dsp t60">6 QUALITIES</p><p class="k">ONE FOUNDATION</p>', 'col', 'd2'),
  T('terra', '11 / 13', '4 / 6', mot(200, 'mot mid'), '', 'd2'),
  T('cream', '1 / 13', '6 / 7', '<img class="cv-cal" src="{{CALG}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:420px;height:90px"><p class="k green-t">A TRADITION OF EXCELLENCE</p>', 'row', 'd3')), 'bone')
S['question'] = (grid(
  T('green', '1 / 9', '1 / 7', f'{mot(360, "mot big")}<p class="k gold-t">WHO ARE WE?</p><p class="dsp q-t">WHO<br>ARE WE?</p>', 'col', 'd1'),
  T('gold', '9 / 13', '1 / 5', '<p class="kufi q-ar">من نحن؟</p>', 'center', 'd2'),
  T('terra', '9 / 13', '5 / 7', '<p class="body t40">And what kind of Muslims do we want to become?</p>', 'col end', 'd3')), 'bone')
verbs = [('ANCHOR', 'our faith', 'green'), ('PURSUE', 'knowledge', 'navy'), ('BUILD', 'character', 'terra'), ('PREPARE', 'to serve', 'teal')]
S['grades'] = (grid(
  T('plain', '1 / 13', '1 / 3', '<p class="dsp h-t green-t">MORE THAN GRADES</p><p class="body t36 soft-t">We are here for more than exams, good grades or a good career.</p>', 'col', 'd1'),
  *[T(c, f'{1 + 3 * i} / {4 + 3 * i}', '3 / 6', f'{mot(200, "mot corner")}<p class="num-f">{i + 1}</p><div><p class="dsp t90">{v}</p><p class="k">{o.upper()}</p></div>', 'col end', 'd2') for i, (v, o, c) in enumerate(verbs)],
  T('cream', '1 / 13', '6 / 7', '<p class="body t36 green-t">Our aim: Muslims whose knowledge, character and actions benefit the people around us.</p>', 'center', 'd3')), 'bone')
stops = [('SPAIN & NORTH AFRICA', 'al-Andalus and Fez', 'terra', '1 / 5', '3 / 7'), ('THE MIDDLE EAST', 'Baghdad, Cairo and Damascus', 'gold', '5 / 9', '2 / 6'), ('INDONESIA & CHINA', 'trade, travel and scholarship', 'teal', '9 / 13', '3 / 7')]
S['continents'] = (grid(
  T('plain', '1 / 5', '1 / 3', '<p class="dsp t100 green-t">THREE<br>CONTINENTS</p>', 'col', 'd1'),
  *[T(c, cs, rs, f'{mot(200, "mot corner")}<p class="num-f">{i + 1}</p><div><p class="dsp t54">{n}</p><p class="body t32">{d}</p></div>', 'col end', 'd2') for i, (n, d, c, cs, rs) in enumerate(stops)],
  T('plain', '5 / 9', '6 / 7', '<p class="body t28 soft-t">Men and women of many backgrounds built on earlier discoveries and pushed human knowledge further.</p>', 'col', 'd3'),
  T('plain', '9 / 13', '1 / 3', '<p class="k green-t right">WHERE WE COME FROM</p>', 'col', 'd1')), 'bone')
six_c = ['green', 'navy', 'terra', 'teal', 'olive', 'gold']
places = [('5 / 9', '1 / 4'), ('9 / 13', '1 / 3'), ('1 / 5', '3 / 7'), ('5 / 9', '4 / 7'), ('9 / 11', '3 / 7'), ('11 / 13', '3 / 7')]
S['overview'] = (grid(
  T('cream', '1 / 5', '1 / 3', '<p class="dsp t100 green-t">SIX<br>QUALITIES</p>', 'col', 'd1'),
  *[T(c, cs, rs, f'<p class="num-f">{k + 1}</p><p class="kufi ov-ar">{a}</p><p class="k">{t.upper()}</p>', 'col end', 'd2') for k, ((t, a), c, (cs, rs)) in enumerate(zip(SIX, six_c, places))]), 'bone')
QC = {'faith': ('green', 'gold', 'terra', 'teal', 'navy'), 'knowledge': ('navy', 'teal', 'gold', 'terra', 'green'),
      'character': ('terra', 'green', 'navy', 'gold', 'teal'), 'society': ('teal', 'terra', 'green', 'navy', 'gold'),
      'service': ('olive', 'navy', 'terra', 'green', 'gold'), 'excellence': ('gold', 'green', 'teal', 'terra', 'navy')}
def quality(id_, mirror):
    q = Q[id_]; c = QC[id_]
    W, R = ('9 / 13', 1) if mirror else ('1 / 5', 5)       # word tile columns, first column of the rest
    span = lambda a, b: f'{R + a} / {R + b}'
    quote = (f'<p class="ar qq-ar">{q["ar"]}</p><p class="body t32 ital">{q["tr"]}</p><p class="k soft-t">{q["ref"].upper()}</p>' if 'ar' in q
             else f'<p class="body qq-lead">“{q["lead"]}”</p>')
    aims = AIMS[id_]; n = len(aims); widths = [2] * 4 if n == 4 else [3, 3, 2]
    at, x = [], 0
    for i, a in enumerate(aims):
        at.append(T(c[1 + i % 4], span(x, x + widths[i]), '5 / 7', f'<p class="dsp t40">{a.upper()}</p>', 'col end', 'd3')); x += widths[i]
    return (grid(
        T(c[0], W, '1 / 7', f'{mot(300, "mot corner")}<p class="num-f big">{q["n"]}</p><p class="kufi qw">{q["word"]}</p><p class="body t28">{q["foot"]}</p>', 'col end', 'd1'),
        T('cream', span(0, 8), '1 / 3', f'<p class="k soft-t">{q["sub"].upper()}</p><p class="dsp qt green-t">{q["title"].upper()}</p>', 'col', 'd1'),
        T('plain', span(0, 8), '3 / 5', quote, 'col', 'd2'), *at), 'bone')
for i, k in enumerate(Q): S[k] = quality(k, i % 2 == 1)
cab_c = ['green', 'navy', 'terra', 'teal', 'olive', 'gold']
S['cabinet'] = (grid(
  T('plain', '1 / 13', '1 / 2', '<p class="dsp t84 green-t">WHEN FAITH FUELLED CURIOSITY</p>', 'col', 'd1'),
  *[T(c, f'{1 + 4 * (i % 3)} / {5 + 4 * (i % 3)}', f'{2 + 2 * (i // 3)} / {4 + 2 * (i // 3)}', f'{mot(160, "mot corner")}<p class="dsp t44">{h.upper()}</p><p class="body t30">{nm}</p>', 'col', 'd2') for i, ((h, nm), c) in enumerate(zip(CAB, cab_c))],
  T('cream', '1 / 13', '6 / 7', '<p class="body t32 green-t">From the House of Wisdom in Baghdad to al-Qarawiyyīn in Fez, the world’s oldest university still operating.</p>', 'center', 'd3')), 'bone')
S['numbers'] = (grid(
  T('green', '1 / 6', '1 / 7', f'{mot(300, "mot corner")}<p class="k gold-t">WITH PARCHMENT, INK AND HARD WORK</p><div><p class="dsp n-big">200+</p><p class="dsp t44">SURGICAL INSTRUMENTS</p><p class="body t30">al-Zahrāwī</p></div>', 'col', 'd1'),
  T('terra', '6 / 13', '1 / 4', '<p class="dsp n-mid">75,000</p><div><p class="dsp t44">MILES TRAVELLED</p><p class="body t30">Ibn Baṭṭūṭa</p></div>', 'row between', 'd2'),
  T('navy', '6 / 13', '4 / 7', '<p class="dsp n-mid">44</p><div><p class="dsp t44">OF TODAY’S COUNTRIES</p><p class="body t30">Ibn Baṭṭūṭa</p></div>', 'row between', 'd3')), 'bone')
S['room'] = (grid(
  T('green', '1 / 6', '1 / 7', f'{mot(300, "mot corner")}<p class="kufi rm-ar">اقرأ</p><p class="k gold-t">READ</p>', 'col center', 'd1'),
  T('plain', '6 / 13', '1 / 5', '<p class="dsp rm-t green-t">WHY NOT<br>IN THIS ROOM?</p>', 'col end', 'd2'),
  T('gold', '6 / 13', '5 / 7', '<p class="body t40">Why shouldn’t the next great doctor, engineer, mathematician or scholar be sitting here?</p>', 'col center', 'd3')), 'bone')
S['balance'] = (grid(
  T('plain', '1 / 13', '1 / 2', '<p class="dsp t84 green-t">KNOWLEDGE NEEDS CHARACTER</p>', 'col', 'd1'),
  T('grey', '1 / 7', '2 / 7', '<p class="body t40">Knowledge without character</p><div><p class="k">LEADS TO</p><p class="dsp t130">ARROGANCE</p></div>', 'col', 'd2'),
  T('green', '7 / 13', '2 / 7', f'{mot(260, "mot corner")}<p class="body t40">Knowledge guided by faith and humility</p><div><p class="k gold-t">BENEFITS</p><p class="dsp t130">EVERYONE</p></div>', 'col', 'd3')), 'bone')
jr = [('MADĪNAH', 'Muslims and neighbours of other faiths, under agreed rights and justice', 'green', '1 / 5', '2 / 6'), ('TRADE ROUTES', 'Ideas, navigation, citrus, rice and irrigation across Africa, Asia and Europe', 'gold', '5 / 9', '3 / 7'), ('LONDON', 'Yemeni coffee reaches the coffeehouses, the “penny universities”', 'navy', '9 / 13', '2 / 6')]
S['journey'] = (grid(
  T('plain', '1 / 9', '1 / 2', '<p class="dsp t84 green-t">FROM MADĪNAH TO LONDON</p>', 'col', 'd1'),
  *[T(c, cs, rs, f'{mot(200, "mot corner")}<p class="num-f">{i + 1}</p><div><p class="dsp t60">{n}</p><p class="body t30">{d}</p></div>', 'col end', 'd2') for i, (n, d, c, cs, rs) in enumerate(jr)]), 'bone')
S['chapter'] = (grid(
  T('gold', '1 / 7', '1 / 7', f'{mot(300, "mot corner")}<p class="k">THEIR CHAPTER</p><div><p class="dsp t84">THE ALHAMBRA<br>THE SÜLEYMANIYE</p><p class="body t32">Ibn Rushd · Ibn Khaldūn · Rūmī · Saʿdī</p></div>', 'col', 'd1'),
  T('green', '7 / 13', '1 / 7', '<p class="k gold-t">OUR CHAPTER</p><div class="lines"><div class="ln"></div><div class="ln"></div><div class="ln"></div></div><p class="dsp t84">IS OURS TO WRITE</p>', 'col', 'd2')), 'bone')
S['heritage'] = (grid(
  T('plain', '1 / 13', '1 / 2', '<p class="dsp t84 green-t">OUR HERITAGE, OUR RESPONSIBILITY</p>', 'col', 'd1'),
  *[T(c, f'{1 + 4 * i} / {5 + 4 * i}', '2 / 5', f'<p class="dsp t54">{a.upper()}</p><div><p class="k">WITHOUT</p><p class="body t32">{b}</p></div>', 'col', 'd2') for i, ((a, b), c) in enumerate(zip(COUPLETS, ['terra', 'teal', 'navy']))],
  T('green', '1 / 13', '5 / 7', f'{mot(240, "mot corner")}<p class="body t44 ital">True greatness: faith with knowledge, knowledge with character, character with service.</p>', 'center', 'd3')), 'bone')
S['six'] = (grid(
  T('plain', '1 / 13', '1 / 2', '<p class="dsp t84 green-t">THE SIX QUALITIES, TO CARRY FORWARD</p>', 'col', 'd1'),
  *[T(c, f'{1 + 2 * k} / {3 + 2 * k}', '2 / 7', f'<p class="dsp t60">{k + 1}</p><p class="kufi sx-ar">{a}</p><p class="k">{t.upper()}</p>', 'col between', 'd2') for k, ((t, a), c) in enumerate(zip(SIX, six_c))]), 'bone')
S['final'] = (grid(
  T('green', '1 / 9', '1 / 7', f'{mot(380, "mot big")}<p class="k gold-t">A FINAL THOUGHT</p><div><p class="dsp fn-t">WHAT WILL PEOPLE REMEMBER?</p><p class="body t40">Not our grades or our prizes, but how we treated them, whether we kept our word, and whether we stood up for what was right.</p></div>', 'col', 'd1'),
  T('gold', '9 / 13', '1 / 5', '<p class="body t36">Let us be a generation firm in faith, rich in knowledge, noble in character, confident in our identity and devoted to serving others.</p>', 'col', 'd2'),
  T('cream', '9 / 13', '5 / 7', '<img class="fn-cal" src="{{CALG}}" alt="Calligraphy: Maʿhad al-Imām Muḥammad Ādam al-Islāmī" style="width:520px;height:112px">', 'center', 'd3')), 'bone')
write_deck('mos-out', 'Our Identity as Young Muslims — Mosaic', S, open('mosaic.css', encoding='utf-8').read(), FACES, SECTIONS,
           {'CALG': ('__CALG_BLOB__', '../callig-green.png')}, 'mos-prev')
print('ok')
