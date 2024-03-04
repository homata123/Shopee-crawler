# This module used for fetching top categories in Shopee's home page by API v4, then save it to a json output file. 
# The result in file will be checked and used for getting top shops in get_top_shops module

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

top_cates_url = 'https://shopee.vn/api/v4/pages/get_homepage_category_list'
login_url = 'https://shopee.vn/buyer/login?next=https%3A%2F%2Fshopee.vn%2Froman.official%3Fpage%3D01'
shopee_url = 'https://shopee.vn'

options = uc.ChromeOptions()
options.user_data_dir="./temp/profile"
driver = uc.Chrome(version_main=121, options=options,enable_cdp_events=True)


Cate = {}
def getXHRdata(eventdata):
    request_id = eventdata["params"]["requestId"]
    data =  driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
    try:
        if len(str(data)) > 10:
            idx_data_start = str(data).find('"data":')-1
            idx_data_end = -2
            json_data =json.loads(str(data)[idx_data_start:idx_data_end])
            cat_list = json_data["data"]["category_list"]
            for catdata in cat_list:
                Cate[catdata["display_name"]] = {"catid":catdata["catid"], "items":[]}
            print(Cate)
            with open('output_cates.json', 'w', encoding='utf-8') as json_file:
                json.dump(Cate, json_file, indent=2)
    except Exception as e:
       print("HH: ", e)


def get_cates():
    driver.add_cdp_listener("Network.responseReceived", getXHRdata)
    driver.get(top_cates_url)
    if len(Cate) > 0:
        driver.clear_cdp_listeners()
        driver.quit()
    input("Press any key to exit ! \n")
    driver.quit()

# get_cates()