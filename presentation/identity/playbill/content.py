import re
md = open('/home/user/skills/presentation/identity/script.md', encoding='utf-8').read()
secs = {int(n): re.sub(r'\*\*', '', b).strip() for n, b in re.findall(r'^## (\d+)\. .*?\n(.*?)(?=^## |\Z)', md, re.S | re.M)}
P = {k: [p.strip() for p in v.split('\n\n') if p.strip()] for k, v in secs.items()}
j = lambda *ps: '\n\n'.join(ps)
AIMS = {
 'faith': ['Anchor in worship', 'Understand our beliefs', 'Live the Sunnah', 'Stand firm'],
 'knowledge': ['Love all useful learning', 'Question and reflect', 'Honour our heritage'],
 'character': ['Respect everyone', 'Live with integrity', 'Choose humility', 'Control ourselves'],
 'society': ['Quiet confidence', 'Build bridges', 'Stand up for justice', 'Lead by example'],
 'service': ['Care deeply', 'Serve first', 'Solve real problems', 'Lead by serving'],
 'excellence': ['Give our best', 'Refuse to coast', 'Learn from setbacks', 'Stay grateful'],
}
Q = {
 'faith': dict(n=1, title='Strong in Faith', sub='Our Islamic identity', word='الإيمان', lead='Knowing Allah, loving His Messenger ﷺ, and living by His guidance.', foot='Never apologetic about being Muslim.', notes=secs[3]),
 'knowledge': dict(n=2, title='Seekers of Knowledge', sub='Our scholarly identity', word='العلم', ar='اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ', tr='“Read in the name of your Lord Who created.”', ref='Sūrat al-ʿAlaq: 1', foot='Knowledge is an amānah, a trust.', notes=j(P[4][0], P[4][1], P[4][-4], P[4][-3], P[4][-2], P[4][-1])),
 'character': dict(n=3, title='Noble in Character', sub='Our identity of adab and akhlāq', word='الأخلاق', ar='وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ', tr='“And indeed, you are upon an outstanding standard of character.”', ref='Sūrat al-Qalam: 4', foot='Character is how we act when nobody is watching.', notes=secs[5]),
 'society': dict(n=4, title='Confident in Society', sub='Our identity as British Muslims', word='المجتمع', lead='Being a committed Muslim and contributing to British life support each other.', foot='We don’t watch from the sidelines.', notes=j(P[6][0], *P[6][3:])),
 'service': dict(n=5, title='A Life of Service', sub='Our identity of khidmah', word='الخدمة', ar='وَأَحْسِنْ كَمَا أَحْسَنَ اللَّهُ إِلَيْكَ', tr='“And do good as Allah has done good to you.”', ref='Sūrat al-Qaṣaṣ: 77', foot='Success is the lives made better because we were here.', notes=secs[7]),
 'excellence': dict(n=6, title='Striving for Excellence', sub='Our identity of iḥsān', word='الإحسان', ar='إِنَّ اللَّهَ كَتَبَ الْإِحْسَانَ عَلَىٰ كُلِّ شَيْءٍ', tr='“Indeed, Allah has prescribed excellence in all things.”', ref='Ṣaḥīḥ Muslim', foot='None of it came from doing the minimum.', notes=j(*P[8][:-1])),
}
SIX = [('Strong in Faith', 'الإيمان'), ('Seekers of Knowledge', 'العلم'), ('Noble in Character', 'الأخلاق'), ('Confident in Society', 'المجتمع'), ('Committed to Service', 'الخدمة'), ('Striving for Excellence', 'الإحسان')]
CAB = [('Medicine', 'Ibn Sīnā · al-Zahrāwī · Jābir ibn Ḥayyān'), ('The heavens', 'ʿAbd al-Raḥmān al-Ṣūfī · Maryam al-Aṣṭurlābiyya · Ulugh Beg'), ('Numbers', 'al-Khwārizmī · al-Kindī · al-Bīrūnī'),
       ('Light', 'Ibn al-Haytham and the camera obscura'), ('The earth', 'al-Idrīsī · Ibn Baṭṭūṭa'), ('Machines', 'al-Jazarī · Taqī al-Dīn · ʿAbbās ibn Firnās')]
NUMS = [('200+', 'surgical instruments', 'al-Zahrāwī'), ('75,000', 'miles travelled', 'Ibn Baṭṭūṭa'), ('44', 'of today’s countries visited', 'Ibn Baṭṭūṭa')]
COUPLETS = [('Proud of our history', 'living in the past'), ('Confident in our beliefs', 'falling into arrogance'), ('Ambitious in our goals', 'forgetting Allah and His creation')]
ORDER = ['cover', 'question', 'grades', 'continents', 'overview', 'faith', 'knowledge', 'cabinet', 'numbers', 'room', 'balance', 'character', 'society', 'journey', 'service', 'excellence', 'chapter', 'heritage', 'six', 'final']
NOTES = {
 'cover': 'Bismillāh. Welcome everyone. Today’s talk: our identity as young Muslims.',
 'question': secs[1], 'grades': P[2][0], 'continents': P[2][1], 'overview': P[2][2],
 'cabinet': j(P[4][2], P[4][3]), 'numbers': j(P[4][2], P[4][3]), 'room': P[4][4], 'balance': P[4][-1],
 'journey': j(P[6][1], P[6][2]), 'chapter': P[8][-1], 'heritage': secs[9], 'six': secs[10], 'final': secs[11],
}
for k, q in Q.items(): NOTES[k] = q['notes']
