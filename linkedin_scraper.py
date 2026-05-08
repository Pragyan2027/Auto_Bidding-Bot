from playwright.sync_api import sync_playwright

KEYWORD = "looking for developer"

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="user_data",
        headless=False
    )

    # Use existing tab
    page = context.pages[0]

    search_keyword = KEYWORD.replace(" ", "%20")

    url = f"https://www.linkedin.com/search/results/content/?keywords={search_keyword}"

    print("Opening LinkedIn...")
    page.goto(url, timeout=60000)

    # Wait for page to load
    page.wait_for_timeout(10000)

    # Scroll slowly
    for _ in range(5):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

    print("Getting page text...")

    # Get full page text
    full_text = page.locator("body").inner_text()

    print("\n===== PAGE TEXT PREVIEW =====\n")

    print(full_text[:5000])

    print("\n============================\n")

    input("Press Enter to finish...")