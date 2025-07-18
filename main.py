import asyncio
from playwright.async_api import async_playwright,Page,expect
import random

async def Credential_Input(page,random_email):
    await asyncio.sleep(3)
    await page.locator('#user_email').fill(random_email)
    await page.locator('#user_password').fill("manggo_123")

    H2_Sign_Up = await page.locator('#login > div > h2').text_content()
    if H2_Sign_Up == 'Sign Up':
        await page.locator('#user_password_confirmation').fill("manggo_123")
        await page.locator('#new_user > div.actions > input').click()
    else:
        await page.locator('#login-button').click()

async def Logout_Account(page):
    print ("This is working 2")
    await page.wait_for_load_state('load')
    await page.locator('#wishlist-icon > div > svg').click()
    await page.locator('body > div.page-container.grid.grid-cols-1.lg\:grid-cols-12.lg\:gap-6.lg\:mt-6 > div.lg\:col-span-3 > div > form > button').click() 

async def Sign_Up_Account(page,random_email):
    print("this is working 1")
    await page.wait_for_load_state('load')
    await page.locator('#section-3942 > header > nav > div.page-container > div > div.flex.items-center.gap-4.flex-1.justify-end > div:nth-child(2) > button > svg').click()
    await page.locator('#login > div > div > a:nth-child(1)').click()
    await Credential_Input(page,random_email)

    await page.wait_for_load_state('load')
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_be_visible() #assertion for successful sign up
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_contain_text('Welcome! You have signed up successfully') #assertion for successful sign up
    

async def Login_Account(page,random_email):
    print("this is working 3")
    await page.wait_for_load_state('load')
    await page.locator('#section-3942 > header > nav > div.page-container > div > div.flex.items-center.gap-4.flex-1.justify-end > div:nth-child(2) > button > svg').click()
    await Credential_Input(page,random_email)

async def Shopping_Item(page):
    print("this is working 4")
    await page.locator('#block-6467 > a > span').click()

    await page.wait_for_load_state('load')
    await expect(page.locator('#product-256 > div.product-card-inner > h3')).to_be_visible() #assertion for specific item to buy
    await expect(page.locator('#product-256 > div.product-card-inner > h3')).to_contain_text('Dotted Shirt') #assertion for specific item to buy

    await page.locator('#product-256 > div.product-card-inner > h3').click()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        await page.goto('https://demo.spreecommerce.org/')
        random_gen_num = random.randrange(0,1000000)
        random_email = str(random_gen_num)+"@hotmail.com"

        await Sign_Up_Account(page,random_email)
        await page.wait_for_load_state('load')
        # logout account to proceed with login step
        await Logout_Account(page)
        await Login_Account(page,random_email)
        await Shopping_Item(page)
        await page.wait_for_load_state('load')

        await page.pause()
        await browser.close

asyncio.run(main())