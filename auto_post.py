from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import requests, json, time, os

# Load env
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def get_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random")
        data = json.loads(res.text)
        return f"{data[0]['q']} — {data[0]['a']}"
    except:
        return "Stay strong. Keep going! 🚀"

def post_to_linkedin(content):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(), options=options)

    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "share-box-feed-entry__top-bar")))
    driver.find_element(By.XPATH, "//strong[contains(text(), 'Start a post')]").click()

    editor = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "ql-editor")))
    editor.click()
    editor.send_keys(content)
    time.sleep(2)

    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]"))
    )
    driver.execute_script("arguments[0].click();", post_button)
    print("✅ Posted successfully!")

if __name__ == '__main__':
    quote = get_quote()
    print("Generated quote:", quote)
    post_to_linkedin(quote)
