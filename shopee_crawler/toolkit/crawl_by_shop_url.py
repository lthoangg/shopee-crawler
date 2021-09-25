from .curl import curl
from .crawl_product import get_all_data, get_neccesary_data
import concurrent.futures
import re


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_shop_info(origin, shop_url):
    try:
        match = re.match('https?:\/\/.+?\/(.*)', shop_url)
        shop_name = match.group(1).split("?")[0].split('/')[0]
        url = f"https://{origin}/api/v4/shop/get_shop_detail?username={shop_name}"
        return curl(url)['data']['shopid'], shop_name
    except Exception:
        match = re.match('https?:\/\/.+?\/shop\/(\d+)\/?.+', shop_url)
        shop_id = match.group(1)
        url = f"https://{origin}/api/v4/shop/get_shop_detail?shopid={shop_id}"
        return shop_id, curl(url)['data']['name']


def get_total(origin, id):
    url = 'https://{}/api/v4/search/search_items?by=pop&limit=1&match_id={}&newest=0&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2'.format(origin, id)

    return curl(url)['total_count']

def crawl_by_shop_url(origin, shop_url:str, limit:int=60, max_workers:int=32) -> list:
    
    shop_id, shop_name = get_shop_info(origin, shop_url)
    total_count = get_total(origin, shop_id)
    logger.info(f"There are {total_count} products in {shop_name}({shop_id})")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for newest in range(0, total_count, limit):
            url = 'https://{}/api/v4/search/search_items?by=pop&limit={}&match_id={}&newest={}&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2'.format(origin, limit, shop_id, newest)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    all_data = get_neccesary_data(origin, results)
    length = len(all_data)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} products from {shop_name}({shop_id})")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} products from {shop_name}({shop_id})")

    return all_data