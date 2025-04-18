from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

import config

main_url = config.WHOSCORED_URL_BASE

def initializeSeleniumScraperOptions():
    #browser_options = ChromeOptions()
    browser_options = EdgeOptions()
    browser_options.add_argument("--headless=new")  # Nuova modalità headless più compatibile
    browser_options.add_argument("--disable-blink-features=AutomationControlled")  # Nasconde Selenium
    browser_options.add_argument("--window-size=1920x1080")  # Imposta una finestra visibile
    browser_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Simula un utente reale
    browser_options.add_argument("--disable-gpu")  
    browser_options.add_argument("--no-sandbox")  
    browser_options.add_argument("--disable-dev-shm-usage")  
    browser_options.add_argument("--enable-unsafe-swiftshader")

    return browser_options

def constructWhoscoredWebDriver(url=main_url, minimize_window=True):  

    #driver = webdriver.Chrome(options=initializeSeleniumScraperOptions())
    driver = webdriver.Edge(options=initializeSeleniumScraperOptions())

    # Nascondere il WebDriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if minimize_window:
        driver.minimize_window()

    try:
        driver.get(url)
    except WebDriverException:
        driver.get(url)

    try:
        cookie_button = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-container"]/div/div/div/div[2]/div/button[2]')
        driver.execute_script("arguments[0].click();", cookie_button)
    except NoSuchElementException:
        pass
    
    return driver