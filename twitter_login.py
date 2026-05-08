from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="twitter_data",
        headless=False
    )

    page = context.pages[0]

    page.goto("https://twitter.com/login")

    input("Login manually, then press Enter here...")