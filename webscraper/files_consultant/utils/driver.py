from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run without UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


# Explicitly specify Chromium's driver path
def get_driver():
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver
