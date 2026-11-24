# Group each animation step's shapes into one PowerPoint group, then fade the groups in (max 3 per slide).
import sys, re, zipfile
src, out = sys.argv[1], sys.argv[2]
EMU = re.compile(r"<a:off x=\"(-?\d+)\" y=\"(-?\d+)\"/>\s*<a:ext cx=\"(\d+)\" cy=\"(\d+)\"/>")
def process(x):
    tree_open = x.index('<p:spTree>'); tree_close = x.rindex('</p:spTree>')
    body = x[tree_open + len('<p:spTree>'):tree_close]
    m = re.search(r'</p:grpSpPr>', body); head, rest = body[:m.end()], body[m.end():]
    parts = re.findall(r'<p:(?:sp|pic|cxnSp)>.*?</p:(?:sp|pic|cxnSp)>', rest, re.S)
    assert ''.join(parts) == rest.strip() or ''.join(parts) == rest, 'unexpected tree content'
    ids = [int(i) for i in re.findall(r'<p:cNvPr id="(\d+)"', x)]; nxt = max(ids) + 1
    groups, order = {}, []
    for p in parts:
        nm = re.search(r'<p:cNvPr id="\d+" name="([^"]+)"', p).group(1)
        g = re.match(r'a(\d)_', nm); g = int(g.group(1)) if g else 0
        if g: groups.setdefault(g, []).append(p)
        order.append((g, p))
    out_parts, done, gids = [], set(), {}
    for g, p in order:
        if not g: out_parts.append(p); continue
        if g in done: continue
        done.add(g); kids = groups[g]
        boxes = [tuple(map(int, EMU.search(k).groups())) for k in kids if EMU.search(k)]
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[0] + b[2] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
        gid = nxt; nxt += 1; gids[g] = gid
        out_parts.append(f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="{gid}" name="Step {g}"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                         f'<p:grpSpPr><a:xfrm><a:off x="{x0}" y="{y0}"/><a:ext cx="{x1-x0}" cy="{y1-y0}"/><a:chOff x="{x0}" y="{y0}"/><a:chExt cx="{x1-x0}" cy="{y1-y0}"/></a:xfrm></p:grpSpPr>'
                         + ''.join(kids) + '</p:grpSp>')
    x = x[:tree_open] + '<p:spTree>' + head + ''.join(out_parts) + '</p:spTree>' + x[tree_close + len('</p:spTree>'):]
    timing = ''
    if gids:
        n = [3]
        def nid(): n[0] += 1; return n[0]
        pars = []
        for i, g in enumerate(sorted(gids)):
            a, b, c, p = nid(), nid(), nid(), nid()
            pars.append(f'<p:par><p:cTn id="{p}" fill="hold"><p:stCondLst><p:cond delay="{i * 250}"/></p:stCondLst><p:childTnLst>'
                        f'<p:par><p:cTn id="{a}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{"afterEffect" if i == 0 else "withEffect"}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                        f'<p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{gids[g]}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
                        f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{c}" dur="450"/><p:tgtEl><p:spTgt spid="{gids[g]}"/></p:tgtEl></p:cBhvr></p:animEffect>'
                        '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
        timing = ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
                  '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
                  f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>{"".join(pars)}</p:childTnLst></p:cTn></p:par>'
                  '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
                  '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
                  '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
    x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr><p:transition spd="fast"><p:fade/></p:transition>' + timing, 1)
    return x, len(gids)
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    if it.filename.endswith('/'): continue
    d = zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$', it.filename):
        s, n = process(d.decode('utf-8')); d = s.encode('utf-8'); print(it.filename, 'steps', n)
    zout.writestr(it, d)
zout.close()
