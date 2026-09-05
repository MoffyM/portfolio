const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const output = path.join(process.cwd(), 'docs', 'qa', 'homepage');
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const results = {};
  for (const viewport of [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle' });
    results[viewport.name] = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      about: document.body.innerText.includes('ABOUT ME'),
      qrWidth: document.querySelector('img[alt="MoffyAI 微信二维码"]')?.getBoundingClientRect().width,
      inviteSize: getComputedStyle(document.querySelector('.hero-invite')).fontSize,
      storyCopySize: getComputedStyle(document.querySelector('.story-item-copy')).fontSize,
    }));
    await page.screenshot({ path: path.join(output, `${viewport.name}-full.png`), fullPage: true });
    await page.locator('text=ABOUT ME').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(output, `${viewport.name}-story.png`) });
    await page.locator('.story-timeline-panel').screenshot({ path: path.join(output, `${viewport.name}-timeline-panel.png`) });
    await page.locator('text=感谢你看到这里。').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(output, `${viewport.name}-contact.png`) });
    await page.close();
  }
  const staticPage = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await staticPage.route('**/assets/js/vendor.js', route => route.abort());
  await staticPage.goto('http://127.0.0.1:4173/', { waitUntil: 'domcontentloaded' });
  results.staticCss = await staticPage.evaluate(() => {
    const profileRow = document.querySelector('.agent-copy section');
    const stamp = document.querySelector('.story-stamp');
    const timeline = document.querySelector('.story-timeline-panel');
    return {
      gridDisplay: getComputedStyle(profileRow).display,
      gridTemplate: getComputedStyle(profileRow).gridTemplateColumns,
      stampPosition: getComputedStyle(stamp).position,
      timelineWidth: timeline.getBoundingClientRect().width,
    };
  });
  await staticPage.close();
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
  if (results.desktop.scrollWidth !== results.desktop.clientWidth || results.mobile.scrollWidth !== results.mobile.clientWidth ||
      !results.desktop.about || !results.mobile.about || !results.desktop.qrWidth || !results.mobile.qrWidth ||
      results.staticCss.gridDisplay !== 'grid' || !results.staticCss.gridTemplate.includes('32px') ||
      results.staticCss.stampPosition !== 'absolute' || results.staticCss.timelineWidth < 500) process.exit(1);
})();
