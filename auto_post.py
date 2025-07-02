from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import chromedriver_autoinstaller
import requests, json, time, os

# Auto-install matching ChromeDriver version
chromedriver_autoinstaller.install()

# Load credentials
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def get_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random")
        data = json.loads(res.text)
        return f"{data[0]['q']} — {data[0]['a']}"
    except Exception:
        return "Stay positive and keep going!"

def post_to_linkedin(content):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1024")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.linkedin.com/login")

    # Log in
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for the feed to load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "main")))

    # Click "Start a post"
    post_trigger = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'artdeco-button') and .//span[contains(text(),'Start a post')]]"
    )))
    post_trigger.click()

    # Enter text in post box
    editor = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "ql-editor")))
    editor.click()
    editor.send_keys(content)

    # Wait a bit before clicking Post
    time.sleep(2)

    # Click the Post button
    post_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'share-actions__primary-action') and .//span[text()='Post']]"
    )))
    driver.execute_script("arguments[0].click();", post_btn)

    print("✅ Successfully posted to LinkedIn!")
    driver.quit()

if __name__ == '__main__':
    quote = get_quote()
    print("Generated quote:", quote)
    post_to_linkedin(quote)
