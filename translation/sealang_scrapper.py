import argparse
import sys
import csv
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import pathlib

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.firefox.options import Options

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def submit_form(url: str, input_text: str, headless: bool = False, timeout: int = 20):
    if pathlib.Path("datasets").is_dir() is False:
            pathlib.Path("datasets").mkdir(parents=True, exist_ok=True)    
    if pathlib.Path(f"datasets/{input_text}.csv").is_file():
        logger.info(f"File datasets/{input_text}.csv already exists. Skipping download.")
        return # Skip if file already exists
    if pathlib.Path(f"error_screenshots/error_{input_text}.png").is_file():
        logger.info(f"File error_screenshots/error_{input_text}.png already exists. Skipping download.")
        return
    
    options = Options()
    if headless:
        options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    options = Options()
    options.add_argument("--headless")    
    options.set_preference("general.useragent.override", user_agent)
    options.set_preference("intl.accept_languages", "en-US, en")
    
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout)
    logger.info(f"Text '{input_text}' - Browser launched")

    try:
        driver.get(url)
        driver.switch_to.frame("menu")

        field = wait.until(EC.presence_of_element_located((By.NAME, "westernTarget")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        field.clear()
        field.send_keys(input_text)

        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form0 > button:nth-child(8)")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()

        driver.switch_to.default_content()
        
        try:
            sleep(2)  # Wait for 2 seconds to ensure the frame is loaded
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "corpus")))
            ltab = wait.until(EC.presence_of_element_located((By.TAG_NAME, "ltab")))
            
            ltab_elements = driver.find_elements(By.TAG_NAME, "ltab")
            with open(f"datasets/{input_text}.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["mdh", "en"])
                for ltab in ltab_elements:
                    rows = ltab.find_elements(By.TAG_NAME, "row")
                    if len(rows) >= 2:
                        writer.writerow([rows[0].text, rows[1].text])
        except (NoSuchElementException, UnexpectedAlertPresentException) as e:
            logger.error(f"Failed to find element in 'corpus' frame: {e}")
    except (TimeoutException, NoSuchElementException) as e:
        if pathlib.Path(f"error_screenshots").is_dir() is False:
            pathlib.Path(f"error_screenshots").mkdir(parents=True, exist_ok=True)
        if pathlib.Path(f"error_screenshots/error_{input_text}.png").is_file() is False:
            driver.save_screenshot(f"error_screenshots/error_{input_text}.png")
        logger.info(f"Screenshot saved as error_screenshots/error_{input_text}.png")
        sys.exit(1)
    finally:
        driver.quit()
        sleep(20)  # Ensure the browser has time to close properly
        logger.info(f"Text {input_text} - Browser closed")
    logger.info(f"Text {input_text} - Form submitted successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill 'westernTarget' and click the 7th button under #form0.")
    parser.add_argument("--url", required=True, help="Target page URL")
    parser.add_argument("--text", nargs='+', required=True, help="Text(s) to input into the 'westernTarget' field (space separated)")
    parser.add_argument("--headless", action="store_true", help="Run Firefox in headless mode")
    parser.add_argument("--timeout", type=int, default=20, help="Max wait seconds for elements to appear")
    args = parser.parse_args()

    # Use multiprocessing instead of subprocess for better resource management
    # with multiprocessing.Pool(processes=min(4, len(args.text))) as pool:
    #     pool.starmap(
    #         submit_form,
    #         [(args.url, text, args.headless, args.timeout) for text in args.text]
    #     )
    # logger.info("All processes completed.")
    
    with ThreadPoolExecutor(max_workers=min(6, len(args.text))) as executor:
        futures = [
            executor.submit(submit_form, args.url, text, args.headless, args.timeout)
            for text in args.text
            
        ]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"An error occurred: {e}")