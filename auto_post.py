import os
from playwright.sync_api import sync_playwright
import random
import requests
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Generate a motivational quote using ZenQuotes API
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            return response.json()[0]['q'] + " — " + response.json()[0]['a']
        else:
            return "Believe you can and you're halfway there. — Theodore Roosevelt"
    except:
        return "Success usually comes to those who are too busy to be looking for it. — Henry David Thoreau"

def post_to_linkedin(quote):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login to LinkedIn
        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", LINKEDIN_EMAIL)
        page.fill("input#password", LINKEDIN_PASSWORD)
        page.click("button[type=submit]")

        # Wait for homepage
        page.wait_for_selector("[role=button][aria-label^='Start a post']", timeout=15000)
        page.click("[role=button][aria-label^='Start a post']")

        # Wait for editor and fill the post
        page.wait_for_selector("div[role=textbox]")
        page.fill("div[role=textbox]", quote)

        # Click Post button
        page.click("button:has-text('Post')")

        # Confirm posted
        page.wait_for_timeout(5000)
        print("✅ Posted to LinkedIn successfully!")

        context.close()
        browser.close()

if __name__ == "__main__":
    quote = get_quote()
    print(f"Generated quote: {quote}")
    post_to_linkedin(quote)
