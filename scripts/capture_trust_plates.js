const { chromium } = require('playwright-core');
const os = require('os');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const HTML_FILE = path.join(WORKSPACE, 'index.html');

(async () => {
  const tmpDir = path.join(os.tmpdir(), 'pw-trust-' + Date.now());
  console.log('Launching headless browser with isolated context...');
  
  const context = await chromium.launchPersistentContext(tmpDir, {
    channel: 'chrome',
    headless: true,
    viewport: { width: 1440, height: 900 },
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = context.pages()[0] || await context.newPage();

  try {
    console.log('Navigating to index.html...');
    await page.goto(`file://${HTML_FILE}`, { waitUntil: 'commit', timeout: 30000 });
    await page.waitForSelector('.trust-spec-plate', { timeout: 30000 });
    await page.waitForTimeout(1000);

    const trustSection = page.locator('.trust-spec-plate').first().locator('..');

    // 1. Arabic Obsidian Desktop
    await page.evaluate(() => switchLanguage('ar'));
    await page.waitForTimeout(800);
    await trustSection.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await trustSection.screenshot({ path: path.join(WORKSPACE, 'trust_plates_ar_obsidian.png') });
    console.log('Saved trust_plates_ar_obsidian.png');

    // 2. Arabic Daylight Desktop
    await page.evaluate(() => applyTheme('daylight', false));
    await page.waitForTimeout(800);
    await trustSection.screenshot({ path: path.join(WORKSPACE, 'trust_plates_ar_daylight.png') });
    console.log('Saved trust_plates_ar_daylight.png');

    // 3. English Obsidian Desktop
    await page.evaluate(() => {
      applyTheme('obsidian', false);
      switchLanguage('en');
    });
    await page.waitForTimeout(800);
    await trustSection.screenshot({ path: path.join(WORKSPACE, 'trust_plates_en_obsidian.png') });
    console.log('Saved trust_plates_en_obsidian.png');

    // 4. Arabic Mobile Viewport (390x844)
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => switchLanguage('ar'));
    await page.waitForTimeout(800);
    await trustSection.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await trustSection.screenshot({ path: path.join(WORKSPACE, 'trust_plates_ar_mobile.png') });
    console.log('Saved trust_plates_ar_mobile.png');

    console.log('All trust plate captures completed successfully!');
  } catch (err) {
    console.error('Error during capture:', err);
  } finally {
    await context.close();
    process.exit(0);
  }
})();
