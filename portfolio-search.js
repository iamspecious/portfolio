/* portfolio-search.js — Portfolio Search
   Additive / progressive enhancement. Client-side full-text search over
   portfolio-index.json — the same tagged index Digital Spec queries for
   its routes. No backend, no AI, no fuzzy/semantic matching: a query
   word either starts a word in a title, tag (including a short
   hand-maintained synonym list), or summary, or it doesn't. If this script
   errors or is removed, the underlying portfolio is unaffected — the
   search bar just doesn't render.
*/
(function () {
    'use strict';

    var TYPE_LABELS = {
        work: 'Work',
        'case-study': 'Case Study',
        project: 'Project',
        document: 'Document'
    };
    var GROUP_ORDER = ['project', 'document', 'case-study', 'work'];
    var DEBOUNCE_MS = 120;

    // A query word that names a facet informally maps onto the tag values
    // that actually carry it, so "docs" finds items tagged
    // technical-writing even though the word "docs" never appears in a
    // title or summary. Substring matching still runs underneath — this
    // only widens which tags count as a hit.
    var TAG_SYNONYMS = {
        'doc': ['technical-writing'],
        'docs': ['technical-writing'],
        'documentation': ['technical-writing'],
        'ai': ['ai-engineering'],
        'hr': ['people-hr'],
        'frontend': ['frontend-dev'],
        'dev': ['frontend-dev', 'ai-engineering'],
        'pm': ['project-management'],
        'cs': ['customer-support'],
        'csm': ['customer-support', 'support-ops'],
        'mod': ['community'],
        'mods': ['community'],
        'moderator': ['community'],
        'moderators': ['community'],
        'postgres': ['sql'],
        'postgresql': ['sql'],
        'database': ['sql'],
        'databases': ['sql'],
        'db': ['sql']
    };

    var searchableItems = [];
    var wrapper, input, panel;
    var resultEls = [];
    var activeIndex = -1;
    var panelOpen = false;
    var lastQuery = '';
    var debounceTimer = null;

    fetch('portfolio-index.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            searchableItems = data.map(buildSearchable);
            boot();
        })
        .catch(function (err) {
            if (typeof console !== 'undefined') {
                console.warn('[portfolio-search] failed to load index:', err);
            }
        });

    // ─── Index prep ─────────────────────────────────────────────────────
    // `keywords` is a search-only list of extra words per item (tools named
    // on the card, common phrasings like "Kingdom Hearts"). It scores like a
    // tag but is never used for Digital Spec routing. See TAXONOMY.md §13.
    function buildSearchable(item) {
        var tags = []
            .concat(item.domains || [])
            .concat(item.evidence || [])
            .concat(item.tools || [])
            .concat(item.keywords || [])
            .concat([item.type])
            .concat(item.context ? [item.context.stage, item.context.level, item.context.engagement] : [])
            .join(' ')
            .toLowerCase();

        var titleLc = (item.title || '').toLowerCase();
        var summaryLc = (item.summary || '').toLowerCase();

        return {
            item: item,
            titleLc: titleLc,
            summaryLc: summaryLc,
            tagsLc: tags
        };
    }

    // ─── Boot: build the DOM, wire up events ───────────────────────────
    function boot() {
        var root = document.getElementById('pfs-root');
        if (!root) return;

        wrapper = document.createElement('div');
        wrapper.className = 'pfs-search';
        wrapper.setAttribute('role', 'search');

        var inputWrap = document.createElement('div');
        inputWrap.className = 'pfs-input-wrap';

        input = document.createElement('input');
        input.type = 'search';
        input.id = 'pfs-input';
        input.className = 'pfs-input';
        input.placeholder = 'Search the portfolio — try “PostHog” or “writing”';
        input.autocomplete = 'off';
        input.setAttribute('aria-label', 'Search the portfolio');
        input.setAttribute('role', 'combobox');
        input.setAttribute('aria-autocomplete', 'list');
        input.setAttribute('aria-expanded', 'false');
        input.setAttribute('aria-controls', 'pfs-panel');

        var kbd = document.createElement('kbd');
        kbd.className = 'pfs-kbd';
        kbd.textContent = '/';

        inputWrap.appendChild(input);
        inputWrap.appendChild(kbd);

        panel = document.createElement('div');
        panel.id = 'pfs-panel';
        panel.className = 'pfs-panel';
        panel.setAttribute('role', 'listbox');
        panel.setAttribute('aria-label', 'Search results');
        panel.hidden = true;

        wrapper.appendChild(inputWrap);
        wrapper.appendChild(panel);
        root.appendChild(wrapper);

        input.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () { runSearch(input.value); }, DEBOUNCE_MS);
        });

        input.addEventListener('keydown', onInputKeydown);
        input.addEventListener('focus', function () {
            if (lastQuery) runSearch(input.value);
        });

        document.addEventListener('click', function (e) {
            if (!wrapper.contains(e.target)) closePanel();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key !== '/') return;
            var active = document.activeElement;
            var tag = active && active.tagName;
            if (tag === 'INPUT' || tag === 'TEXTAREA' || (active && active.isContentEditable)) return;
            e.preventDefault();
            input.focus();
        });
    }

    // ─── Search + scoring ───────────────────────────────────────────────
    // A query word hits where some word in the text starts with it, so
    // "post" finds PostHog but "eor" doesn't find "theory". Every query
    // word must hit somewhere for an item to qualify; only if nothing
    // matches every word do partial matches show, so a typo or an extra
    // word still returns something. Where a word hits decides the score:
    // title beats a tag, a tag beats the summary.
    function wordStart(w) {
        return new RegExp('(^|[^a-z0-9])' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    }

    function search(query) {
        var words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
        if (!words.length) return [];
        var patterns = words.map(wordStart);

        var full = [];
        var partial = [];
        searchableItems.forEach(function (entry) {
            var score = 0;
            var matched = 0;

            words.forEach(function (w, i) {
                var re = patterns[i];
                var found = false;
                if (re.test(entry.titleLc)) { score += 10; found = true; }
                if (re.test(entry.tagsLc)) { score += 6; found = true; }
                var synonyms = TAG_SYNONYMS[w];
                if (synonyms && synonyms.some(function (t) { return entry.tagsLc.indexOf(t) !== -1; })) {
                    score += 5; found = true;
                }
                if (re.test(entry.summaryLc)) { score += 4; found = true; }
                if (found) matched++;
            });

            if (!matched) return;
            var hit = { item: entry.item, score: score, matched: matched };
            (matched === words.length ? full : partial).push(hit);
        });

        var scored = full.length ? full : partial;
        scored.sort(function (a, b) {
            if (b.score !== a.score) return b.score - a.score;
            if (b.matched !== a.matched) return b.matched - a.matched;
            return a.item.title.localeCompare(b.item.title);
        });

        // No cap: a broad tag (e.g. "engineering") can legitimately match a
        // dozen-plus items, and the point of the fix that added this
        // comment is that the dropdown shows all of them, not a subset
        // that forces a trip back to the tab's own filter buttons.
        return scored;
    }

    function runSearch(rawQuery) {
        lastQuery = rawQuery.trim();
        if (!lastQuery) {
            closePanel();
            return;
        }
        var words = lastQuery.toLowerCase().split(/\s+/).filter(Boolean);
        renderResults(search(lastQuery), words);
    }

    // ─── Rendering ──────────────────────────────────────────────────────
    function renderResults(results, words) {
        panel.innerHTML = '';
        resultEls = [];
        activeIndex = -1;

        if (!results.length) {
            var empty = document.createElement('div');
            empty.className = 'pfs-empty';
            empty.textContent = 'No matches for “' + lastQuery + '”. Try a tool (PostHog, Zendesk), a discipline (writing, HR, ops), or a project name.';
            panel.appendChild(empty);
            openPanel();
            return;
        }

        var byType = {};
        results.forEach(function (r) {
            (byType[r.item.type] = byType[r.item.type] || []).push(r);
        });

        var count = document.createElement('div');
        count.className = 'pfs-count';
        count.textContent = results.length + (results.length === 1 ? ' result' : ' results') + ' for “' + lastQuery + '”';
        panel.appendChild(count);

        // Groups appear in order of their best match, so a search for a
        // job title shows the Work group first rather than below every
        // project that happens to share a word. GROUP_ORDER breaks ties.
        var groupOrder = GROUP_ORDER.slice().sort(function (a, b) {
            var sa = byType[a] ? byType[a][0].score : -1;
            var sb = byType[b] ? byType[b][0].score : -1;
            return sb - sa;
        });

        groupOrder.forEach(function (type) {
            var group = byType[type];
            if (!group || !group.length) return;

            var label = document.createElement('div');
            label.className = 'pfs-group-label';
            label.textContent = (TYPE_LABELS[type] || type) + ' (' + group.length + ')';
            panel.appendChild(label);

            group.forEach(function (r) {
                var row = buildResultRow(r.item, words);
                panel.appendChild(row);
                resultEls.push(row);
            });
        });

        openPanel();
    }

    function buildResultRow(item, words) {
        var row = document.createElement('button');
        row.type = 'button';
        row.className = 'pfs-result';
        row.setAttribute('role', 'option');

        var badge = document.createElement('span');
        badge.className = 'pfs-type-badge pfs-type-' + item.type;
        badge.textContent = TYPE_LABELS[item.type] || item.type;

        var body = document.createElement('span');
        body.className = 'pfs-result-body';

        var title = document.createElement('span');
        title.className = 'pfs-result-title';
        title.innerHTML = highlight(item.title, words);

        var summary = document.createElement('span');
        summary.className = 'pfs-result-summary';
        summary.innerHTML = highlight(truncate(item.summary, 130), words);

        body.appendChild(title);
        body.appendChild(summary);
        row.appendChild(badge);
        row.appendChild(body);

        row.addEventListener('click', function () { navigate(item); });
        return row;
    }

    function truncate(s, n) {
        if (!s) return '';
        return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, '') + '…' : s;
    }

    function escapeHtml(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\'': '&#39;' }[c];
        });
    }

    // Matches are found in the raw text and each piece escaped on its own,
    // so a query like "&" can't land inside an escaped entity ("&amp;").
    function highlight(text, words) {
        text = text || '';
        if (!words.length) return escapeHtml(text);
        var pattern = words
            .slice()
            .sort(function (a, b) { return b.length - a.length; })
            .map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); })
            .join('|');
        if (!pattern) return escapeHtml(text);
        var re = new RegExp('(' + pattern + ')', 'ig');
        var out = '';
        var last = 0;
        var m;
        while ((m = re.exec(text)) !== null) {
            if (!m[0].length) { re.lastIndex++; continue; }
            out += escapeHtml(text.slice(last, m.index)) +
                '<mark class="pfs-mark">' + escapeHtml(m[0]) + '</mark>';
            last = m.index + m[0].length;
        }
        return out + escapeHtml(text.slice(last));
    }

    // ─── Panel + keyboard state ─────────────────────────────────────────
    function openPanel() {
        panel.hidden = false;
        panelOpen = true;
        input.setAttribute('aria-expanded', 'true');
    }

    function closePanel() {
        panel.hidden = true;
        panelOpen = false;
        activeIndex = -1;
        input.setAttribute('aria-expanded', 'false');
    }

    function setActive(i) {
        if (!resultEls.length) return;
        activeIndex = (i + resultEls.length) % resultEls.length;
        resultEls.forEach(function (el, idx) {
            el.classList.toggle('pfs-active', idx === activeIndex);
        });
        resultEls[activeIndex].scrollIntoView({ block: 'nearest' });
    }

    function onInputKeydown(e) {
        if (e.key === 'Escape') {
            if (panelOpen) {
                closePanel();
                e.stopPropagation();
            } else {
                input.blur();
            }
            return;
        }
        if (!panelOpen || !resultEls.length) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive(activeIndex + 1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive(activeIndex - 1);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            var el = resultEls[activeIndex >= 0 ? activeIndex : 0];
            if (el) el.click();
        }
    }

    // ─── Navigation ─────────────────────────────────────────────────────
    // Results live in three shapes: an in-page anchor inside a Bootstrap
    // tab-pane, an in-page anchor already on the visible tab, or a
    // standalone document (e.g. technical-writing-portfolio.html). Each
    // is handled on its own terms rather than forcing one code path.
    function navigate(item) {
        closePanel();
        var anchor = item.anchor || '';

        if (anchor.charAt(0) !== '#') {
            if (anchor) window.location.href = anchor;
            return;
        }

        var target;
        try {
            target = document.querySelector(anchor);
        } catch (err) {
            target = null;
        }
        if (!target) {
            if (typeof console !== 'undefined') {
                console.warn('[portfolio-search] anchor not found in page:', anchor);
            }
            return;
        }

        var pane = target.closest('.tab-pane');
        var needsTabSwitch = pane && !pane.classList.contains('active');

        if (needsTabSwitch) {
            var trigger = document.querySelector('#myTab a[href="#' + pane.id + '"]');
            if (trigger) {
                if (window.bootstrap && window.bootstrap.Tab) {
                    new window.bootstrap.Tab(trigger).show();
                } else {
                    trigger.click();
                }
            }
        }

        setTimeout(function () {
            // Class goes on before scrollIntoView, not after: pfs-highlight
            // carries the scroll-margin-top that keeps the heading clear of
            // the viewport edge, and that only takes effect if it's already
            // applied when the scroll is calculated.
            history.replaceState(null, '', anchor);
            target.classList.add('pfs-highlight');
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            setTimeout(function () { target.classList.remove('pfs-highlight'); }, 2200);
        }, needsTabSwitch ? 80 : 0);

        input.blur();
    }
})();
