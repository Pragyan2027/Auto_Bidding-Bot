from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.linkedin.com/login")
    
    print("Login manually and wait until feed loads...")
    input("Press Enter AFTER you see your LinkedIn homepage...")

    # Extra wait to ensure cookies are stored
    time.sleep(5)

    context.storage_state(path="linkedin_session.json")
    print("Session saved successfully!")

    browser.close()