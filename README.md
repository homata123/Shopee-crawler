I use undetected_chromedriver which is a folk version of selenium to avoid shopee checks bots which make regular selenium doesn't usable. The result will be summarized in stats.txt. Data will be captured when the web client calls XHR to shopee's server, the code will automatically control the necessary pages to retrieve data follow below pipeline:

    Get top categories --> Get top shops for each category --> Get recommeded or sold out items in each shop --> Combine all of them to the output results (List of categories with their items)


Steps to run: 

0. Create folder ./data/ and ./temp/. Install requirements.txt by: pip install -r requirements.txt

1. Change config params such as items per page, driver version, enable_cdp_events in get_items.py file

2. Running main.py file : python main.py


*Notes* : Some sample data files which i have get are 'output_cates.json'; 'output_shops.json' and 'the_deme.json' which save raw item data of 'https://shopee.vn/the_deme' shop . 
