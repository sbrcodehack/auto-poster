import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time, os, requests, json

# Load .env
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def get_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random")
        data = json.loads(res.text)
        return f"{data[0]['q']} — {data[0]['a']}"
    except:
        return "Keep going. You're doing great!"

def post_to_linkedin(quote):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = uc.Chrome(options=options)
    driver.get("https://www.linkedin.com/login")

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "main")))

    start_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'artdeco-button') and .//span[contains(text(),'Start a post')]]"
    )))
    start_btn.click()

    editor = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "ql-editor")))
    editor.click()
    editor.send_keys(quote)
    time.sleep(2)

    post_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'share-actions__primary-action') and .//span[text()='Post']]"
    )))
    post_btn.click()

    print("✅ Posted successfully.")
    driver.quit()

if __name__ == "__main__":
    quote = get_quote()
    print("Generated quote:", quote)
    post_to_linkedin(quote)
