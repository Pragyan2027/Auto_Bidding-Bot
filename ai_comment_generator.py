from playwright.sync_api import sync_playwright
from groq import Groq
import csv
import os

client = Groq(
    api_key=" YOUR_GROQ_API_KEY"
)

KEYWORD = "looking for developer"


CSV_FILE = "processed_posts.csv"
def load_processed_posts():

    processed = set()

    if os.path.exists(CSV_FILE):

        with open(CSV_FILE, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for row in reader:
                if row:
                    processed.add(row[0])

    return processed

def save_post(post_text):

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([post_text[:100]])


with sync_playwright() as p:

    # Load processed posts
    processed_posts = load_processed_posts()

    # Launch browser with saved session
    context = p.chromium.launch_persistent_context(
        user_data_dir="user_data",
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

    # LinkedIn search URL
    url = f"https://www.linkedin.com/search/results/content/?keywords={search_keyword}"

    print("Opening LinkedIn...")

    page.goto(url, timeout=60000)

    # Wait for posts to load
    page.wait_for_timeout(10000)

    # Scroll page slowly
    print("Scrolling page...\n")

    for _ in range(5):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

    print("Getting page text...\n")

    # Extract full page text
    full_text = page.locator("body").inner_text()

    # Split possible posts
    posts = full_text.split("Feed post")

    print(f"Found {len(posts)} possible posts\n")

    count = 0

    for post in posts:

        post = post.strip()

        # Skip small text
        if len(post) < 200:
            continue

        # Create simple post ID
        post_id = post[:100]

        # Skip duplicates
        if post_id in processed_posts:
            print("Skipping duplicate post...\n")
            continue

        count += 1

        print("=" * 60)
        print(f"POST {count}")
        print("=" * 60)

        print(post[:500])

        print("\nGenerating AI comment...\n")
        prompt = f"""
        Generate a short professional LinkedIn reply
        for this hiring post.

        Hiring Post:
        {post[:1000]}

        Requirements:
        - Sound human
        - Sound professional
        - 3 to 4 lines
        - Do not sound spammy
        - Show genuine interest
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        comment = response.choices[0].message.content

        print("===== GENERATED COMMENT =====\n")

        print(comment)

        print("\n")

        # Save processed post
        save_post(post)

        # Add to memory immediately
        processed_posts.add(post_id)

        # Limit number of generated comments
        if count >= 3:
            break

    input("Press Enter to finish...")