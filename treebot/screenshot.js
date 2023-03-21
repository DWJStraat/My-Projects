const puppeteer = require('puppeteer')
const path = require("node:path")
const fs = require('node:fs');
async function screenshot() {
    const imagesPath = path.join(__dirname, 'images')
    const browser = await puppeteer.launch()
    const page = await browser.newPage()

    await page.setViewport({
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1
    })
    console.log('done')
    await page.goto("https://global-mind.org/gcpdot/gcp.html")
    await page.screenshot({
        path: `${imagesPath}/dashboard.png`
    })

    if (fs.existsSync(`${imagesPath}/dashboard.png`)) {
        console.log("screenshot saved");
    }

    await browser.close()
    console.log('done')
    return `${imagesPath}/dashboard.png`

}
screenshot()