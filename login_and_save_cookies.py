import json

from playwright.async_api import async_playwright


async def login_and_save_cookies(username: str, password: str, cookies_file: str = 'twitter_cookies.json'):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://twitter.com/login')
        await page.fill('input[name="text"]', username)
        next_button_texts = ["Next", "Weiter"]
        for text in next_button_texts:
            next_buttons = await page.query_selector_all(f'text="{text}"')
            if next_buttons:
                await next_buttons[0].click()
                break

        await page.wait_for_selector('input[name="password"]', state='visible')
        await page.fill('input[name="password"]', password)
        await page.click('text="Log in"')

        await page.wait_for_url('https://twitter.com/home')

        cookies = await context.cookies()
        with open(cookies_file, 'w') as f:
            f.write(json.dumps(cookies))

        await browser.close()
