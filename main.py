import re
import asyncio
from playwright.sync_api import sync_playwright,Page
import pytest

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://demo.spreecommerce.org/')



    page.wait_for_load_state()
    browser.close