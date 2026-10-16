#!/usr/bin/env python3
"""Portfolio audit — repeatable structural checks.

Run from the repo root:  python3 tools/audit.py
Exit code is 1 if any FAIL is found, 0 otherwise (WARN does not fail).

Checks, in order:
  1. Index schema + controlled vocabulary (portfolio-index.json vs TAXONOMY.md)
  2. Index <-> HTML anchors (every item resolves; every block is indexed)
  3. Projects tab blocks (data-date, data-category, filter coverage)
  4. Digital Spec config (nodes, lanes, deep links, find-project ids)
  5. Digital Spec lane simulation (what each lane shows / hides)
  6. Portfolio Search lexicon (expected queries per item, see tools/search-lexicon.json)
  7. Local links + assets referenced from index.html
  8. README project tables vs the Projects tab

Requires: Python 3.8+, beautifulsoup4.
"""
import json
import os
import re
import sys
from collections import defaultdict

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

fails, warns = [], []


def fail(section, msg):
    for (sec, iid), why in KNOWN_EXCEPTIONS.items():
        if sec == section and msg.startswith(iid + ':'):
            warns.append((section, f'{msg}  [accepted: {why}]'))
            return
    fails.append((section, msg))


def warn(section, msg):
    warns.append((section, msg))


def heading(t):
    print('\n' + '=' * 72 + '\n' + t + '\n' + '=' * 72)


# ─── Load ───────────────────────────────────────────────────────────────
index = json.load(open('portfolio-index.json'))
lanes = json.load(open('lanes.json'))
fd = json.load(open('front-door-config.json'))
taxonomy = open('TAXONOMY.md').read()
html = open('index.html').read()
soup = BeautifulSoup(html, 'html.parser')
readme = open('README.md').read()
lexicon_path = 'tools/search-lexicon.json'
lexicon = json.load(open(lexicon_path)) if os.path.exists(lexicon_path) else {}

by_id = {i['id']: i for i in index}
html_ids = {el.get('id') for el in soup.find_all(id=True)}


def taxonomy_values(section_heading):
    """Backticked values in the first column of the table under a §heading."""
    m = re.search(r'^## .*' + re.escape(section_heading) + r'.*?$(.*?)(?=^## )',
                  taxonomy, re.S | re.M)
    if not m:
        return set()
    return set(re.findall(r'^\| `([a-z0-9-]+)` \|', m.group(1), re.M))


VOCAB = {
    'type': taxonomy_values('Facet: `type`'),
    'domains': taxonomy_values('Facet: `domain`'),
    'evidence': taxonomy_values('Facet: `evidence`'),
    'status': taxonomy_values('Facet: `status`'),
    'stage': set(), 'level': set(), 'engagement': set(),
}
ctx = re.search(r'^## 5\..*?(?=^## 6\.)', taxonomy, re.S | re.M).group(0)
for sub in ('stage', 'level', 'engagement'):
    m = re.search(r'### `' + sub + r'`(.*?)(?=###|\Z)', ctx, re.S)
    VOCAB[sub] = set(re.findall(r'^\| `([a-z0-9-]+)` \|', m.group(1), re.M))
tools_line = re.search(r'Current approved values:\s*\n(.*?)\n', taxonomy).group(1)
VOCAB['tools'] = set(re.findall(r'`([a-z0-9-]+)`', tools_line))
PROPOSED_DOMAINS = set(re.findall(r'^\| `([a-z0-9-]+)` \| \*\(proposed', taxonomy, re.M))
DO_NOT_APPLY = {'security'}

# Accepted exceptions from earlier audits. Each one downgrades a FAIL to a
# WARN so it stays visible without blocking. Add a reason; remove the entry
# when the item changes.
KNOWN_EXCEPTIONS = {
    ('anti-rule', 'denim-brand-turnaround'):
        'TAGGING-AUDIT.md crossover audit: eight work streams, each domain earned by a named section (s1–s7)',
}

# ─── 1. Schema + vocabulary ─────────────────────────────────────────────
heading('1. Index schema + controlled vocabulary')
REQUIRED = ['id', 'title', 'type', 'domains', 'evidence', 'context', 'tools',
            'summary', 'anchor', 'relatedIds', 'status', 'dateStart', 'dateEnd']
seen = set()
date_re = re.compile(r'^\d{4}-(0[1-9]|1[0-2])$')
for it in index:
    iid = it.get('id', '?')
    if iid in seen:
        fail('schema', f'{iid}: duplicate id')
    seen.add(iid)
    for k in REQUIRED:
        if k not in it:
            fail('schema', f'{iid}: missing field `{k}`')
    t = it.get('type')
    if t not in VOCAB['type']:
        fail('vocab', f'{iid}: type `{t}` not in TAXONOMY')
    st = it.get('status')
    if t in ('work', 'case-study') and st is not None:
        fail('schema', f'{iid}: status must be null for {t}')
    if t in ('project', 'document') and st not in VOCAB['status']:
        fail('vocab', f'{iid}: status `{st}` not in TAXONOMY')
    doms = it.get('domains', [])
    if not 1 <= len(doms) <= 3:
        (warn if t == 'case-study' else fail)(
            'schema', f'{iid}: {len(doms)} domains (TAXONOMY says 1–3)')
    for d in doms:
        if d in DO_NOT_APPLY:
            fail('vocab', f'{iid}: domain `{d}` is marked do-not-apply')
        elif d in PROPOSED_DOMAINS:
            fail('vocab', f'{iid}: domain `{d}` is proposed, not approved')
        elif d not in VOCAB['domains']:
            fail('vocab', f'{iid}: domain `{d}` not in TAXONOMY')
    ev = it.get('evidence', [])
    if not 1 <= len(ev) <= 4:
        warn('schema', f'{iid}: {len(ev)} evidence tags (TAXONOMY says 1–4)')
    for e in ev:
        if e not in VOCAB['evidence']:
            fail('vocab', f'{iid}: evidence `{e}` not in TAXONOMY')
    for tl in it.get('tools', []):
        if tl not in VOCAB['tools']:
            fail('vocab', f'{iid}: tool `{tl}` not in TAXONOMY §6')
    c = it.get('context') or {}
    for sub in ('stage', 'level', 'engagement'):
        if c.get(sub) not in VOCAB[sub]:
            fail('vocab', f'{iid}: context.{sub} `{c.get(sub)}` not in TAXONOMY')
    if 'people-hr' in doms and ({'ai-engineering', 'frontend-dev'} & set(doms)):
        fail('anti-rule', f'{iid}: people-hr co-tagged with a build domain')
    ds, de = it.get('dateStart'), it.get('dateEnd')
    if ds and not date_re.match(ds):
        fail('dates', f'{iid}: dateStart `{ds}` not YYYY-MM')
    if de and de != 'present' and not date_re.match(de):
        fail('dates', f'{iid}: dateEnd `{de}` not YYYY-MM or "present"')
    if ds and de and de != 'present' and de < ds:
        fail('dates', f'{iid}: dateEnd before dateStart')
    if st == 'complete' and de == 'present' and 'is intended alongside status complete' not in it.get('notes', ''):
        warn('dates', f'{iid}: status complete but dateEnd "present"')
    if st in ('in-progress', 'live') and de not in ('present', None) and t == 'project':
        warn('dates', f'{iid}: status {st} but dateEnd {de}')
    for rid in it.get('relatedIds', []):
        if rid not in by_id:
            fail('relations', f'{iid}: relatedId `{rid}` does not exist')
        elif iid not in by_id[rid].get('relatedIds', []):
            warn('relations', f'{iid} -> {rid} is one-way')
    if (it.get('audiencePin') or it.get('audienceExclude')) and not it.get('notes'):
        fail('overrides', f'{iid}: override set without a `notes` rationale')
    for lane in (it.get('audiencePin') or []) + (it.get('audienceExclude') or []):
        if lane not in lanes:
            fail('overrides', f'{iid}: override names unknown lane `{lane}`')
    if not it.get('summary'):
        fail('schema', f'{iid}: empty summary')
    kw = it.get('keywords', [])
    if not isinstance(kw, list) or not all(isinstance(k, str) and k == k.lower() for k in kw):
        fail('schema', f'{iid}: keywords must be a list of lowercase strings')

used_tools = {tl for it in index for tl in it.get('tools', [])}
for tl in sorted(VOCAB['tools'] - used_tools):
    warn('vocab', f'tool `{tl}` approved in TAXONOMY but used by no item')
used_domains = {d for it in index for d in it['domains']}
for d in sorted(VOCAB['domains'] - used_domains - DO_NOT_APPLY - PROPOSED_DOMAINS):
    warn('vocab', f'domain `{d}` approved but used by no item')
print(f'{len(index)} items; vocab: {len(VOCAB["domains"])} domains, '
      f'{len(VOCAB["evidence"])} evidence, {len(VOCAB["tools"])} tools')

# ─── 2. Anchors ─────────────────────────────────────────────────────────
heading('2. Index <-> HTML anchors')
for it in index:
    a = it.get('anchor', '')
    if a.startswith('#'):
        if a[1:] not in html_ids:
            fail('anchors', f'{it["id"]}: anchor {a} not in index.html')
    else:
        if not os.path.exists(a.split('#')[0]):
            fail('anchors', f'{it["id"]}: file {a} does not exist')
        pa = it.get('pageAnchor')
        if not pa:
            fail('anchors', f'{it["id"]}: standalone anchor without pageAnchor '
                            '(Digital Spec cards would be unclickable)')
        elif pa[1:] not in html_ids:
            fail('anchors', f'{it["id"]}: pageAnchor {pa} not in index.html')
    for lane, secs in (it.get('sectionsByLane') or {}).items():
        for s in secs:
            sub = f'{a[1:]}-s{s}'
            if sub not in html_ids:
                fail('anchors', f'{it["id"]}: sectionsByLane {lane} -> #{sub} missing')

indexed_anchors = {it['anchor'].lstrip('#') for it in index} | \
                  {(it.get('pageAnchor') or '').lstrip('#') for it in index}
for el in soup.select('#projects .project, #case-studies .project, #work [id^="work-"]'):
    pid = el.get('id')
    if pid and pid not in indexed_anchors:
        fail('anchors', f'HTML #{pid} has no entry in portfolio-index.json')
for el in soup.select('#projects .project:not([id]), #case-studies .project:not([id])'):
    h = el.find(['h3', 'h4'])
    fail('anchors', f'HTML block "{h.get_text(strip=True) if h else "?"}" has no id')

# ─── 3. Projects tab blocks ─────────────────────────────────────────────
heading('3. Projects tab: blocks, dates, categories')
proj_pane = soup.find(id='projects')
filters = {b['data-filter'] for b in proj_pane.select('.project-filters .filter-btn')} - {'all'}
cat_count = defaultdict(int)
proj_rows = []
for blk in proj_pane.select('.project-block'):
    inner = blk.find(class_='project')
    pid = inner.get('id') if inner else None
    title = inner.find('h3').get_text(' ', strip=True) if inner and inner.find('h3') else '?'
    cats = (blk.get('data-category') or '').split()
    date = blk.get('data-date')
    proj_rows.append((pid, title, date, cats))
    if not date:
        fail('projects-tab', f'{pid}: no data-date (sorts as newest)')
    elif not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        fail('projects-tab', f'{pid}: data-date `{date}` not YYYY-MM-DD')
    if not cats:
        fail('projects-tab', f'{pid}: no data-category (filter JS will throw)')
    for c in cats:
        cat_count[c] += 1
        if c not in filters:
            fail('projects-tab', f'{pid}: category `{c}` has no filter button')
    it = next((i for i in index if i['anchor'] == '#' + (pid or '') or
               i.get('pageAnchor') == '#' + (pid or '')), None)
    if it and date and it.get('dateStart') and date[:7] != it['dateStart']:
        warn('projects-tab', f'{pid}: data-date {date} vs index dateStart {it["dateStart"]}')
for f in sorted(filters):
    if not cat_count[f]:
        fail('projects-tab', f'filter `{f}` matches no block')
print('filter counts:', dict(sorted(cat_count.items())))

# ─── 4. Digital Spec config ─────────────────────────────────────────────
heading('4. Digital Spec (front door) config')
nodes = fd['nodes']
if fd['startNode'] not in nodes:
    fail('front-door', f'startNode {fd["startNode"]} missing')
reachable, stack = set(), [fd['startNode'], 'contact']
lanes_used = set()
while stack:
    n = stack.pop()
    if n in reachable:
        continue
    reachable.add(n)
    for o in nodes[n]['options']:
        if 'target' in o:
            if o['target'] not in nodes:
                fail('front-door', f'node {n}: target `{o["target"]}` missing')
            else:
                stack.append(o['target'])
        if 'lane' in o:
            lanes_used.add(o['lane'])
            if o['lane'] not in lanes:
                fail('front-door', f'node {n}: lane `{o["lane"]}` not in lanes.json')
        if o.get('action') == 'find-project' and o.get('itemId') not in by_id:
            fail('front-door', f'node {n}: itemId `{o.get("itemId")}` not indexed')
        if o.get('action') == 'deeplink':
            if o['anchor'][1:] not in html_ids:
                fail('front-door', f'node {n}: deeplink {o["anchor"]} missing')
            if o.get('tab') and not soup.find(id=o['tab']):
                fail('front-door', f'node {n}: tab {o["tab"]} missing')
    targets = [(o.get('target'), o.get('lane'), o.get('anchor'), o.get('itemId'))
               for o in nodes[n]['options']]
    dupes = {t for t in targets if targets.count(t) > 1 and any(t)}
    for d in dupes:
        warn('front-door', f'node {n}: two options go to the same place {d}')
for n in nodes:
    if n not in reachable:
        warn('front-door', f'node `{n}` is unreachable')
real_lanes = {k for k in lanes if not k.startswith('_')}
for l in sorted(real_lanes - lanes_used):
    warn('front-door', f'lane `{l}` is defined but no node routes to it')
for l in sorted(real_lanes):
    if l not in fd.get('laneIntros', {}):
        warn('front-door', f'lane `{l}` has no laneIntro blurb')

# ─── 5. Lane simulation (mirrors front-door.js queryLane) ──────────────
heading('5. Digital Spec lane simulation')
ORDER = ['work', 'case-study', 'project', 'document']
gcaps = lanes.get('_bucketCaps', {})


def dkey(s):
    return '9999-99' if s == 'present' else (s or '0000-00')


def query_lane(lid):
    lane = lanes[lid]
    inc, boost = lane['include']['domains'], lane['boost']['evidence']
    caps = {t: lane.get('bucketCaps', {}).get(t, gcaps.get(t, 4)) for t in ORDER}
    m = [i for i in index if any(d in inc for d in i['domains'])
         and lid not in (i.get('audienceExclude') or [])]
    buckets = defaultdict(list)
    for i in m:
        buckets[i['type']].append((lid in (i.get('audiencePin') or []),
                                   sum(e in boost for e in i['evidence']), i))
    shown, hidden = [], []
    for t in ORDER:
        b = sorted(buckets[t], key=lambda x: (not x[0], -x[1],
                                              ''.join(chr(255 - ord(c)) for c in dkey(x[2]['dateEnd']))))
        pinned = [x for x in b if x[0]]
        rest = [x for x in b if not x[0]]
        kept = pinned + rest[:max(0, caps[t] - len(pinned))]
        for x in b:
            (shown if x in kept else hidden).append(x[2])
    cap = lane.get('maxItems')
    if cap and len(shown) > cap:
        hidden = shown[cap:] + hidden
        shown = shown[:cap]
    return shown, hidden


in_some_lane = set()
for lid in sorted(real_lanes):
    shown, hidden = query_lane(lid)
    in_some_lane |= {i['id'] for i in shown}
    print(f'\n[{lid}] shows {len(shown)}' + (' (UNREACHABLE from dialogue)' if lid not in lanes_used else ''))
    for i in shown:
        print(f'   + {i["type"]:10} {i["id"]}')
    for i in hidden:
        print(f'   - {i["type"]:10} {i["id"]}  (capped)')
for it in index:
    if it['id'] not in in_some_lane:
        warn('lanes', f'{it["id"]} ({it["type"]}, {"/".join(it["domains"])}) '
                      'is not shown in any Digital Spec lane')

# ─── 6. Search lexicon ──────────────────────────────────────────────────
heading('6. Portfolio Search lexicon')
js = open('portfolio-search.js').read()
syn_block = re.search(r'TAG_SYNONYMS = \{(.*?)\};', js, re.S).group(1)
SYN = {k: re.findall(r"'([a-z0-9-]+)'", v)
       for k, v in re.findall(r"'([a-z0-9 -]+)':\s*\[([^\]]*)\]", syn_block)}
all_tags = VOCAB['domains'] | VOCAB['evidence'] | VOCAB['tools'] | VOCAB['type'] | \
           VOCAB['stage'] | VOCAB['level'] | VOCAB['engagement']
for k, vs in SYN.items():
    for v in vs:
        if v not in all_tags:
            fail('search', f'synonym `{k}` -> `{v}` is not a real tag')


def search_ids(q):
    """Mirror of portfolio-search.js: each word must start a word somewhere."""
    words = q.lower().split()
    out = []
    for it in index:
        tags = ' '.join(it['domains'] + it['evidence'] + it['tools'] + it.get('keywords', []) + [it['type']] +
                        [it['context'][k] for k in ('stage', 'level', 'engagement')]).lower()
        hay = ' '.join([it['title'].lower(), it['summary'].lower(), tags])
        hit = 0
        for w in words:
            if re.search(r'(^|[^a-z0-9])' + re.escape(w), hay) or \
                    any(t in tags for t in SYN.get(w, [])):
                hit += 1
        if hit:
            out.append((hit == len(words), it['id']))
    return out


misses = 0
for iid, queries in lexicon.items():
    if iid.startswith('_'):
        continue
    if iid not in by_id:
        fail('search', f'lexicon names unknown id `{iid}`')
        continue
    for q in queries:
        res = search_ids(q)
        if not any(full and rid == iid for full, rid in res):
            misses += 1
            warn('search', f'"{q}" does not find {iid}')
for it in index:
    if it['type'] in ('project', 'document') and it['id'] not in lexicon:
        warn('search', f'{it["id"]}: no expected queries in {lexicon_path}')
print(f'{sum(len(v) for k, v in lexicon.items() if not k.startswith("_"))} expected queries, '
      f'{misses} miss')

# ─── 7. Local links + assets ────────────────────────────────────────────
heading('7. Local links and assets')
for tag, attr in (('a', 'href'), ('img', 'src'), ('script', 'src'), ('link', 'href')):
    for el in soup.find_all(tag):
        v = el.get(attr)
        if not v or re.match(r'^(https?:|mailto:|tel:|#|javascript:|data:)', v):
            if v and v.startswith('#') and len(v) > 1 and v[1:] not in html_ids:
                fail('links', f'in-page link {v} has no target')
            continue
        path = v.split('#')[0].split('?')[0]
        if path.startswith('./'):
            path = path[2:]
        if path.endswith('/'):
            path += 'index.html' if os.path.exists(path + 'index.html') else 'README.md'
        if not os.path.exists(path) and not os.path.exists(path + '.html'):
            fail('links', f'<{tag} {attr}="{v}"> -> missing file')
for el in soup.find_all('img'):
    if not el.get('alt'):
        warn('a11y', f'<img src="{el.get("src")}"> has no alt text')
for el in soup.find_all('a', target='_blank'):
    if 'noopener' not in (el.get('rel') or []) and 'noreferrer' not in (el.get('rel') or []):
        warn('links', f'target=_blank without rel=noopener: {el.get("href")}')
# Link previews: every page except the date-proposal experience (its title
# is part of the reveal) carries a description and Open Graph tags.
import glob
for page in sorted(glob.glob('*.html')):
    ps = BeautifulSoup(open(page).read(), 'html.parser')
    if not ps.find('meta', attrs={'name': 'description'}):
        warn('previews', f'{page}: no <meta name="description">')
    for prop in ('og:title', 'og:description', 'og:url'):
        if not ps.find('meta', attrs={'property': prop}):
            warn('previews', f'{page}: no {prop}')
    for a in ps.find_all('a', href=True):
        m = re.match(r'^index\.html#(.+)$', a['href'])
        if m and m.group(1) not in html_ids:
            fail('links', f'{page}: back link {a["href"]} has no target')
ext = sorted({el['href'] for el in soup.find_all('a', href=True) if el['href'].startswith('http')})
print(f'{len(ext)} external links (not fetched; check manually or with --external)')
if '--external' in sys.argv:
    import urllib.request
    for u in ext:
        try:
            req = urllib.request.Request(u, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            code = urllib.request.urlopen(req, timeout=15).status
        except Exception as e:
            code = getattr(e, 'code', str(e)[:60])
        if code not in (200, 301, 302):
            warn('external', f'{u} -> {code}')

# ─── 8. README vs Projects tab ──────────────────────────────────────────
heading('8. README vs Projects tab')
STOP = {'a', 'an', 'the', 'of', 'for', 'and', 'to', 'in', 'on', 'with', 'into', 'that', 'by'}


def words(s):
    return {w for w in re.findall(r'[a-z0-9]+', s.lower()) if w not in STOP}


def same(a, b):
    wa, wb = words(a), words(b)
    return bool(wa and wb) and len(wa & wb) / min(len(wa), len(wb)) >= 0.75


readme_rows = [t.strip() for t in
               re.findall(r'^\| \[?([^\]|]+?)\]?(?:\([^)]*\))? \|', readme, re.M)
               if t.strip() not in ('Project', 'Case Study', '---')]
page_titles = [t for _, t, _, _ in proj_rows] + \
              [h.get_text(' ', strip=True) for h in soup.select('#case-studies .project h3')]
for pid, title, date, cats in proj_rows:
    base = re.sub(r'\s*(In Progress|Live|Complete|Research.*|Sample|Internal Tool)$', '', title).strip()
    if 'consulting' in cats:
        continue  # README summarises consulting in prose
    if not any(same(base, r) for r in readme_rows):
        fail('readme', f'Projects tab item "{base}" ({pid}) is not in README')
for t in readme_rows:
    if not any(same(t, p) for p in page_titles):
        warn('readme', f'README row "{t}" matches nothing on the page')
n_cs = len(soup.select('#case-studies .project'))
m = re.search(r'(\w+) narrative case studies', readme)
if m and m.group(1).lower() not in ('one two three four five six seven eight nine ten'.split()[n_cs - 1:n_cs]):
    fail('readme', f'README says "{m.group(1)} narrative case studies"; page has {n_cs}')

# ─── Report ─────────────────────────────────────────────────────────────
heading(f'RESULT: {len(fails)} FAIL, {len(warns)} WARN')
for label, rows in (('FAIL', fails), ('WARN', warns)):
    for sec, msg in sorted(rows):
        print(f'{label:4} [{sec}] {msg}')
sys.exit(1 if fails else 0)
