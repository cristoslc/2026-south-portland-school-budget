// SPIKE-002: Investigate Diligent Community portal structure
// Test: Load a known meeting page and see what loads after JS execution

import { chromium } from 'playwright';

const MEETING_URL = 'https://southportland-gov.community.diligentoneplatform.com/Portal/MeetingInformation.aspx?Id=1285';

(async () => {
  // Reinstall playwright if needed
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Track API/XHR calls the page makes
  const apiCalls = [];
  page.on('response', async (response) => {
    const url = response.url();
    const ct = response.headers()['content-type'] || '';
    if (ct.includes('json') || url.includes('api') || url.includes('Ajax') ||
        url.includes('WebService') || url.includes('.asmx') || url.includes('.ashx')) {
      let bodyPreview = '';
      try { bodyPreview = (await response.text()).substring(0, 300); } catch {}
      apiCalls.push({ url: url.substring(0, 150), status: response.status(), ct, bodyPreview });
    }
  });

  console.log(`Loading: ${MEETING_URL}\n`);
  try {
    await page.goto(MEETING_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
    console.log('DOM loaded, waiting 8s for JS to render...');
    await page.waitForTimeout(8000);

    // Check for agenda content in the rendered DOM
    const agendaText = await page.evaluate(() => {
      // Look for common agenda containers
      const selectors = [
        '.agenda-content', '#agenda', '[class*="agenda"]', '[id*="agenda"]',
        '.meeting-content', '#meeting-content', '[class*="meeting"]',
        '.item-list', '[class*="item"]', '.topic', '[class*="topic"]',
        'table', '.section-content', '#ContentPlaceHolder'
      ];
      const results = {};
      for (const sel of selectors) {
        const els = document.querySelectorAll(sel);
        if (els.length > 0) {
          results[sel] = Array.from(els).map(el => ({
            tag: el.tagName,
            id: el.id,
            class: el.className?.toString().substring(0, 80),
            text: el.textContent?.substring(0, 200)
          }));
        }
      }
      // Also get overall body text length and sample
      const bodyText = document.body.innerText;
      results._bodyTextLength = bodyText.length;
      results._bodyTextSample = bodyText.substring(0, 500);
      results._bodyTextEnd = bodyText.substring(Math.max(0, bodyText.length - 500));
      return results;
    });

    console.log('=== Rendered DOM analysis ===');
    console.log(`Body text length: ${agendaText._bodyTextLength} chars`);
    console.log(`\nBody text start:\n${agendaText._bodyTextSample}`);
    console.log(`\nBody text end:\n${agendaText._bodyTextEnd}`);

    // Show matched selectors
    for (const [sel, matches] of Object.entries(agendaText)) {
      if (sel.startsWith('_')) continue;
      console.log(`\nSelector "${sel}": ${matches.length} match(es)`);
      for (const m of matches.slice(0, 3)) {
        console.log(`  <${m.tag} id="${m.id}" class="${m.class}">`);
        console.log(`  text: ${m.text?.substring(0, 150)}`);
      }
    }

    console.log(`\n=== API/XHR calls (${apiCalls.length}) ===`);
    for (const call of apiCalls) {
      console.log(`\n  [${call.status}] ${call.url}`);
      console.log(`  CT: ${call.ct}`);
      console.log(`  Body: ${call.bodyPreview?.substring(0, 200)}`);
    }

    // Try to find and click the agenda section
    console.log('\n=== Trying to find agenda items ===');
    const agendaItems = await page.evaluate(() => {
      // Diligent portals often use TreeView or specific div structures
      const allText = document.body.innerText;
      // Look for typical agenda markers
      const markers = ['EXECUTIVE SESSION', 'OPENING', 'PUBLIC HEARING', 'CONSENT',
                       'PETITIONS', 'ORDER OF THE DAY', 'NEW BUSINESS', 'OLD BUSINESS',
                       'Pledge', 'Roll Call', 'Minutes'];
      const found = markers.filter(m => allText.includes(m));
      return { foundMarkers: found, totalMarkers: markers.length };
    });
    console.log(`Found ${agendaItems.foundMarkers.length}/${agendaItems.totalMarkers} agenda markers: ${agendaItems.foundMarkers.join(', ')}`);

  } catch (err) {
    console.error(`Error: ${err.message}`);
  }

  await browser.close();
})();
