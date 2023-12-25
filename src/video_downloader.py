'''The `tiktok_downloader` function downloads a TikTok video from a given URL and saves it to a
specified directory.

Parameters
----------
directory
    The `directory` parameter is the path to the directory where the files are located. It should be a
string representing the directory path.
new_name
    The `new_name` parameter is a string representing the new name you want to give to the most recent
file in the specified directory.

Returns
-------
    The `rename_most_recent_file` function returns the new file path after renaming the most recent
file in the specified directory.

'''

import os
import glob
import time
from pathlib import Path
from selenium import webdriver  # pylint: disable=import-error
from selenium.webdriver.common.by import By  # pylint: disable=import-error
from selenium.webdriver.chrome.service import Service  # pylint: disable=import-error
from selenium.webdriver.support.ui import WebDriverWait  # pylint: disable=import-error
from selenium.webdriver.support import ( # pylint: disable=import-error
    expected_conditions as EC,
)

# Determine parent path of repository
parent_dir = Path.cwd()


def rename_most_recent_file(new_dir, new_name):
    '''The function `rename_most_recent_file` renames the most recent file in a given directory with a new
    name.
    
    Parameters
    ----------
    directory
        The directory parameter is the path to the directory where the files are located. It should be a
    string representing the directory path.
    new_name
        The new name is a string that you want to rename the most recent file to.
    
    Returns
    -------
        the new file path after renaming the most recent file in the specified directory.
    
    '''

    # Ensure the directory ends with a slash
    new_dir = str(new_dir)
    if not new_dir.endswith('\\'):
        new_dir += "\\"

    # List all files in the directory
    files = glob.glob(new_dir + '*')

    # Filter out directories, only keep files
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        print("No files found in the directory.")
        return

    # Sort files by creation time in descending order
    files.sort(key=os.path.getctime, reverse=True)

    # Get the most recent file
    most_recent_file = files[0]

    # Extract the extension from the most recent file
    _, file_extension = os.path.splitext(most_recent_file)

    # Create new file path with the same extension
    new_file_path = os.path.join(new_dir, new_name + file_extension)

    # Rename the file
    os.rename(most_recent_file, new_file_path)
    # print(f"Renamed '{most_recent_file}' to '{new_file_path}'")

    return new_file_path

def tiktok_downloader(tiktok_url: str, download_dir: str):
    '''The `tiktok_downloader` function downloads a TikTok video from a given URL and saves it to a
    specified directory.
    
    Parameters
    ----------
    tiktok_url : str
        The URL of the TikTok video you want to download.
    download_dir : str
        The `download_dir` parameter is the directory where you want to save the downloaded TikTok video.
    It should be a string representing the path to the directory on your computer. For example,
    "C:/Users/Username/Downloads" or "/home/username/Downloads".
    
    Returns
    -------
        the file path of the downloaded TikTok video.
    
    '''
    vid_num = tiktok_url.rsplit("/", maxsplit=1)[-1]
    creator = tiktok_url.split("/")[-3][1:]
    filename = f"{creator}-{vid_num}"
    vid_dir = os.listdir(download_dir)
    if f"{filename}.mp4" in vid_dir:
        print("Using existing Video file!")
        return download_dir / f"{filename}.mp4"
    
    print(parent_dir)
    service = Service(executable_path= str(parent_dir / "chromedriver.exe"))
    prefs = {"download.default_directory": str(download_dir)}
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

    time.sleep(5)

    new_file_path = rename_most_recent_file(download_dir, filename)

    return new_file_path
