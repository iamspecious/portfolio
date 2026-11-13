#!/usr/bin/env python3
"""Put every dev log in the house style. Safe to re-run at any time.

    python3 tools/devlogs.py          # rewrite the pages in place
    python3 tools/devlogs.py --check  # report problems, change nothing (exit 1 if any)

For each <div class="devlog"> that holds entries, in each page listed in PAGES:
  - entries run newest first (entries on the same date keep their order;
    a log written oldest-first is flipped as a whole first);
  - only the newest entry shows, the rest sit in .devlog-overflow behind a
    "+ show N older entries" button;
  - dates read day month year: <time datetime="2026-11-13">13 Nov 2026</time>.
    A month-only date reads "Nov 2026" and sorts below that month's days.

DEVLOG.md files get the same treatment: newest entry first, older entries in a
collapsible <details> block (GitHub renders it as "Show N older entries"),
and dates in headings and **Date:** lines as day month year. Entries are
headed "## Entry 012 — title" (ordered by number) or "### 2026-11-13: title"
(ordered by date). New entries can go anywhere; re-run the script.

To add an entry, paste a .devlog-entry anywhere in the log with an ISO date in
its timestamp (`<span class="timestamp">2026-11-13 — what happened</span>`)
and run this script. Only the dev log blocks are rewritten; the rest of the
page is left byte for byte as it was.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'pregvoice.html']
# Every DEVLOG.md in the repo is handled too (see MARKDOWN below).
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()

TS_RE = re.compile(r'<span class="timestamp">\s*(.*?)\s*</span>', re.S)
ISO_RE = re.compile(r'^(\d{4})-(\d{2})(?:-(\d{2}))?\s*(?:[—:–-]\s*)?(.*)$', re.S)
TIME_RE = re.compile(r'^<time datetime="([\d-]+)">[^<]*</time>\s*(?:—\s*)?(.*)$', re.S)


def block_end(html, start):
    """Index just past the </div> that closes the <div ...> opening at start."""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group() == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError(f'unclosed <div> at {start}')


def child_blocks(html, cls):
    """Raw text of every <div class="cls"> in html, outermost first, in order."""
    out, pos = [], 0
    pat = re.compile(r'<div class="%s"' % re.escape(cls))
    while True:
        m = pat.search(html, pos)
        if not m:
            return out
        end = block_end(html, m.start())
        out.append(html[m.start():end])
        pos = end


def entry_date(entry):
    """(iso, display, rest) from an entry's timestamp, or None if it has no date."""
    m = TS_RE.search(entry)
    if not m:
        return None
    text = m.group(1)
    t = TIME_RE.match(text)
    if t:
        iso, rest = t.group(1), t.group(2)
    else:
        d = ISO_RE.match(text)
        if not d:
            return None
        y, mo, day, rest = d.groups()
        iso = f'{y}-{mo}' + (f'-{day}' if day else '')
    parts = iso.split('-')
    display = (f'{int(parts[2])} ' if len(parts) == 3 else '') + f'{MONTHS[int(parts[1]) - 1]} {parts[0]}'
    return iso, display, rest.strip()


def sort_key(iso):
    return iso if iso.count('-') == 2 else iso + '-00'


def restamp(entry):
    got = entry_date(entry)
    if not got:
        return entry
    iso, display, rest = got
    new = f'<span class="timestamp"><time datetime="{iso}">{display}</time>' + \
          (f' — {rest}' if rest else '') + '</span>'
    return TS_RE.sub(lambda _: new, entry, count=1)


def reindent(block, indent):
    lines = block.strip('\n').split('\n')
    # The first line was cut at '<div', so it carries no indentation of its
    # own; the block's closing </div> sits at the opening tag's level, so the
    # shallowest of the other lines gives the block's original indent.
    rest = [l for l in lines[1:] if l.strip()]
    base = min((len(l) - len(l.lstrip()) for l in rest), default=0)
    out = [indent + lines[0].strip()]
    for l in lines[1:]:
        if not l.strip():
            out.append('')
        elif len(l) - len(l.lstrip()) >= base:
            out.append(indent + l[base:])
        else:
            out.append(indent + l.lstrip())
    return '\n'.join(out)


def rebuild(block, indent):
    """Rewrite one devlog block; returns (new_block, problems found in the old one)."""
    problems = []
    open_tag = block[:block.index('>') + 1]
    inner = block[len(open_tag):]
    header = child_blocks(inner, 'devlog-header')
    entries = child_blocks(inner, 'devlog-entry')
    dates = [entry_date(e) for e in entries]
    if any(d is None for d in dates):
        problems.append('an entry has no ISO date in its timestamp; left unsorted')
        return block, problems
    isos = [d[0] for d in dates]
    keys = [sort_key(i) for i in isos]
    if keys and keys[0] < keys[-1]:
        problems.append('oldest first')
        entries, keys = entries[::-1], keys[::-1]
    order = sorted(range(len(entries)), key=lambda i: keys[i], reverse=True)
    if order != list(range(len(entries))):
        if 'oldest first' not in problems:
            problems.append('entries out of date order')
    entries = [restamp(entries[i]) for i in order]
    if any('<time ' not in TS_RE.search(e).group(1) for e in child_blocks(inner, 'devlog-entry')):
        problems.append('dates not in day-month-year form')
    visible = len(re.findall(r'<div class="devlog-entry"', inner.split('<div class="devlog-overflow"')[0]))
    if len(entries) > 1 and visible != 1:
        problems.append(f'{visible} entries showing before the drop-down (should be 1)')

    i1, i2, i3 = indent + '    ', indent + '        ', indent + '            '
    parts = [open_tag]
    for h in header:
        parts.append(reindent(h, i1))
    if entries:
        parts.append('')
        parts.append(reindent(entries[0], i1))
    older = entries[1:]
    if older:
        word = 'entry' if len(older) == 1 else 'entries'
        parts.append('')
        parts.append(f'{i1}<button class="devlog-toggle" onclick="toggleDevlog(this)">+ show {len(older)} older {word}</button>')
        parts.append('')
        parts.append(f'{i1}<div class="devlog-overflow">')
        parts.append('\n\n'.join(reindent(e, i2) for e in older))
        parts.append(f'{i1}</div>')
    parts.append(f'{indent}</div>')
    return '\n'.join(parts), problems


def process(path, write):
    html = open(path, encoding='utf-8').read()
    out, pos, report = [], 0, []
    for m in re.finditer(r'<div class="devlog"', html):
        if m.start() < pos:
            continue
        end = block_end(html, m.start())
        block = html[m.start():end]
        if '<div class="devlog-entry"' not in block:
            continue
        line_start = html.rfind('\n', 0, m.start()) + 1
        indent = html[line_start:m.start()]
        new, problems = rebuild(block, indent)
        where = re.findall(r'id="([^"]+)"', html[:m.start()])
        label = where[-1] if where else '?'
        for p in problems:
            report.append(f'{path}: {label}: {p}')
        out.append(html[pos:m.start()])
        out.append(new)
        pos = end
    out.append(html[pos:])
    new_html = ''.join(out)
    if write and new_html != html:
        open(path, 'w', encoding='utf-8').write(new_html)
    return report, new_html != html


# ─── Markdown DEVLOG.md files ─────────────────────────────────────────────
MD_ENTRY = re.compile(r'^(## Entry (\d+)\b.*|### (\d{4}-\d{2}-\d{2}|\d{1,2} [A-Z][a-z]{2} \d{4})\b.*)$', re.M)
MD_ISO = re.compile(r'(?<![\w/.-])(\d{4})-(\d{2})-(\d{2})(?![\w/-])')
DETAILS_OPEN = re.compile(r'\n*<details>\s*\n<summary>Show \d+ older entr(?:y|ies)</summary>\s*\n', re.M)
DETAILS_CLOSE = re.compile(r'\n*</details>\s*\n?', re.M)


def euro(iso_match):
    y, m, d = iso_match.groups()
    return f'{int(d)} {MONTHS[int(m) - 1]} {y}'


def md_date_key(heading):
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', heading)
    if m:
        return '-'.join(m.groups())
    m = re.search(r'(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})', heading)
    return f'{m.group(3)}-{MONTHS.index(m.group(2)) + 1:02d}-{int(m.group(1)):02d}'


def process_markdown(path, write):
    text = open(path, encoding='utf-8').read()
    problems = []
    body = DETAILS_CLOSE.sub('\n', DETAILS_OPEN.sub('\n', text))
    heads = list(MD_ENTRY.finditer(body))
    if len(heads) < 2:
        return problems, False
    preamble = body[:heads[0].start()].rstrip()
    chunks = [body[h.start():(heads[i + 1].start() if i + 1 < len(heads) else len(body))]
              for i, h in enumerate(heads)]
    uses_rules = bool(re.search(r'\n---\s*$', preamble)) or any(re.search(r'\n---\s*$', c) for c in chunks[:-1])
    # A closing note after the last entry (after its final ---) stays at the bottom.
    footer = ''
    last = chunks[-1]
    cut = last.rfind('\n---\n')
    if uses_rules and cut != -1 and '\n#' not in last[cut:]:
        footer, chunks[-1] = last[cut + 5:].strip(), last[:cut]
    chunks = [re.sub(r'(\s*\n---\s*)+$', '', c.rstrip()).rstrip() for c in chunks]
    if preamble.endswith('---'):
        preamble = preamble[:-3].rstrip()

    numbered = [h.group(2) for h in heads]
    if all(numbered):
        keys = [int(n) for n in numbered]
    else:
        keys = [md_date_key(h.group(0)) for h in heads]
        if keys[0] < keys[-1]:
            problems.append('oldest first')
            chunks, keys = chunks[::-1], keys[::-1]
    order = sorted(range(len(chunks)), key=lambda i: keys[i], reverse=True)
    if 'oldest first' not in problems and order != list(range(len(chunks))):
        problems.append('oldest first' if keys[0] < keys[-1] else 'entries out of order')
    chunks = [chunks[i] for i in order]
    if MD_ISO.search(text):
        problems.append('dates not in day-month-year form')
    if '<details>' not in text:
        problems.append(f'{len(chunks) - 1} older ' + ('entry' if len(chunks) == 2 else 'entries') + ' not collapsed')
    chunks = [MD_ISO.sub(euro, c) for c in chunks]

    sep = '\n\n---\n\n' if uses_rules else '\n\n'
    n = len(chunks) - 1
    word = 'entry' if n == 1 else 'entries'
    out = preamble + sep + chunks[0] + '\n\n' + \
        f'<details>\n<summary>Show {n} older {word}</summary>\n\n' + \
        sep.join(chunks[1:]) + '\n\n</details>\n'
    if footer:
        out += '\n---\n\n' + footer + '\n'
    changed = out != text
    if write and changed:
        open(path, 'w', encoding='utf-8').write(out)
    return problems, changed


def markdown_logs():
    found = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        if 'DEVLOG.md' in files:
            found.append(os.path.relpath(os.path.join(dirpath, 'DEVLOG.md'), ROOT))
    return sorted(found)


def main():
    check = '--check' in sys.argv
    os.chdir(ROOT)
    problems, changed = [], []
    for page in PAGES:
        rep, did = process(page, write=not check)
        problems += rep
        if did:
            changed.append(page)
    for md in markdown_logs():
        rep, did = process_markdown(md, write=not check)
        problems += [f'{md}: {p}' for p in rep]
        if did:
            changed.append(md)
    for p in problems:
        print(('FAIL ' if check else 'fixed ') + p)
    if not check:
        print('rewrote: ' + (', '.join(changed) or 'nothing (already in house style)'))
    sys.exit(1 if check and problems else 0)


if __name__ == '__main__':
    main()
