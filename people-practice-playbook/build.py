#!/usr/bin/env python3
"""Build index.html from the playbook markdown.

The markdown file is the source of truth. This script converts it with
pandoc (GitHub-flavoured markdown, no smart punctuation, so the text is not
altered), then adds stable anchors, a table of contents, scrollable table
wrappers and the page chrome.

    python3 people-practice-playbook/build.py

Requires pandoc on PATH. When a new version is published, update SOURCE,
VERSION and DATE below, then rebuild.
"""
import html
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = 'people-practice-playbook-v0.1.1.md'
VERSION = '0.1.1'
DATE = '6 November 2026'
LICENCE_URL = 'https://creativecommons.org/licenses/by-sa/4.0/'
CREDIT = 'Specious Coda-Bishop'
REPO_URL = 'https://github.com/iamspecious/portfolio'
EMAIL = 'work.specious@gmail.com'
PAGE_URL = 'https://iamspecious.github.io/portfolio/people-practice-playbook/'
TITLE = 'People Practice Playbook, Vol. 1: Job Architecture and Levelling'
DESCRIPTION = ('An open, living playbook for anyone stuck on job levels at a 50 to 500 '
               'person company. It starts with working out which problem you actually '
               "have, and leans on research where it exists and says so where it doesn't.")


def slug(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text).lower()
    text = re.sub(r"[’']", '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text


def main():
    md_path = os.path.join(HERE, SOURCE)
    lines = open(md_path, encoding='utf-8').read().split('\n')

    # The title (line 1) and byline (line 3) become the page header; the body
    # starts at the first "## " heading.
    first_h2 = next(i for i, l in enumerate(lines) if l.startswith('## '))
    header_title = lines[0].lstrip('# ').strip()
    header_byline = next(l for l in lines[1:first_h2] if l.strip())
    body_md = '\n'.join(lines[first_h2:])

    body = subprocess.run(
        ['pandoc', '-f', 'gfm-smart', '-t', 'html5', '--wrap=none'],
        input=body_md, capture_output=True, text=True, check=True,
    ).stdout

    # Stable anchors: section-N for each numbered section, and
    # section-N-<slug> for each subheading inside it.
    toc = []
    state = {'n': None}
    seen = set()

    def heading(m):
        level, inner = m.group(1), m.group(3)
        if level == '2':
            num = re.match(r'(\d+)\.\s*(.*)', html.unescape(re.sub(r'<[^>]+>', '', inner)))
            state['n'] = num.group(1)
            hid = f'section-{state["n"]}'
            toc.append((hid, num.group(1), num.group(2)))
        else:
            hid = f'section-{state["n"]}-{slug(inner)}'
        base, k = hid, 2
        while hid in seen:
            hid = f'{base}-{k}'
            k += 1
        seen.add(hid)
        return (f'<h{level} id="{hid}">{inner}'
                f'<a class="anchor" href="#{hid}" aria-label="Link to this section">#</a>'
                f'</h{level}>')

    body = re.sub(r'<h([23])( id="[^"]*")?>(.*?)</h\1>', heading, body)

    # Tables scroll sideways on narrow screens instead of squashing.
    body = re.sub(r'<table>', '<div class="table-wrap" role="region" tabindex="0" '
                  'aria-label="Table, scrolls sideways"><table>', body)
    body = body.replace('</table>', '</table></div>')

    toc_html = '\n'.join(
        f'            <li><a href="#{hid}"><span class="toc-num">{int(n):02d}</span>'
        f'{html.escape(t)}</a></li>' for hid, n, t in toc)

    changelog_id = next((h for h in seen if h.startswith('section-10-changelog')), 'section-10')

    licence_line = (f'<a href="{LICENCE_URL}">CC BY-SA 4.0</a>. Credit: {CREDIT}. '
                    'Take it, change it and share it. Credit it and keep your version '
                    'open on the same terms.')

    page = TEMPLATE.format(
        title=html.escape(header_title),
        meta_title=html.escape(TITLE),
        description=html.escape(DESCRIPTION),
        page_url=PAGE_URL,
        byline=html.escape(header_byline),
        version=VERSION,
        date=DATE,
        source=SOURCE,
        licence_line=licence_line,
        licence_url=LICENCE_URL,
        credit=CREDIT,
        repo_url=REPO_URL,
        email=EMAIL,
        changelog_id=changelog_id,
        toc=toc_html,
        body=body,
    )
    out = os.path.join(HERE, 'index.html')
    open(out, 'w', encoding='utf-8').write(page)

    if '—' in page:
        sys.exit('Em dash found in the built page. Remove it before publishing.')
    print(f'Wrote {out}: {len(toc)} sections, {len(seen)} anchors')


TEMPLATE = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title} · Specious Coda-Bishop</title>
    <meta name="description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Specious Coda Bishop, Portfolio">
    <meta property="og:title" content="{meta_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{page_url}">
    <meta name="twitter:card" content="summary">
    <link rel="license" href="{licence_url}">
    <!-- Built from {source} by build.py. Edit the markdown, then rebuild. -->
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html {{ scroll-behavior: smooth; }}
        body {{
            background: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.7;
            font-size: 15px;
        }}
        a {{ color: #b392f0; }}
        a:hover {{ color: #d2b3ff; }}
        .doc-container {{ max-width: 860px; margin: 0 auto; padding: 40px 24px 80px; }}

        .back-link {{
            color: #b392f0; text-decoration: none; font-size: 0.82rem;
            display: inline-flex; align-items: center; gap: 6px; margin-bottom: 40px;
        }}

        .doc-header {{ border-bottom: 2px solid #30363d; padding-bottom: 28px; margin-bottom: 28px; }}
        .doc-label {{
            font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.12em; color: #b392f0; margin-bottom: 10px; display: block;
        }}
        .doc-title {{ font-size: 1.75rem; font-weight: 700; color: #e6edf3; line-height: 1.3; margin-bottom: 6px; }}
        .doc-subtitle {{ font-size: 0.92rem; color: #8b949e; margin-bottom: 4px; }}
        .doc-version {{ font-size: 0.82rem; color: #8b949e; }}
        .doc-version a {{ text-decoration: none; }}

        .licence-box {{
            background: #161b22; border: 1px solid #30363d; border-left: 4px solid #b392f0;
            border-radius: 0 6px 6px 0; padding: 18px 22px; margin-bottom: 32px;
        }}
        .licence-box .note-label {{
            font-size: 0.63rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.1em; color: #b392f0; margin-bottom: 8px; display: block;
        }}
        .licence-box p {{ font-size: 0.88rem; line-height: 1.7; margin-bottom: 10px; }}
        .licence-box p:last-child {{ margin-bottom: 0; }}
        .download {{
            display: inline-block; background: #6e40c9; color: #fff; font-weight: 700;
            font-size: 0.82rem; text-decoration: none; padding: 8px 14px; border-radius: 5px;
        }}
        .download:hover {{ background: #8957e5; color: #fff; }}

        .toc {{
            background: #161b22; border: 1px solid #30363d; border-radius: 6px;
            padding: 20px 24px; margin-bottom: 52px;
        }}
        .toc-label {{
            font-size: 0.63rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.1em; color: #8b949e; margin-bottom: 12px; display: block;
        }}
        .toc ol {{ list-style: none; }}
        .toc li {{ border-bottom: 1px solid #21262d; }}
        .toc li:last-child {{ border-bottom: none; }}
        .toc a {{ display: flex; gap: 14px; padding: 8px 0; color: #e6edf3; text-decoration: none; font-size: 0.9rem; }}
        .toc a:hover {{ color: #b392f0; }}
        .toc-num {{ font-family: 'Consolas', monospace; color: #b392f0; font-weight: 700; flex-shrink: 0; }}

        .doc-body h2 {{
            font-size: 1.2rem; font-weight: 700; color: #e6edf3; line-height: 1.35;
            border-bottom: 2px solid #30363d; padding-bottom: 10px;
            margin: 64px 0 20px; scroll-margin-top: 20px;
        }}
        .doc-body h2:first-child {{ margin-top: 0; }}
        .doc-body h3 {{
            font-size: 0.82rem; font-weight: 700; color: #b392f0; text-transform: uppercase;
            letter-spacing: 0.08em; margin: 36px 0 14px; scroll-margin-top: 20px;
        }}
        .doc-body .anchor {{
            margin-left: 8px; color: #484f58; text-decoration: none; font-weight: 400;
            opacity: 0; transition: opacity 0.15s;
        }}
        .doc-body h2:hover .anchor, .doc-body h3:hover .anchor,
        .doc-body .anchor:focus {{ opacity: 1; }}
        .doc-body p, .doc-body li {{ font-size: 0.92rem; color: #c9d1d9; line-height: 1.75; }}
        .doc-body p {{ margin-bottom: 14px; }}
        .doc-body ul, .doc-body ol {{ padding-left: 22px; margin: 10px 0 20px; }}
        .doc-body li {{ margin-bottom: 8px; padding-left: 4px; }}
        .doc-body strong {{ color: #e6edf3; }}
        .doc-body em {{ color: #8b949e; }}
        .doc-body a {{ overflow-wrap: anywhere; }}

        .table-wrap {{
            overflow-x: auto; -webkit-overflow-scrolling: touch;
            margin: 14px 0 24px; border: 1px solid #30363d; border-radius: 6px;
        }}
        .table-wrap:focus {{ outline: 2px solid #b392f0; outline-offset: 2px; }}
        .table-wrap table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .table-wrap th {{
            background: #161b22; color: #e6edf3; font-weight: 700; font-size: 0.72rem;
            text-transform: uppercase; letter-spacing: 0.06em; padding: 10px 14px;
            text-align: left; border-bottom: 1px solid #30363d; vertical-align: bottom;
        }}
        .table-wrap td {{
            padding: 10px 14px; border-bottom: 1px solid #21262d; color: #c9d1d9;
            vertical-align: top; line-height: 1.6;
        }}
        .table-wrap tr:last-child td {{ border-bottom: none; }}
        .table-wrap tbody tr:nth-child(even) td {{ background: #0f1318; }}
        .table-wrap td a {{ overflow-wrap: normal; }}

        .doc-footer {{
            border-top: 1px solid #30363d; margin-top: 64px; padding-top: 28px;
        }}
        .doc-footer .links {{ font-size: 0.82rem; color: #8b949e; margin-top: 18px; }}
        .doc-footer .links a {{ text-decoration: none; }}

        @media (max-width: 600px) {{
            .doc-container {{ padding: 28px 16px 64px; }}
            .doc-title {{ font-size: 1.35rem; }}
            /* Columns keep a readable width; the wrapper scrolls instead. */
            .table-wrap table {{ min-width: 560px; }}
            .table-wrap th, .table-wrap td {{ min-width: 160px; }}
            .doc-body .anchor {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
<div class="doc-container">
    <a class="back-link" href="../index.html#doc-people-practice-playbook">&larr; Back to Portfolio</a>

    <header class="doc-header">
        <span class="doc-label">People Practice · Job Architecture · CC BY-SA 4.0</span>
        <h1 class="doc-title">{title}</h1>
        <p class="doc-subtitle">{byline}</p>
        <p class="doc-version"><a href="#{changelog_id}">Changelog and version history</a> in section 10</p>
    </header>

    <div class="licence-box">
        <span class="note-label">Licence</span>
        <p>{licence_line}</p>
        <p><a class="download" href="{source}" download>Download the markdown (v{version})</a></p>
    </div>

    <nav class="toc" aria-label="Contents">
        <span class="toc-label">Contents</span>
        <ol>
{toc}
        </ol>
    </nav>

    <main class="doc-body">
{body}
    </main>

    <footer class="doc-footer">
        <div class="licence-box">
            <span class="note-label">Licence</span>
            <p>{licence_line}</p>
            <p><a class="download" href="{source}" download>Download the markdown (v{version})</a></p>
        </div>
        <p class="links">{credit} · <a href="{repo_url}">Suggest a correction on GitHub</a> · <a href="mailto:{email}">{email}</a> · <a href="../index.html#doc-people-practice-playbook">Back to portfolio</a></p>
    </footer>
</div>
</body>
</html>
'''

if __name__ == '__main__':
    main()
