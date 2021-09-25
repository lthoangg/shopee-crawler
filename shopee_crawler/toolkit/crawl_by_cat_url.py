from .curl import curl
from .crawl_product import get_all_data, get_neccesary_data
import json
import re
import urllib.parse

import concurrent.futures

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_category_info(origin, cat_url):
    cat_url = urllib.parse.unquote(cat_url)
    pattern = rf'https://{origin}/(.+)-cat.(\d+)'
    match = re.search(pattern, cat_url)
    cat_name = match.group(1)
    cat_id = match.group(2)
    return cat_id, cat_name

def get_total(origin, id):
    url = 'https://{}/api/v4/search/search_items?by=relevancy&limit=60&match_id={}&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2'.format(origin, id)

    return json.loads(curl(url)['search_tracking'])["total_count"]

def crawl_by_cat_url(origin, cat_url:str, limit:int=60, max_workers:int=32) -> list:

    cat_id, cat_name = get_category_info(origin, cat_url)
    total_count = get_total(origin, cat_id)
    logger.info(f"There are {total_count} products in {cat_name}({cat_id})")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for newest in range(0, total_count, limit):
            url = 'https://{}/api/v4/search/search_items?by=relevancy&limit={}&match_id={}&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2'.format(origin, limit, cat_id, newest)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    all_data = get_neccesary_data(origin, results)
    length = len(all_data)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} products from {cat_name} ({cat_id})")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} products from {cat_name} ({cat_id})")

    return all_data