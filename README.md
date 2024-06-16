# Lusha Automation Script

## Overview

This project automates the process of retrieving contact information from Lusha for a list of companies. The script performs the following tasks:

1. Logs into Lusha.
2. Searches for companies listed in an Excel file.
3. Extracts contact information (name, email, phone numbers) for specified positions.
4. Saves the extracted data to a CSV file.

## Prerequisites

To run this script, ensure you have the following installed:

- Python 3.x
- Selenium
- Chrome WebDriver
- pandas
- webdriver-manager

## Installation

1. **Clone the repository:**

    - Open your terminal or command prompt.
    - Navigate to the directory where you want to clone the repository.
    - Run the following command to clone the repository:

        ```sh
        git clone https://github.com/yourusername/lusha-automation.git
        cd lusha-automation
        ```

2. **Install the required Python packages:**

    - Ensure you have `pip` installed.
    - Run the following command to install the necessary packages:

        ```sh
        pip install selenium pandas webdriver-manager
        ```

3. **Download the Lusha Chrome extension:**

    - Go to the Lusha Chrome extension page.
    - Download the CRX file for the extension.
    - Place the CRX file in a suitable directory.
    - Update the path to the CRX file in the script.

## Setup

1. **Prepare your Excel file:**

    - Create an Excel file with a column named `CompanyName` containing the list of companies.
    - Place the Excel file in a suitable directory.
    - Update the path to the Excel file in the script.

2. **Update login credentials:**

    - Open the script file.
    - Update the Lusha login credentials with your email and password.

3. **Configure Chrome WebDriver:**

    - Ensure the `webdriver-manager` is installed as per the instructions above.
    - The script will automatically manage the Chrome WebDriver.
  

## Changeable Code  ( USE ONLY COMBINED.PY ) 

1. **Lusha Credentials:**  LINE 53 AND LINE 58
2. **Company Excel file location:**  LINE 27 AND LINE 28
3. **Lusha.crx Location:** LINE 36
4. **Position of Contact:** LINE 151
5. **Serial Number of Target Contact in Lusha List:** LINE 156


## Manual Stuff To Do 

1. When the chrome browser opens, it opens two tabs of lusha , close the righter tab immediately
2. Only While extracting the first contact, Lusha shows a pop up saying "Lusha is available everywhere" , just close it
   

   

