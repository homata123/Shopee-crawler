from multiprocessing import Process
import time
import json
from utils import *
from get_top_cates import get_cates
from get_top_shops import top_shop_ids
from get_items import get_items_by_shop_id


if __name__ == "__main__":
    result = {}
    process1 = Process(target=get_cates)
    process2 = Process(target=top_shop_ids)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    while is_file_not_empty('output_shops.json') and is_file_not_empty('output_cates.json') == False:
        time.sleep(2.0)
    else:
        print("Output shops and cates files existed and not empty")
        process1.terminate()
        process2.terminate()
    shops_data = {}
    with open('output_shops.json', 'r') as json_file:
        shops_data = json.load(json_file)
    for cate, list_shops in shops_data.items():
        for shop in list_shops[:3]:
            print(shop)
            get_items_by_shop_id(shop, cate)

    # get_items_by_shop_id("atuner.official", "Thời trang nam")