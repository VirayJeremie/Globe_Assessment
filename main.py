import asyncio
from playwright.async_api import async_playwright,Page,expect
import random

async def Credential_Input(page,random_email):
    await asyncio.sleep(3)
    await page.locator('//*[@id="user_email"]').fill(random_email)
    await page.locator('//*[@id="user_password"]').fill("manggo_123")

    H2_Sign_Up = await page.locator('//*[@id="login"]/div/h2').text_content()
    if H2_Sign_Up == 'Sign Up':
        await page.locator('//*[@id="user_password_confirmation"]').fill("manggo_123")
        await page.locator('//*[@id="new_user"]/div[4]/input').click()
    else:
        await page.locator('//*[@id="login-button"]').click()


async def Sign_Up_Account(page,random_email):
    print("this is working 1")
    await page.locator('//*[@id="section-3942"]/header/nav/div[1]/div/div[3]/div[2]/button').click()
    await page.wait_for_load_state('load')
    await page.locator('//*[@id="login"]/div/div/a[1]').click()
    await page.wait_for_load_state()
    await Credential_Input(page,random_email)

    await page.wait_for_load_state()
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_be_visible() #assertion for successful login
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_contain_text('Welcome! You have signed up successfully') #assertion for successful login

async def Login_Account(page,random_email):
    print("this is working 2")
    await page.locator('//*[@id="section-3942"]/header/nav/div[1]/div/div[3]/div[2]/button').click()
    await page.wait_for_load_state()
    await Credential_Input(page,random_email)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        await page.goto('https://demo.spreecommerce.org/')
        random_gen_num = random.randrange(0,100000)
        random_email = str(random_gen_num)+"@hotmail.com"
        await page.wait_for_load_state()
        await Sign_Up_Account(page,random_email)
        await Login_Account(page,random_email)
        # await page.wait_for_load_state()
        # print("this is working 2")

        await page.pause()
        await browser.close

asyncio.run(main())