import asyncio
from playwright.async_api import async_playwright,Page,expect
import pytest
from Login_Credentials import Credentials
from Order_Details import Order_Details
from Checkout_Details import Checkout_Details

@pytest.mark.asyncio
async def Credential_Input(page,random_email,password):
    await asyncio.sleep(5)
    await page.locator('#user_email').fill(random_email)
    await page.locator('#user_password').fill(password)

    H2_Sign_Up = await page.locator('#login > div > h2').text_content()
    if H2_Sign_Up == 'Sign Up':
        await page.locator('#user_password_confirmation').fill(password)
        await page.locator('#new_user > div.actions > input').click()
    else:
        await page.locator('#login-button').click()

@pytest.mark.asyncio
async def Logout_Account(page):
    await page.locator('#wishlist-icon > div > svg').click()
    await page.wait_for_load_state('load')

    await page.locator(r'body > div.page-container.grid.grid-cols-1.lg\:grid-cols-12.lg\:gap-6.lg\:mt-6 > div.lg\:col-span-3 > div > form > button').click() 
    await page.wait_for_load_state('load')

@pytest.mark.asyncio
async def Sign_Up_Account(page,random_email,password):
    
    await page.locator('#section-3942 > header > nav > div.page-container > div > div.flex.items-center.gap-4.flex-1.justify-end > div:nth-child(2)').click()
    await page.wait_for_load_state('load')

    #await page.screenshot(path="screenshots/screenshot.png")
    await page.locator('#login > div > div > a:nth-child(1)').click()
    await page.wait_for_load_state('load')
    await Credential_Input(page,random_email,password)

    await page.wait_for_load_state('load')
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_be_visible() # assertion for successful sign up
    await expect(page.locator('//*[@id="flashes"]/div/div/div/p')).to_contain_text('Welcome! You have signed up successfully') # assertion for successful sign up
    
@pytest.mark.asyncio
async def Login_Account(page,random_email,password):
    await page.locator('#section-3942 > header > nav > div.page-container > div > div.flex.items-center.gap-4.flex-1.justify-end > div:nth-child(2) > button > svg').click()
    await page.wait_for_load_state('load')
    await Credential_Input(page,random_email,password)

@pytest.mark.asyncio
async def Shopping_Item(page,Ordered_Item,Ordered_Size):
    await page.locator('#block-6467 > a > span').click()
    await page.wait_for_load_state('load')

    await expect(page.locator('#product-256 > div.product-card-inner > h3')).to_be_visible() # assertion for specific item to buy
    await expect(page.locator('#product-256 > div.product-card-inner > h3')).to_contain_text(Ordered_Item) # assertion for specific item to buy
    await page.locator('#product-256 > div.product-card-inner > h3').click()
    await page.wait_for_load_state('load')

    await asyncio.sleep(5)
    await page.locator('#option-23-value').click()
    await page.wait_for_load_state('load')
    
    await expect(page.locator(r'#product-variant-picker > fieldset:nth-child(3) > div > div.absolute.top-11.left-0.z-\[9999\].flex.w-screen.max-w-max.shadow-xs')).to_contain_text(Ordered_Size) #assertion for size in list
    
    await page.locator(r'#product-variant-picker > fieldset:nth-child(3) > div > div.absolute.top-11.left-0.z-\[9999\].flex.w-screen.max-w-max.shadow-xs > div > label:nth-child(4)').click()
    await page.locator(r'#product-details-page > div.lg\:col-span-5.lg\:col-start-8 > div > div.h-full.w-full.waitlist-modal > form > div.flex.w-full.my-5 > div.w-full.bottom-0.flex.flex-col.gap-4.z-10 > button').click()
    await asyncio.sleep(5) # timer for delay to process items in cart

@pytest.mark.asyncio
async def Checkout_Item(page,Checkout_firstname,Checkout_lastname,Checkout_address1,Checkout_city,Checkout_zipcode,Ordered_Item,Ordered_Price,Ordered_Quantity,Checkout_card_number,Checkout_card_cvc,Checkout_card_date):
    await asyncio.sleep(5)
    await expect(page.locator('[id^="line_item_"] > li > div.ml-3.w-full > div.flex.justify-between > a')).to_contain_text(Ordered_Item) # assertion for ordered item
    await expect(page.locator('[id^="line_item_"] > li > div.ml-3.w-full > div.mb-2.text-sm > span')).to_contain_text(str(Ordered_Price)) # assertion for price
    await expect(page.locator('#line_item_quantity')).to_have_value(str(Ordered_Quantity)) # assertion for quantity

    await asyncio.sleep(5)
    await page.locator('#cart_summary > div > div.flex.flex-col.gap-4.mt-4.w-full.justify-end.items-end > div.flex.flex-col.gap-4.w-full > a').click()
    await page.wait_for_load_state('load')
    await page.select_option("select#order_ship_address_attributes_country_id", index=168)
    await page.locator('#order_ship_address_attributes_firstname').fill(Checkout_firstname)
    await page.locator('#order_ship_address_attributes_lastname').fill(Checkout_lastname)
    await page.locator('#order_ship_address_attributes_address1').fill(Checkout_address1)
    await page.locator('#order_ship_address_attributes_city').fill(Checkout_city)
    await page.locator('#order_ship_address_attributes_zipcode').fill(Checkout_zipcode)

    await asyncio.sleep(10)
    await page.locator('#checkout_form_address > div.flex.justify-end.w-full > button').click()
    await page.get_by_text("Save and Continue").click()
    await page.wait_for_load_state('load')

    #await page.locator('#order_payments_attributes__payment_method_id_24').click()
    await asyncio.sleep(10)
    card_frame = page.frame_locator('iframe[src*="elements-inner-payment"]')
    await card_frame.locator('input[name="number"]').fill(Checkout_card_number)
    await card_frame.locator('input[name="expiry"]').fill(Checkout_card_date)
    await card_frame.locator('input[name="cvc"]').fill(Checkout_card_cvc)

    await page.locator('#checkout-payment-submit').scroll_into_view_if_needed()
    await page.locator('#checkout-payment-submit').click()
    await page.wait_for_load_state('load')

@pytest.mark.asyncio
async def Verify_Order_Completion(page,Confirmed_Order):
    await asyncio.sleep(5) # timer for delay to process checkout
    await page.wait_for_load_state('load')
    await expect(page.locator('[id^="order_"] > div:nth-child(3) > h5')).to_contain_text(Confirmed_Order) #validates order confirmation
    await expect(page.locator('#checkout')).to_be_visible() #validates order number

@pytest.mark.asyncio
async def test_main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto('https://demo.spreecommerce.org/')

        # Instantiate credential values for New User
        Generate_User = Credentials()
        User_Email = Generate_User.user_username
        User_Password = Generate_User.user_password

        # Sign up/Register Account
        await asyncio.sleep(10)
        await Sign_Up_Account(page,User_Email,User_Password)
        await page.wait_for_load_state('load')

        # Logout account to proceed with login step
        await Logout_Account(page)

        # Login Account
        await asyncio.sleep(5)
        await Login_Account(page,User_Email,User_Password)

        # Instantiate constant values for Order Details
        Order_Information = Order_Details()
        Ordered_Item = Order_Information.Ordered_item
        Ordered_Size = Order_Information.Ordered_Size
        Ordered_Quantity = Order_Information.Ordered_Quantity
        Ordered_Price = Order_Information.Ordered_Price
        Confirmed_Order = Order_Information.Confirmed_Order

        # Shop Clothes/Items 
        await Shopping_Item(page,Ordered_Item,Ordered_Size)

        # Instantiate constant values for Checkout Details
        Checkout_Information = Checkout_Details()
        Checkout_firstname = Checkout_Information.firstname
        Checkout_lastname = Checkout_Information.lastname
        Checkout_address1 = Checkout_Information.address1
        Checkout_city = Checkout_Information.city
        Checkout_zipcode = Checkout_Information.zipcode
        Checkout_card_number = Checkout_Information.card_number
        Checkout_card_cvc = Checkout_Information.card_cvc
        Checkout_card_date = Checkout_Information.card_date

        # Checkout and Process payment 
        await Checkout_Item(page,Checkout_firstname,Checkout_lastname,Checkout_address1,Checkout_city,
                            Checkout_zipcode,Ordered_Item,Ordered_Price,Ordered_Quantity,
                            Checkout_card_number,Checkout_card_cvc,Checkout_card_date)

        # Verify Order is completed
        await Verify_Order_Completion(page,Confirmed_Order)

        await page.wait_for_load_state('load')

        await browser.close()

asyncio.run(test_main())