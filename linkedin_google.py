import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Set Chrome options to ignore SSL certificate errors and add user agent
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")  # W3C Standard mode

# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the Google sign-in page
    driver.get("https://accounts.google.com/")
    
    # Enter email and proceed
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys("kaygee1803@gmail.com")
    email_input.send_keys(Keys.RETURN)
    logging.debug("Entered email and submitted")
    
    # Wait for the password input field to appear
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "password")))
    
    # Enter password and proceed
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("yourgmailpassword")
    password_input.send_keys(Keys.RETURN)
    logging.debug("Entered password and submitted")

    # Wait for Google authentication and LinkedIn to load after sign-in
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))

    # Perform a search (e.g., for 'Google HR')
    search_input = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
    search_input.click()
    search_input.send_keys("Google HR")
    search_input.send_keys(Keys.RETURN)
    logging.info("Performed search for 'Google HR'")

    # Wait for the search results to load
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "See all people results")))

    # Click on the "See all people results" link
    try:
        # Add a delay to ensure the search results page has loaded completely
        time.sleep(2)
        see_all_link = driver.find_element(By.LINK_TEXT, "See all people results")
        see_all_link.click()
        logging.info("Clicked on the 'See all people results' link")
    except Exception as e:
        logging.warning(f"Could not interact with the 'See all people results' link: {e}")

    # Add a sleep to keep the browser open for debugging purposes
    logging.info("Keeping the browser open for 30 seconds for debugging purposes.")
    time.sleep(30)  # Adjust the sleep time as needed for debugging

    # Keep the script running to keep the browser open
    logging.info("Keeping the browser open indefinitely for debugging purposes.")
    while True:
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    logging.info("Exiting the script. The browser will remain open.")
    input("Press Enter to close the browser and exit the script...")
    driver.quit()  # Use this to manually close the browser after pressing Enter
