from selenium import webdriver
from PIL import Image, ImageOps
from io import BytesIO
import time, requests
from sys import platform

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

url_base = "https://items.blossomcraft.org/"

@dataclass
class Item:
    id: int


def dictToItem(item: Dict[str, str]) -> Item:
    """Convert the raw JSON data of an item into an easy to use Object."""
    return Item(
            int(item["id"]))

def pullItemList() -> List[Item] | None:
    """Pull the list of Items from the Item List Website."""
    dataToPull = ["id"]
    headers = {
        "I-INCLUDED-INFO" : ";".join(dataToPull)
    }
    results = requests.get(
        f"{url_base}api/items",
        headers = headers)
    if results:
        return [dictToItem(item) for item in results.json()["data"]]
    return None

def pullMiscItems() -> List[Item] | None:
    """Pull the list of Items from the Item List Website."""
    dataToPull = ["id"]
    headers = {
        "I-INCLUDED-INFO" : ";".join(dataToPull)
    }
    results = requests.get(
        f"{url_base}api/miscitems",
        headers = headers)
    if results:
        return [dictToItem(item) for item in results.json()["data"]]
    return None


missingImages = {"miscDescriptions" : [], "descriptions" : []}
items = pullItemList()
miscItems = pullMiscItems()
if platform == "win32":
    loc = f"core/static/images/"
else:
    loc = f"/home/blossomcraft/BlossomCraft/core/_Shared/static/images/"
desc_file_list = [p.name for p in Path(f"{loc}Descriptions").iterdir() if p.is_file()]
misc_file_list = [p.name for p in Path(f"{loc}Misc_Descriptions").iterdir() if p.is_file()]
if items:
    for item in items:
        if f"{item.id}.png" not in desc_file_list:
            print(f"Missing Description for {item.id}")
            missingImages["descriptions"].append(item.id)
if miscItems:
    for item in miscItems:
        if f"{item.id}.png" not in misc_file_list:
            print(f"Missing Description for *MISC* {item.id}")
            missingImages["miscDescriptions"].append(item.id)
if len(missingImages["descriptions"]) > 0:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(522, 1080)
    
    try:
        for itemID in missingImages["descriptions"]:
            browser.get(f"{url_base}items/rawitem/{itemID}")
            while True:
                script = '''return document.fonts.status;'''
                loaded = browser.execute_script(script)
                if loaded == 'loaded':
                    break
                time.sleep(.25)
            png = browser.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            imageSize = im.size
            invert_im = im.convert("RGB")
            invert_im = ImageOps.invert(invert_im)
            imageBox = invert_im.getbbox()
            cropped=im.crop(imageBox)
            cropped.save(f"{loc}Descriptions/{itemID}.png")
    finally:
        browser.quit()
if len(missingImages["miscDescriptions"]) > 0:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(522, 1080)
    
    try:
        for itemID in missingImages["miscDescriptions"]:
            browser.get(f"{url_base}miscitems/rawmiscitem/{itemID}")
            while True:
                script = '''return document.fonts.status;'''
                loaded = browser.execute_script(script)
                if loaded == 'loaded':
                    break
                time.sleep(.25)
            png = browser.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            imageSize = im.size
            invert_im = im.convert("RGB")
            invert_im = ImageOps.invert(invert_im)
            imageBox = invert_im.getbbox()
            cropped=im.crop(imageBox)
            cropped.save(f"{loc}Misc_Descriptions/{itemID}.png")
    finally:
        browser.quit()
else:
    print("No missing descriptions, generation skipped.")
