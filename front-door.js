/* front-door.js — Digital Spec front-door overlay
   Additive / progressive enhancement. If this script errors or is
   removed, the underlying portfolio is unaffected.
*/
(function () {
  'use strict';

  var config, portfolioIndex, lanesData;
  var nodeStack = [];
  var currentNodeId = null;

  // ─── Session state keys ──────────────────────────────────────────────
  var SS_STATE = 'fd-state';   // 'open' | 'collapsed'
  var SS_NODE  = 'fd-node';    // last node id

  Promise.all([
    fetch('front-door-config.json').then(function (r) { return r.json(); }),
    fetch('portfolio-index.json').then(function (r) { return r.json(); }),
    fetch('lanes.json').then(function (r) { return r.json(); })
  ]).then(function (results) {
    config        = results[0];
    portfolioIndex = results[1];
    lanesData     = results[2];
    boot();
  }).catch(function (err) {
    if (typeof console !== 'undefined') {
      console.warn('[front-door] failed to load:', err);
    }
  });

  // ─── Boot ─────────────────────────────────────────────────────────────
  function boot() {
    var savedState = sessionStorage.getItem(SS_STATE);
    var savedNode  = sessionStorage.getItem(SS_NODE);

    // Restore current node from session, or default to startNode
    currentNodeId = savedNode || config.startNode;

    buildDOM();

    if (savedState === 'collapsed') {
      // Stay collapsed — show docked tab only
      collapseInstant();
    } else {
      // First visit OR was open — expand (with entrance transition)
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          expand();
        });
      });
    }
  }

  // ─── DOM construction ─────────────────────────────────────────────────
  function buildDOM() {
    // ── Overlay (starts in collapsed/hidden state) ──
    var overlay = document.createElement('div');
    overlay.id = 'fd-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Digital Spec — portfolio guide');
    overlay.setAttribute('aria-hidden', 'true');
    overlay.classList.add('fd-collapsed');

    overlay.innerHTML =
      '<div id="fd-backdrop"></div>' +
      '<div id="fd-panel">' +
        '<div id="fd-header">' +
          '<div id="fd-brand">' +
            '<span id="fd-avatar" aria-hidden="true">dS</span>' +
            '<span id="fd-speaker-name">Digital Spec</span>' +
          '</div>' +
          '<div id="fd-persistent">' +
            '<button class="fd-persistent-btn fd-skip-btn" type="button">Skip to everything</button>' +
            '<button class="fd-persistent-btn fd-contact-btn" type="button">Talk to Spec</button>' +
            '<button class="fd-minimize-btn" type="button" aria-label="Minimise Digital Spec" title="Minimise">&#8722;</button>' +
          '</div>' +
        '</div>' +
        '<div id="fd-scroll">' +
          '<div id="fd-dialogue" role="log" aria-live="polite" aria-atomic="false"></div>' +
          '<div id="fd-interaction"></div>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    // ── Docked tab (hidden while overlay is expanded) ──
    var tab = document.createElement('button');
    tab.id = 'fd-tab';
    tab.type = 'button';
    tab.setAttribute('aria-label', 'Ask Digital Spec — open chat guide');
    tab.setAttribute('aria-hidden', 'true');
    tab.setAttribute('tabindex', '-1');
    tab.innerHTML =
      '<span id="fd-tab-avatar" aria-hidden="true">dS</span>' +
      '<span id="fd-tab-label">Ask Digital Spec</span>';
    document.body.appendChild(tab);

    // ── Events ──
    document.getElementById('fd-backdrop').addEventListener('click', collapse);
    overlay.addEventListener('keydown', handleKeydown);
    overlay.querySelector('.fd-skip-btn').addEventListener('click', collapse);
    overlay.querySelector('.fd-contact-btn').addEventListener('click', function () {
      goToNode('contact');
    });
    overlay.querySelector('.fd-minimize-btn').addEventListener('click', collapse);
    tab.addEventListener('click', expand);
  }

  // ─── Collapse / Expand ────────────────────────────────────────────────
  function collapse() {
    var overlay = document.getElementById('fd-overlay');
    var tab     = document.getElementById('fd-tab');

    if (currentNodeId) sessionStorage.setItem(SS_NODE, currentNodeId);
    sessionStorage.setItem(SS_STATE, 'collapsed');

    overlay.classList.add('fd-collapsed');
    overlay.setAttribute('aria-hidden', 'true');

    tab.classList.add('fd-tab-visible');
    tab.setAttribute('aria-hidden', 'false');
    tab.setAttribute('tabindex', '0');
    tab.focus();
  }

  function collapseInstant() {
    // Used on page load when already collapsed — no transition needed
    var overlay = document.getElementById('fd-overlay');
    var tab     = document.getElementById('fd-tab');
    overlay.classList.add('fd-collapsed', 'fd-no-transition');
    overlay.setAttribute('aria-hidden', 'true');
    tab.classList.add('fd-tab-visible', 'fd-no-transition');
    tab.setAttribute('aria-hidden', 'false');
    tab.setAttribute('tabindex', '0');
    // Remove no-transition flag after paint so future transitions work
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        overlay.classList.remove('fd-no-transition');
        tab.classList.remove('fd-no-transition');
      });
    });
  }

  function expand() {
    var overlay = document.getElementById('fd-overlay');
    var tab     = document.getElementById('fd-tab');

    sessionStorage.setItem(SS_STATE, 'open');

    overlay.classList.remove('fd-collapsed');
    overlay.setAttribute('aria-hidden', 'false');

    tab.classList.remove('fd-tab-visible');
    tab.setAttribute('aria-hidden', 'true');
    tab.setAttribute('tabindex', '-1');

    // If dialogue is empty (page reload or first ever open), render current node
    var dialogue = document.getElementById('fd-dialogue');
    if (!dialogue.hasChildNodes()) {
      nodeStack = [];
      goToNode(currentNodeId || config.startNode);
    } else {
      // DOM intact — just restore focus to the first interactive element
      var focusTarget =
        overlay.querySelector('#fd-interaction button:not([disabled])') ||
        overlay.querySelector('#fd-interaction [tabindex="0"]') ||
        overlay.querySelector('button:not([disabled])');
      if (focusTarget) focusTarget.focus();
    }
  }

  // ─── Node navigation ──────────────────────────────────────────────────
  function goToNode(nodeId) {
    var node = config.nodes[nodeId];
    if (!node) {
      if (typeof console !== 'undefined') console.warn('[front-door] unknown node:', nodeId);
      return;
    }
    currentNodeId = nodeId;
    sessionStorage.setItem(SS_NODE, nodeId);
    nodeStack.push(nodeId);
    appendSpecBubble(node.text);
    renderOptions(node.options);
    scrollBottom();
  }

  function appendSpecBubble(text) {
    var bubble = document.createElement('div');
    bubble.className = 'fd-bubble fd-bubble-spec';
    bubble.textContent = text;
    document.getElementById('fd-dialogue').appendChild(bubble);
  }

  function appendUserBubble(text) {
    var bubble = document.createElement('div');
    bubble.className = 'fd-bubble fd-bubble-user';
    bubble.setAttribute('aria-label', 'You chose: ' + text);
    bubble.textContent = text;
    document.getElementById('fd-dialogue').appendChild(bubble);
  }

  function renderOptions(options) {
    var zone = document.getElementById('fd-interaction');
    zone.innerHTML = '';

    var group = document.createElement('div');
    group.className = 'fd-options';
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Choose a response');

    options.forEach(function (opt) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'fd-option';
      btn.textContent = opt.label;
      btn.addEventListener('click', function () { handleOption(opt, group); });
      group.appendChild(btn);
    });

    zone.appendChild(group);

    var first = group.querySelector('button');
    if (first) first.focus();
  }

  // ─── Option dispatch ──────────────────────────────────────────────────
  function handleOption(opt, group) {
    var btns = group.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) { btns[i].disabled = true; }

    appendUserBubble(opt.label);

    if (opt.target) {
      goToNode(opt.target);
    } else if (opt.lane) {
      showLane(opt.lane);
    } else if (opt.action === 'skip') {
      collapse();
    } else if (opt.action === 'goto-about') {
      collapse();
      if (typeof switchToTab === 'function') switchToTab('about-tab');
    } else if (opt.action === 'contact-email') {
      collapse();
      window.location.href = 'mailto:' + config.contacts.email;
    } else if (opt.action === 'contact-linkedin') {
      collapse();
      window.open(config.contacts.linkedin, '_blank', 'noopener,noreferrer');
    } else if (opt.action === 'deeplink') {
      collapse();
      doDeepLink(opt.tab, opt.anchor);
    }
  }

  // ─── Lane results ─────────────────────────────────────────────────────
  function showLane(laneId) {
    var lane = lanesData[laneId];
    if (!lane) { collapse(); return; }

    var items = queryLane(laneId);
    var fromNodeId = nodeStack[nodeStack.length - 1];

    if (items.length === 0) {
      appendSpecBubble('Still being curated — but everything\'s here. Have a look around.');
      var zone = document.getElementById('fd-interaction');
      zone.innerHTML = '';
      var fb = document.createElement('button');
      fb.type = 'button';
      fb.className = 'fd-option';
      fb.textContent = 'Show me everything';
      fb.addEventListener('click', collapse);
      zone.appendChild(fb);
      fb.focus();
      scrollBottom();
      return;
    }

    appendSpecBubble('Here\'s what\'s most relevant for ' + lane.label + ':');

    var zone = document.getElementById('fd-interaction');
    zone.innerHTML = '';

    var grid = document.createElement('div');
    grid.className = 'fd-cards';
    items.forEach(function (item) {
      grid.appendChild(buildCard(item, laneId));
    });
    zone.appendChild(grid);

    var controls = document.createElement('div');
    controls.className = 'fd-lane-controls';
    var back = document.createElement('button');
    back.type = 'button';
    back.className = 'fd-back-btn';
    back.textContent = '← Back';
    back.addEventListener('click', function () { goBackToNode(fromNodeId); });
    controls.appendChild(back);
    zone.appendChild(controls);

    var firstCard = grid.querySelector('[tabindex="0"]');
    if (firstCard) firstCard.focus();
    scrollBottom();
  }

  function goBackToNode(nodeId) {
    document.getElementById('fd-dialogue').innerHTML = '';
    var idx = nodeStack.lastIndexOf(nodeId);
    if (idx >= 0) nodeStack = nodeStack.slice(0, idx);
    goToNode(nodeId);
  }

  function buildCard(item, laneId) {
    var typeLabels = {
      'work':       'Work',
      'case-study': 'Case Study',
      'project':    'Project',
      'document':   'Document'
    };

    var routing = getRouting(item);
    var card = document.createElement('div');
    card.className = 'fd-card';

    var inner = document.createElement('div');
    inner.className = 'fd-card-inner';

    var badge = document.createElement('span');
    badge.className = 'fd-card-type';
    badge.textContent = typeLabels[item.type] || item.type;

    var title = document.createElement('h3');
    title.className = 'fd-card-title';
    title.textContent = item.title;

    var summary = document.createElement('p');
    summary.className = 'fd-card-summary';
    summary.textContent = item.summary;

    inner.appendChild(badge);
    inner.appendChild(title);
    inner.appendChild(summary);

    var lens = item.lensByAudience && item.lensByAudience[laneId];
    if (lens) {
      var lensEl = document.createElement('p');
      lensEl.className = 'fd-card-lens';
      lensEl.textContent = lens;
      inner.appendChild(lensEl);
    }

    card.appendChild(inner);

    if (routing) {
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.setAttribute('aria-label', 'View ' + item.title);
      var routeTab = routing.tab;
      var routeAnchor = routing.anchor;
      var go = function () {
        collapse();
        doDeepLink(routeTab, routeAnchor);
      };
      card.addEventListener('click', go);
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
      });
    }

    return card;
  }

  // ─── Lane query ───────────────────────────────────────────────────────
  function queryLane(laneId) {
    var lane          = lanesData[laneId];
    var includeDomains = lane.include.domains;
    var boostEvidence  = lane.boost.evidence;
    var max            = lane.maxItems || 8;

    var items = portfolioIndex.filter(function (item) {
      return item.domains.some(function (d) { return includeDomains.indexOf(d) >= 0; });
    });

    items = items.map(function (item) {
      var score = item.evidence.filter(function (e) {
        return boostEvidence.indexOf(e) >= 0;
      }).length;
      return { item: item, score: score };
    });

    items.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      var toKey = function (s) { return s === 'present' ? '9999-99' : (s || '0000-00'); };
      var ka = toKey(a.item.dateEnd), kb = toKey(b.item.dateEnd);
      return kb < ka ? -1 : kb > ka ? 1 : 0;
    });

    return items.slice(0, max).map(function (x) { return x.item; });
  }

  // ─── Routing ──────────────────────────────────────────────────────────
  function getRouting(item) {
    var anchor = item.anchor;
    if (!anchor) return null;

    if (anchor.charAt(0) !== '#') {
      var pa = item.pageAnchor;
      return pa ? { tab: 'projects-tab', anchor: pa } : null;
    }

    var tab;
    if (anchor.indexOf('#work-') === 0)    tab = 'work-tab';
    else if (anchor.indexOf('#cs-') === 0) tab = 'case-studies-tab';
    else                                   tab = 'projects-tab';

    return { tab: tab, anchor: anchor };
  }

  function doDeepLink(tabId, anchor) {
    if (tabId && typeof switchToTab === 'function') switchToTab(tabId);
    if (anchor) {
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      setTimeout(function () {
        var el = document.querySelector(anchor);
        if (el) el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
      }, 80);
    }
  }

  // ─── Focus trap + keyboard ─────────────────────────────────────────────
  function handleKeydown(e) {
    if (e.key === 'Escape') { collapse(); return; }
    if (e.key !== 'Tab') return;

    var overlay  = document.getElementById('fd-overlay');
    var focusable = overlay.querySelectorAll(
      'button:not([disabled]),[tabindex]:not([tabindex="-1"])'
    );
    var arr   = Array.prototype.slice.call(focusable);
    if (arr.length === 0) return;
    var first = arr[0];
    var last  = arr[arr.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus();
    }
  }

  // ─── Scroll ───────────────────────────────────────────────────────────
  function scrollBottom() {
    var scroll = document.getElementById('fd-scroll');
    if (scroll) requestAnimationFrame(function () { scroll.scrollTop = scroll.scrollHeight; });
  }

})();
