// Portfolio smoke test — drives the real page in headless Chromium.
//
//   python3 -m http.server 8765 &        (from the repo root)
//   node tools/smoke-test.js [http://localhost:8765/]
//
// Checks: console/page errors, failed local requests, every Digital Spec
// lane reachable from the dialogue (and every card in it lands on a
// visible target), every index item findable by its title in Portfolio
// Search (and the result lands on its target), and every Projects-tab
// filter button. Exit code 1 on any failure.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://localhost:8765/';
const ROOT = path.join(__dirname, '..');
const index = JSON.parse(fs.readFileSync(path.join(ROOT, 'portfolio-index.json')));
const fd = JSON.parse(fs.readFileSync(path.join(ROOT, 'front-door-config.json')));

const failures = [];
const fail = (m) => { failures.push(m); console.log('FAIL ' + m); };
const ok = (m) => console.log('ok   ' + m);

// Paths through the dialogue to every lane option: [[label, ...], lane]
function lanePaths() {
  const out = [];
  const walk = (nodeId, trail, seen) => {
    if (seen.has(nodeId)) return;
    seen = new Set(seen).add(nodeId);
    for (const o of fd.nodes[nodeId].options) {
      if (o.lane) out.push({ labels: [...trail, o.label], lane: o.lane });
      if (o.target) walk(o.target, [...trail, o.label], seen);
    }
  };
  walk(fd.startNode, [], new Set());
  return out;
}

async function freshPage(browser, opts = {}) {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.errors = [];
  page.on('pageerror', (e) => page.errors.push('pageerror: ' + e.message));
  // "Failed to load resource" is reported separately (and only for local
  // files) by the requestfailed/response listeners below.
  page.on('console', (m) => {
    if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) page.errors.push('console: ' + m.text());
  });
  page.on('requestfailed', (r) => {
    if (r.url().startsWith(BASE)) page.errors.push('requestfailed: ' + r.url());
  });
  page.on('response', (r) => {
    if (r.url().startsWith(BASE) && r.status() >= 400) page.errors.push(`HTTP ${r.status()}: ${r.url()}`);
  });
  // Analytics is never loaded in tests. Bootstrap can be served from a local
  // copy (BOOTSTRAP_JS / BOOTSTRAP_CSS) when the CDN is unreachable.
  await page.route(/posthog\.com/, (route) => route.abort());
  if (process.env.BOOTSTRAP_JS) {
    await page.route(/bootstrap\.bundle\.min\.js/, (r) => r.fulfill({ path: process.env.BOOTSTRAP_JS }));
  }
  if (process.env.BOOTSTRAP_CSS) {
    await page.route(/bootstrap\.min\.css/, (r) => r.fulfill({ path: process.env.BOOTSTRAP_CSS }));
  }
  await page.goto(BASE, { waitUntil: 'networkidle' });
  return page;
}

async function targetInView(page, sel) {
  return page.evaluate((s) => {
    const el = document.querySelector(s);
    if (!el) return 'missing';
    const pane = el.closest('.tab-pane');
    if (pane && !pane.classList.contains('active')) return 'tab not active';
    const r = el.getBoundingClientRect();
    if (r.height === 0 && r.width === 0) return 'hidden (zero size)';
    const atBottom = window.scrollY >= document.documentElement.scrollHeight - window.innerHeight - 2;
    if (r.top < -5 || (r.top > window.innerHeight * 0.6 && !atBottom)) return `not scrolled to (top=${Math.round(r.top)})`;
    return 'ok';
  }, sel);
}

(async () => {
  const browser = await chromium.launch();

  // ── 1. Page load ──
  let page = await freshPage(browser);
  await page.waitForSelector('#fd-overlay:not(.fd-collapsed)', { timeout: 5000 })
    .then(() => ok('Digital Spec opens on first visit'))
    .catch(() => fail('Digital Spec overlay did not open'));
  await page.waitForSelector('.pfs-input', { timeout: 5000 })
    .then(() => ok('search bar rendered'))
    .catch(() => fail('search bar did not render'));

  // ── 2. Digital Spec lanes ──
  const laneSeen = new Set();
  for (const p of lanePaths()) {
    const key = p.labels.join(' > ');
    page = await freshPage(browser);
    await page.waitForSelector('.fd-option');
    for (const label of p.labels) {
      await page.locator('.fd-option:not([disabled])', { hasText: label }).first().click();
      await page.waitForTimeout(450);
    }
    await page.waitForTimeout(500);
    const cards = await page.$$eval('.fd-card', (cs) => cs.map((c) => ({
      title: c.querySelector('.fd-card-title').textContent,
      clickable: c.getAttribute('role') === 'button',
    })));
    if (!cards.length) { fail(`lane ${p.lane} via "${key}" shows no cards`); continue; }
    ok(`lane ${p.lane} via "${key}": ${cards.length} cards`);
    cards.filter((c) => !c.clickable).forEach((c) => fail(`lane ${p.lane}: card "${c.title}" not clickable`));
    if (laneSeen.has(p.lane)) continue;
    laneSeen.add(p.lane);
    for (let i = 0; i < cards.length; i++) {
      const pg = await freshPage(browser);
      await pg.waitForSelector('.fd-option');
      for (const label of p.labels) {
        await pg.locator('.fd-option:not([disabled])', { hasText: label }).first().click();
        await pg.waitForTimeout(450);
      }
      await pg.waitForTimeout(500);
      const item = index.find((x) => x.title === cards[i].title);
      await pg.locator('.fd-card').nth(i).click();
      await pg.waitForTimeout(1300);
      let sel = item.anchor.startsWith('#') ? item.anchor : item.pageAnchor;
      const secs = item.sectionsByLane && item.sectionsByLane[p.lane];
      if (secs && secs.length && item.anchor.startsWith('#')) sel = `${item.anchor}-s${secs[0]}`;
      const res = await targetInView(pg, sel);
      if (res !== 'ok') fail(`lane ${p.lane}: card "${cards[i].title}" -> ${sel}: ${res}`);
      pg.errors.forEach((e) => fail(`lane ${p.lane}: ${e}`));
      await pg.context().close();
    }
  }

  // ── 3. Search: every item findable by title, result lands ──
  for (const item of index) {
    const pg = await freshPage(browser, { storageState: undefined });
    await pg.evaluate(() => sessionStorage.setItem('fd-state', 'collapsed'));
    await pg.reload({ waitUntil: 'networkidle' });
    await pg.fill('.pfs-input', item.title);
    await pg.waitForTimeout(250);
    const titles = await pg.$$eval('.pfs-result-title', (els) => els.map((e) => e.textContent));
    const pos = titles.indexOf(item.title);
    if (pos === -1) { fail(`search "${item.title}" does not list the item`); await pg.context().close(); continue; }
    if (pos > 2) fail(`search by exact title ranks "${item.title}" #${pos + 1}`);
    if (item.anchor.startsWith('#')) {
      await pg.locator('.pfs-result').nth(pos).click();
      await pg.waitForTimeout(1300);
      const res = await targetInView(pg, item.anchor);
      if (res !== 'ok') fail(`search -> ${item.id} (${item.anchor}): ${res}`);
    } else {
      const [resp] = await Promise.all([
        pg.waitForNavigation({ timeout: 5000 }).catch(() => null),
        pg.locator('.pfs-result').nth(pos).click(),
      ]);
      if (!resp || resp.status() >= 400) fail(`search -> ${item.id}: standalone ${item.anchor} did not load`);
    }
    pg.errors.forEach((e) => fail(`search ${item.id}: ${e}`));
    await pg.context().close();
  }
  ok(`search checked for ${index.length} items`);

  // ── 4. Projects-tab filters ──
  page = await freshPage(browser);
  await page.evaluate(() => { sessionStorage.setItem('fd-state', 'collapsed'); });
  await page.reload({ waitUntil: 'networkidle' });
  await page.click('#projects-tab');
  await page.waitForTimeout(300);
  const filters = await page.$$eval('#projects .project-filters .filter-btn', (bs) => bs.map((b) => b.dataset.filter));
  for (const f of filters) {
    await page.click(`#projects .project-filters .filter-btn[data-filter="${f}"]`);
    const n = await page.$$eval('#projects .project-block', (bs) => bs.filter((b) => b.style.display !== 'none').length);
    if (!n) fail(`filter ${f} shows 0 blocks`); else ok(`filter ${f}: ${n} blocks`);
  }
  for (const order of ['oldest', 'newest']) {
    await page.click(`.project-sort .filter-btn[data-sort="${order}"]`);
    const dates = await page.$$eval('#projects .section > .project-block', (bs) => bs.map((b) => b.dataset.date || '9999'));
    const sorted = [...dates].sort();
    if (order === 'newest') sorted.reverse();
    if (dates.join() !== sorted.join()) fail(`sort ${order} out of order`); else ok(`sort ${order}`);
  }
  page.errors.forEach((e) => fail('page: ' + e));

  // ── 5. Phone width: overlay fits, no horizontal scroll ──
  const phone = await freshPage(browser, { viewport: { width: 375, height: 740 } });
  await phone.waitForTimeout(800);
  const overflow = await phone.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  if (overflow > 1) fail(`phone width: page scrolls sideways by ${overflow}px`); else ok('phone width: no sideways scroll');
  await phone.screenshot({ path: process.env.SHOT || '/tmp/phone.png' });

  await browser.close();
  console.log(`\n${failures.length} failure(s)`);
  process.exit(failures.length ? 1 : 0);
})();
