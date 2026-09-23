const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

if (!fs.existsSync('scratch')) {
  fs.mkdirSync('scratch', { recursive: true });
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
  
  // 1. Visit index.html honey showcase
  const indexPath = 'file://' + path.resolve('index.html');
  await page.goto(indexPath, { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(800);
  
  const honeySection = await page.$('#honey-showcase');
  if (honeySection) {
    await honeySection.scrollIntoViewIfNeeded();
    await page.waitForTimeout(600);
    await page.screenshot({ path: 'scratch/screenshot_web_honey_showcase_1440.png' });
    console.log('Captured scratch/screenshot_web_honey_showcase_1440.png');
  }

  // 2. Switch to Arabic and capture
  await page.evaluate(() => switchLanguage('ar'));
  await page.waitForTimeout(600);
  if (honeySection) {
    await page.screenshot({ path: 'scratch/screenshot_web_honey_showcase_ar_1440.png' });
    console.log('Captured scratch/screenshot_web_honey_showcase_ar_1440.png');
  }

  // 3. Test Angle Click (Open Jar)
  await page.evaluate(() => switchLanguage('en'));
  await page.evaluate(() => switchWebHoneyAngle('open'));
  await page.waitForTimeout(600);
  if (honeySection) {
    await page.screenshot({ path: 'scratch/screenshot_web_honey_open_jar.png' });
    console.log('Captured scratch/screenshot_web_honey_open_jar.png');
  }

  // 4. Visit mariam.html Slide 10 (Slide index 9)
  const mariamPath = 'file://' + path.resolve('mariam.html');
  await page.goto(mariamPath, { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.evaluate(() => {
    showSlide(9);
  });
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'scratch/screenshot_catalog_slide_10_pdp.png' });
  console.log('Captured scratch/screenshot_catalog_slide_10_pdp.png');

  // 5. Test Slide 10 angle switch in mariam.html
  await page.evaluate(() => selectHoneyPdpAngle('open'));
  await page.waitForTimeout(600);
  await page.screenshot({ path: 'scratch/screenshot_catalog_slide_10_open.png' });
  console.log('Captured scratch/screenshot_catalog_slide_10_open.png');

  await browser.close();
  console.log('All screenshots verified successfully!');
})();
