import sys, json, re, zipfile, shutil
src, out = sys.argv[1], sys.argv[2]
anim = json.load(open(src + '.anim.json'))
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
STEP = 200   # ms between groups, like the browser version
for item in zin.infolist():
    data = zin.read(item.filename)
    m = re.match(r'ppt/slides/slide(\d+)\.xml$', item.filename)
    if m:
        x = data.decode('utf-8'); si = str(int(m.group(1)) - 1)
        items = anim.get(si, [])
        ids = {nm: (int(i), kind) for kind, i, nm in re.findall(r'<p:(nvSpPr|nvPicPr)><p:cNvPr id="(\d+)" name="([^"]+)"', x)}
        tid = [2]
        def nid(): tid[0] += 1; return tid[0]
        groups = {}
        for g, nm in items:
            if nm in ids: groups.setdefault(g, []).append(nm)
        timing = ''
        if groups:
            outer = nid(); pars = []; first = True
            for gi, g in enumerate(sorted(groups)):
                eff = []
                for nm in groups[g]:
                    spid = ids[nm][0]
                    a, b, c = nid(), nid(), nid()
                    grp = ' grpId="0"'
                    eff.append(f'<p:par><p:cTn id="{a}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold"{grp} nodeType="{"afterEffect" if first else "withEffect"}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                               f'<p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
                               f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{c}" dur="600"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>')
                    first = False
                gid = nid()
                pars.append(f'<p:par><p:cTn id="{gid}" fill="hold"><p:stCondLst><p:cond delay="{gi * STEP}"/></p:stCondLst><p:childTnLst>{"".join(eff)}</p:childTnLst></p:cTn></p:par>')
            bld = ''.join(f'<p:bldP spid="{ids[nm][0]}" grpId="0" animBg="1"/>' for g in sorted(groups) for nm in groups[g] if ids[nm][1] == 'nvSpPr')
            timing = ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
                      '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
                      f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>{"".join(pars)}</p:childTnLst></p:cTn></p:par>'
                      '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
                      '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
                      f'</p:childTnLst></p:cTn></p:par></p:tnLst>{"<p:bldLst>" + bld + "</p:bldLst>" if bld else ""}</p:timing>')
        trans = '<p:transition spd="med"><p:fade/></p:transition>'
        assert '</p:clrMapOvr>' in x
        x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + trans + timing, 1)
        data = x.encode('utf-8')
    zout.writestr(item, data)
zout.close(); print('ok', out)
