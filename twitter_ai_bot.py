from playwright.sync_api import sync_playwright
from groq import Groq

client = Groq(
    api_key=" YOUR_GROQ_API_KEY"
)

KEYWORD = "looking for developer"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="twitter_data",
        headless=False,
        args=[
            "--disable-extensions",
            "--start-maximized"
        ]
    )

    # Use existing tab
    page = context.pages[0]

    # Search keyword
    search_keyword = KEYWORD.replace(" ", "%20")

    # Twitter/X search URL
    url = f"https://twitter.com/search?q={search_keyword}&src=typed_query"

    print("Opening Twitter/X...")

    page.goto(url, timeout=60000)
    page.wait_for_timeout(10000)

    # Scroll page slowly
    for _ in range(5):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

    print("\n===== PAGE TEXT =====\n")

    # Get full page text
    full_text = page.locator("body").inner_text()

    # Split into lines
    tweets = full_text.split("\n")

    # Junk text filter
    blocked_words = [
        "Terms of Service",
        "Privacy Policy",
        "Cookie Use",
        "Sign up",
        "Log in",
        "Trending",
        "What’s happening",
        "Explore",
        "Messages",
        "Notifications"
    ]

    count = 0

    for tweet in tweets:

        tweet = tweet.strip()

        # Skip junk text
        if (
            len(tweet) > 80
            and not any(word in tweet for word in blocked_words)
        ):

            count += 1

            print("=" * 60)
            print(f"TWEET {count}")
            print("=" * 60)

            print(tweet[:500])

            print("\nGenerating AI reply...\n")

            # =========================
            # AI PROMPT
            # =========================
            prompt = f"""
            Generate a professional Twitter/X reply
            for this hiring tweet.

            Tweet:
            {tweet}

            Requirements:
            - Human-like
            - Professional
            - Short
            - Not spammy
            - Show interest naturally
            """
            # GROQ API CALL
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            reply = response.choices[0].message.content

            print("\n===== GENERATED REPLY =====\n")

            print(reply)

            print("\n")

        # Limit replies
        if count >= 3:
            break

    input("Press Enter to finish...")