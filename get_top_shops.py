import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import json
from time import sleep
from pprint import pformat
import threading
import time
import os
import pandas as pd
import re
import os
from utils import *


login_url = 'https://shopee.vn/buyer/login?next=https%3A%2F%2Fshopee.vn%2Froman.official%3Fpage%3D01'
shop_base_api = "https://shopee.vn/api/v4/shop/get_shop_base"
shop_item_rcmd_api = "https://shopee.vn/api/v4/shop/rcmd_items"
shop_sold_out_api = "https://shopee.vn/api/v4/shop/search_items?filter_sold_out"

items_per_page = 30

options = uc.ChromeOptions()

options.user_data_dir="./temp/profile"

driver = uc.Chrome(version_main=121, options=options,enable_cdp_events=True)
top_shops=[]

def getXMRdata(eventdata):
    request_id = eventdata["params"]["requestId"]
    data =  driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
    try:
        if len(str(data)) > 10:
            print(data)
            usernames = re.findall(r'"username"\s*:\s*"([^"]+)"', str(data))
            top_shops.append(usernames)
    except Exception as e:
       print("Error when parsing top shops id: ", e)
    

def onPageNavigated(eventdata):
    resp_url = eventdata["params"]["frame"]["url"]
    if resp_url == 'about:blank':
        return

    print("Navigate to:" + resp_url)

def top_shop_ids():
    output_shops = {}
    while is_file_not_empty('output_cates.json') == False:
        time.sleep(2.0)
    else:
        print("Output categories file existed and not empty")
    cates_data = {}
    with open('output_cates.json', 'r') as json_file:
        cates_data = json.load(json_file)
    for key, value in cates_data.items():
        driver.add_cdp_listener("Network.responseReceived", getXMRdata)
        driver.get('https://shopee.vn/api/v4/official_shop/get_shops_by_category?need_zhuyin=0&category_id={}'.format(value["catid"]))
        time.sleep(2.0)
        driver.clear_cdp_listeners()
    cates_list = list(cates_data.keys())
    for top_s_idx in range(len(top_shops)):
        output_shops[cates_list[top_s_idx]] = top_shops[top_s_idx]
    with open('output_shops.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_shops, json_file, indent=2)
    input("Press any key to exit ! \n")
    driver.quit()

# top_shop_ids()