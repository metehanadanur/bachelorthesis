import asyncio
import json

from playwright.async_api import async_playwright

from intercept_respone import intercept_response


async def fetch_user_posts(url: str, cookies_file: str = 'twitter_cookies.json'):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context()

        with open(cookies_file, 'r') as f:
            cookies = json.loads(f.read())
        await context.add_cookies(cookies)

        page = await context.new_page()
        page.on('response', intercept_response)

        await page.goto(url)
        await page.wait_for_selector("[data-testid='primaryColumn']", timeout=60000)

        last_height = await page.evaluate("() => document.body.scrollHeight")
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)
            new_height = await page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        await browser.close()

