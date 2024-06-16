#HEADERS :
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
import pandas as pd

# SWITCHING TO LUSHA FRAME TO INTERACT
def switch_to_extension_frame(driver):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "LU__extension_iframe")))
        logging.info("Switched to Lusha extension iframe")
    except TimeoutException:
        logging.error("Timeout while waiting to switch to Lusha extension iframe")
    except NoSuchElementException:
        logging.error("Lusha extension iframe not found")


# Read company names from Excel file
company_df = pd.read_excel("C:\\Users\\Koosh Gupta\\OneDrive\\Desktop\\Company list.xlsx")  # Update with your file path
company_list = company_df['CompanyName'].tolist()  # Assuming the column with company names is 'CompanyName'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_extension("C:\\Users\\Koosh Gupta\\Python\\selenium\\10.4.2_0.crx") # LOCATION OF YOUR LUSHA CRX FILE 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Create an empty list to store data for all companies
all_data = []

#OPENING LUSHA WEBSITE 
try:
    logger.info("Opening the Lusha website")
    driver.get("https://auth.lusha.com/login?returnUrl=https%3A%2F%2Fdashboard.lusha.com%2Finstalled")

    wait = WebDriverWait(driver, 5)

    # Wait for the email input to be present and enter the email
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys("kooshg@iitbhilai.ac.in")
    logging.info("Entered email")

    # Wait for the password input to be present and enter the password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys("Your Password")
    logging.info("Entered password")

    # Wait for the login button to be clickable and click it
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    logging.info("Clicked login button")

    logging.info("Successfully logged in")

    # Open LinkedIn in a new tab
    driver.execute_script("window.open('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    logging.info("Opened LinkedIn in a new tab")

   
    wait.until(EC.presence_of_element_located((By.NAME, "session_key")))

   # WAITING TIME FOR LUSHA CAPTCHA IF PRESENT - ALSO REFRESH LINKED IN IF LUSHA CAPTCHA COMES
    time.sleep(15)
    
    # Wait for the page to load after login
    wait.until(EC.presence_of_element_located((By.ID, "LU__extension_badge_main")))

    # Perform a search
    sear = driver.find_element(By.ID, "LU__extension_badge_main")
    sear.click()

    # Wait for the search results to load
    try:
        # Add a delay to ensure the search results page has loaded completely
        time.sleep(5)
        
        # Switch to Lusha extension iframe
        switch_to_extension_frame(driver)
        
        # Use JavaScript to click the button with text "Got it, let's go"
        script = """
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].click();
            console.log("Clicked on 'Got it, let's go' button inside Lusha extension iframe");
            break;
        }
        """
        driver.execute_script(script)
        logging.info("Clicked on 'Got it, let's go' button inside Lusha extension iframe")

        # After clicking the button, wait for some time for new elements to load
        time.sleep(5)

        # SEARCH ICON ON LUSHA
        links = driver.find_elements(By.CLASS_NAME, "tab-nav-text")
        
        links[1].click()
        time.sleep(3)
        comp = driver.find_element(By.ID, "tab-companies")  # COMPANIES ICON ON LUSHA
        comp.click()
        time.sleep(2)

        # Loop through each company in the list
        for company in company_list:
            try:
                ser = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='companies-search-bar']")
                ser.clear()
                ser.send_keys(company)
                ser.send_keys(Keys.RETURN)
                time.sleep(3)

                # Interact with the specific elements (e.g., click on them)
                company_item = driver.find_element(By.CSS_SELECTOR, "div.company-item-name-wrapper > div.TextContainer-sc-16ba1uz-0.kgAxRV")
                company_item.click()
                time.sleep(2)
                emp = driver.find_element(By.ID, "tab-employees")
                emp.click()
                time.sleep(2)
                img_element = driver.find_element(By.CSS_SELECTOR, "img[src='https://static-assets.lusha.com/plugin/icons/FilterV2.svg']")
                img_element.click()
                time.sleep(2)
                contact_location_div = driver.find_element(By.XPATH, "//div[@class='TextContainer-sc-16ba1uz-0 kgAxRV filter-list-item-label' and text()='Contact location']")
                contact_location_div.click()
                time.sleep(2)
                india_div = driver.find_element(By.XPATH, "//div[@class='TextContainer-sc-16ba1uz-0 iKhsI checkboxLabel' and text()='India']")
                india_div.click()
                time.sleep(2)
                show_results_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='filter-show-results']")))
                show_results_button.click()
                logging.info("Clicked on 'Show results' button")
                time.sleep(3)

                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='employees-search-bar']")
                    search_input.clear()  # Clear any existing text in the input field
                    search_input.send_keys("HR")   # POSITION OF PERSON YOU WANT ( CHANGEABLE )
                    search_input.send_keys(Keys.RETURN)
                    logging.info("Entered 'HR' into the search input field")  # NO NEED TO CHANGE THIS 
                    time.sleep(2)

                    img_right = driver.find_element(By.XPATH, "//img[@src='https://static-assets.lusha.com/plugin/icons/Right8x8.svg' and @alt='Right'][1]")   # CHANGEABLE IF YOU WANT 2ND PERSON , CHANGE [1] TO [2] AND SO ON                    img_right.click()
                    time.sleep(2)
                    logging.info("Clicked on the first occurrence of the 'Right' image")

                    name_element = driver.find_element(By.XPATH, "//div[@class='TextContainer-sc-16ba1uz-0 cJHTVA main-title title-wrap']")
                    name_text = name_element.text.strip()
                    time.sleep(2)
                    logging.info(f"Extracted name: {name_text}")
                    
                    try: # SHOW EMAIL ICON ( BOTH DETAILS PRESENT )
                        buttonm = driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="show-email-icon-button-id"]')
                        buttonm.click()
                        time.sleep(5)
                    except NoSuchElementException:
                        logging.warning("Show email button not found")
                        try:
                             show_email_script = """
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                        console.log(buttons[i].textContent)
                            if (buttons[i].textContent.includes('Show Email')) {
                                buttons[i].click();
                                break;
                            }
                        }
                        """
                             driver.execute_script(show_email_script)  
                             time.sleep(3) 
                        except NoSuchElementException:
                            logging.warning("Email button not found")

                    try:
                        email_element = driver.find_element(By.XPATH, "//div[@class='TextContainer-sc-16ba1uz-0 iKhsI contact-detail clickable']")
                        email_text = email_element.text.strip()
                        logging.info(f"Extracted email address: {email_text}")
                    except NoSuchElementException:
                        email_text = None
                        logging.warning("Email address not found")

                    try:
                        show_phone_script = """
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                        console.log(buttons[i].textContent)
                            if (buttons[i].textContent.includes('Show Phone')) {
                                buttons[i].click();
                                break;
                            }
                        }
                        """
                        driver.execute_script(show_phone_script)
                        
                        time.sleep(3)
                    except NoSuchElementException:
                        phone_number1 = None
                        logging.warning("Phone number button not found")
                    
                    try:
                        # Use JavaScript to extract the phone number text based on class name
                        phone_number_script = """
                        var phoneElements = document.getElementsByClassName('user-base');
                        var phoneNumbers = [];
                        for (var i = 0; i < phoneElements.length; i++) {
                            phoneNumbers.push(phoneElements[i].textContent.trim());
                        }
                        return phoneNumbers;
                        """
                        phone_numbers = driver.execute_script(phone_number_script)
    
                         # Initialize an array of two phone numbers with None
                        phone_numbers_array = [0, 0]
    
    # Populate the array with extracted phone numbers, if available
                        for i in range(min(2, len(phone_numbers))):
                            phone_numbers_array[i] = phone_numbers[i]
    
                        logging.info(f"Extracted phone numbers: {phone_numbers_array}")
                    except NoSuchElementException:
                        phone_numbers_array = [0, 0]
                        logging.warning("Phone numbers not found")

                    # Click on cancel button after showing phone number (if exists)
                    try:
                        cancel_button_script = """
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                            if (buttons[i].textContent.includes('Cancel')) {
                                buttons[i].click();
                                break;
                            }
                        }
                        """
                        driver.execute_script(cancel_button_script)
                        logging.info("Clicked on 'Cancel' button after showing phone number")
                    except NoSuchElementException:
                        logging.warning("Cancel button not found")

                    if phone_numbers_array[1] is None:
    # Only one phone number
                        all_data.append({
                              "company": company,
                              "name": name_text,
                              "email": email_text,
                             "phone1": phone_numbers_array[0],
                             "phone2": None
                           })
                    else:
    # Two phone numbers
                            all_data.append({
                             "company": company,
                              "name": name_text,
                              "email": email_text,
                              "phone1": phone_numbers_array[0],
                              "phone2": phone_numbers_array[1]
                           })

                    # Go back to the previous pages to start the loop for the next company
                    app_back_element = driver.find_element(By.XPATH, "//img[@src='https://static-assets.lusha.com/plugin/icons/AppBack.svg' and @alt='AppBack']")
                    app_back_element.click()
                    time.sleep(1)
                    app_back_element.click()
                    time.sleep(1)

                except Exception as e:   # EMPLOYEE NOT FOUND
                    logging.warning(f"An error occurred while processing company 1 '{company}': {e}")
                    app_back_element = driver.find_element(By.XPATH, "//img[@src='https://static-assets.lusha.com/plugin/icons/AppBack.svg' and @alt='AppBack']")
                    app_back_element.click()
                    continue  # Skip to the next company in case of an error

            except Exception as e:  # COMPANY NOT FOUND
                logging.warning(f"An error occurred while processing company '{company}': {e}")
                continue  # Skip to the next company in case of an error

    except Exception as e:
        logging.warning(f"Could not interact with the 'Got it, let's go' button: {e}")

    # Add a sleep to keep the browser open for debugging purposes
    logging.info("Keeping the browser open for 30 seconds for debugging purposes.")
    time.sleep(10)  # Adjust the sleep time as needed for debugging

    # Keep the script running to keep the browser open
    logging.info("Keeping the browser open indefinitely for debugging purposes.")
    

except TimeoutException as e:
    logger.error("TimeoutException: %s", e)
    driver.save_screenshot("screenshot.png")
    logger.info("Screenshot saved for debugging")

except NoSuchElementException as e:
    logger.error("NoSuchElementException: %s", e)
    driver.save_screenshot("screenshot.png")
    logger.info("Screenshot saved for debugging")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    logger.info("Waiting for manual closure...")
    input("Press Enter to close the browser and end the script.")

    # Save all collected data to a CSV file
    all_data_df = pd.DataFrame(all_data)
    all_data_df.to_csv("all_companies_contacts.csv", index=False)    
    logging.info("Saved all companies' contacts to all_companies_contacts.csv")

    # Print the DataFrame
    print(all_data_df)

    logger.info("Closing the browser")
    driver.quit()
