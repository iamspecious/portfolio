/* portfolio-search.js — Portfolio Search
   Additive / progressive enhancement. Client-side full-text search over
   portfolio-index.json — the same tagged index Digital Spec queries for
   its routes. A query matches a title, tag (including a short
   hand-maintained synonym list), or summary substring, or it doesn't —
   still no AI, no semantic matching. The one fuzzy step is a plain
   edit-distance "did you mean" offered only after a real search comes
   back empty, and only against our own content (see suggestCorrection).
   If this script errors or is removed, the underlying portfolio is
   unaffected — the search bar just doesn't render.
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

    // Hard cap on query length. This is defensive, not functional: nothing
    // legitimate anyone types needs 80+ characters, and it bounds the cost
    // of the fuzzy-match fallback below against a pasted wall of text.
    // See the security devlog entries for the full reasoning.
    var MAX_QUERY_LEN = 80;
    // Fuzzy correction only runs on words in this length range — long
    // enough that a couple of typos are unambiguous, short enough that the
    // Levenshtein pass against the vocabulary stays cheap.
    var MIN_FUZZY_LEN = 4;
    var MAX_FUZZY_LEN = 24;

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
        'csm': ['customer-support', 'support-ops']
    };

    var searchableItems = [];
    var vocabulary = [];
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
            vocabulary = buildVocabulary(searchableItems);
            boot();
        })
        .catch(function (err) {
            if (typeof console !== 'undefined') {
                console.warn('[portfolio-search] failed to load index:', err);
            }
        });

    // ─── Index prep ─────────────────────────────────────────────────────
    function buildSearchable(item) {
        var tags = []
            .concat(item.domains || [])
            .concat(item.evidence || [])
            .concat(item.tools || [])
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
            tagsLc: tags,
            haystack: [titleLc, summaryLc, tags].join(' ')
        };
    }

    // Real words drawn from our own content only (titles, summaries, and
    // tags with their hyphens opened up) — never from anything a visitor
    // types. This is what "did you mean" corrections are drawn from.
    function buildVocabulary(entries) {
        var seen = {};
        entries.forEach(function (e) {
            var text = e.titleLc + ' ' + e.summaryLc + ' ' + e.tagsLc.replace(/-/g, ' ');
            var words = text.match(/[a-z0-9]+/g) || [];
            words.forEach(function (w) {
                if (w.length >= MIN_FUZZY_LEN) seen[w] = true;
            });
        });
        return Object.keys(seen);
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
        input.maxLength = MAX_QUERY_LEN;

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
            // Belt and braces alongside the maxlength attribute: maxlength
            // covers typing and most paste paths, but not a value set
            // programmatically or dropped in via IME/autofill in a way a
            // given browser doesn't clip. Truncate here too so nothing
            // downstream ever sees more than MAX_QUERY_LEN characters.
            if (input.value.length > MAX_QUERY_LEN) {
                input.value = input.value.slice(0, MAX_QUERY_LEN);
            }
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
    // Every query word must hit somewhere for an item to qualify at all;
    // where a word hits is what decides the score — title beats a tag,
    // a tag beats the summary, and matching every word beats matching some.
    function search(query) {
        var words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
        if (!words.length) return [];

        var scored = [];
        searchableItems.forEach(function (entry) {
            var score = 0;
            var matched = 0;

            words.forEach(function (w) {
                var found = false;
                if (entry.titleLc.indexOf(w) !== -1) { score += 10; found = true; }
                if (entry.tagsLc.indexOf(w) !== -1) { score += 6; found = true; }
                var synonyms = TAG_SYNONYMS[w];
                if (synonyms && synonyms.some(function (t) { return entry.tagsLc.indexOf(t) !== -1; })) {
                    score += 5; found = true;
                }
                if (entry.summaryLc.indexOf(w) !== -1) { score += 4; found = true; }
                if (!found && entry.haystack.indexOf(w) !== -1) { score += 1; found = true; }
                if (found) matched++;
            });

            if (matched > 0) {
                if (matched === words.length) score += 5 * words.length;
                scored.push({ item: entry.item, score: score, matched: matched });
            }
        });

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
        lastQuery = String(rawQuery).slice(0, MAX_QUERY_LEN).trim();
        if (!lastQuery) {
            closePanel();
            return;
        }
        var words = lastQuery.toLowerCase().split(/\s+/).filter(Boolean);
        renderResults(search(lastQuery), words);
    }

    // ─── "Did you mean" — plain edit-distance, no AI ───────────────────
    // Classic Levenshtein distance (insert/delete/substitute), single-row
    // dynamic programming. Only ever called against our own vocabulary
    // words, and only after a real search has already come back empty.
    function levenshtein(a, b) {
        var m = a.length, n = b.length;
        if (m === 0) return n;
        if (n === 0) return m;

        var prev = new Array(n + 1);
        var curr = new Array(n + 1);
        var i, j;
        for (j = 0; j <= n; j++) prev[j] = j;

        for (i = 1; i <= m; i++) {
            curr[0] = i;
            for (j = 1; j <= n; j++) {
                var cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
                curr[j] = Math.min(
                    prev[j] + 1,        // deletion
                    curr[j - 1] + 1,    // insertion
                    prev[j - 1] + cost  // substitution
                );
            }
            var tmp = prev; prev = curr; curr = tmp;
        }
        return prev[n];
    }

    // Tolerance scales with word length: a one-character slip in a short
    // word changes it more than the same slip in a long one, so a fixed
    // threshold either misses "pothog" or wrongly "corrects" real short
    // words. Matches the "a few characters of difference" the tolerance
    // was scoped to.
    function maxEditDistance(len) {
        if (len <= 4) return 1;
        if (len <= 8) return 2;
        return 3;
    }

    // Tries to correct each word of a failed query against the vocabulary.
    // Returns a corrected query string, or null if nothing in range was
    // found (which is the case that falls through to a plain "no results").
    function suggestCorrection(query) {
        var words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
        var corrected = [];
        var changed = false;

        words.forEach(function (w) {
            if (w.length < MIN_FUZZY_LEN || w.length > MAX_FUZZY_LEN) {
                corrected.push(w);
                return;
            }
            var maxD = maxEditDistance(w.length);
            var bestWord = null;
            var bestDist = Infinity;

            for (var i = 0; i < vocabulary.length; i++) {
                var candidate = vocabulary[i];
                if (candidate === w) { bestWord = null; bestDist = 0; break; }
                if (Math.abs(candidate.length - w.length) > maxD) continue;
                var d = levenshtein(w, candidate);
                if (d < bestDist) { bestDist = d; bestWord = candidate; }
            }

            if (bestWord && bestDist > 0 && bestDist <= maxD) {
                corrected.push(bestWord);
                changed = true;
            } else {
                corrected.push(w);
            }
        });

        return changed ? corrected.join(' ') : null;
    }

    // ─── Rendering ──────────────────────────────────────────────────────
    function renderResults(results, words) {
        panel.innerHTML = '';
        resultEls = [];
        activeIndex = -1;

        if (!results.length) {
            renderEmptyState();
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

        GROUP_ORDER.forEach(function (type) {
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

    function renderEmptyState() {
        var empty = document.createElement('div');
        empty.className = 'pfs-empty';

        var msg = document.createElement('p');
        msg.className = 'pfs-empty-msg';
        msg.textContent = 'No matches for “' + lastQuery + '”.';
        empty.appendChild(msg);

        var suggestion = suggestCorrection(lastQuery);

        if (suggestion && suggestion !== lastQuery.toLowerCase()) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'pfs-suggest';
            btn.innerHTML = 'Did you mean <strong>' + escapeHtml(suggestion) + '</strong>?';
            btn.addEventListener('click', function () {
                input.value = suggestion;
                runSearch(suggestion);
            });
            empty.appendChild(btn);
        } else {
            var hint = document.createElement('p');
            hint.className = 'pfs-empty-hint';
            hint.textContent = 'Try a tool (PostHog, Zendesk), a discipline (writing, HR, ops), or a project name.';
            empty.appendChild(hint);
        }

        panel.appendChild(empty);
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

    function highlight(text, words) {
        var escaped = escapeHtml(text || '');
        if (!words.length) return escaped;
        var pattern = words
            .slice()
            .sort(function (a, b) { return b.length - a.length; })
            .map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); })
            .join('|');
        if (!pattern) return escaped;
        return escaped.replace(new RegExp('(' + pattern + ')', 'ig'), '<mark class="pfs-mark">$1</mark>');
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
            target.classList.add('pfs-highlight');
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            setTimeout(function () { target.classList.remove('pfs-highlight'); }, 2200);
        }, needsTabSwitch ? 80 : 0);

        input.blur();
    }
})();
