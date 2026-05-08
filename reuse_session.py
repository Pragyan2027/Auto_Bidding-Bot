from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    context = browser.new_context(storage_state="linkedin_session.json")
    page = context.new_page()
    
    page.goto("https://www.linkedin.com/feed/")
    
    input("Check if logged in. Press Enter to exit...")
    browser.close()