"""_summary_
"""
import time
from selenium import webdriver  # pylint: disable=import-error
from selenium.webdriver.common.by import By  # pylint: disable=import-error
from selenium.webdriver.chrome.service import Service  # pylint: disable=import-error
from selenium.webdriver.support.ui import WebDriverWait  # pylint: disable=import-error
from selenium.webdriver.support import ( # pylint: disable=import-error
    expected_conditions as EC,
)

def tiktok_downloader(tiktok_url: str, download_dir: str):
    """_summary_

    Args:
        tiktok_url (str): _description_
        download_dir (str): _description_
    """
    service = Service(executable_path="chromedriver.exe")
    prefs = {"download.default_directory": download_dir}
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.veed.io/tools/tiktok-downloader")

    # Find the textbox using its name, ID, or other attributes
    textbox = driver.find_element(By.NAME, "content-url")
    # Clear the textbox if necessary
    textbox.clear()
    # Enter text into the textbox
    textbox.send_keys(tiktok_url)
    # Find the button using its name, ID, or other attributes
    button_search = driver.find_element(
        By.XPATH, '//*[@id="video-downloader-app"]/div[1]/form/button'
    )
    button_search.click()
    download_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="video-downloader-app"]/div[1]/div[2]/div[2]/div[1]/div/button[1]',
            )
        )
    )
    download_link.click()
    # Wait for some time if you need to see the result
    time.sleep(5)
    # Close the browser
    driver.quit()
