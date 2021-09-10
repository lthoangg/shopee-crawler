from .curl import curl
from datetime import datetime
import json
import re
import urllib.parse

import concurrent.futures

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_category_info(cat_url):
    cat_url = urllib.parse.unquote(cat_url)
    match = re.search(r'https://shopee.vn/(.+)-cat.(\d+)', cat_url)
    cat_name = match.group(1)
    cat_id = match.group(2)
    return cat_id, cat_name

def get_total(id):
    url = 'https://shopee.vn/api/v4/search/search_items?by=relevancy&limit=60&match_id={}&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2'.format(id)

    return json.loads(curl(url)['search_tracking'])["total_count"]

def get_all_data(url: str) -> list:
    data = curl(url)
    results = []
    try:
        for d in data['items']:
            results.append(d['item_basic'])
    except Exception as e:
        logger.error(e)

    return results

def get_neccesary_data(data: list) -> list:
    results = []
    try:
        for item in data:
            results.append(
                {
                    'product_id': item['itemid'],
                    'product_name': item['name'],
                    'product_image': r'https://cf.shopee.vn/file/{}_tn'.format(item['image']),
                    'product_link': r'https://shopee.vn/{}-i.{}.{}'.format(item['name'], item['shopid'], item['itemid']),
                    'category_id': item['catid'],
                    'label_ids': item['label_ids'],
                    'product_brand': item['brand'],
                    'product_price': item['price'] if item['raw_discount'] == 0 else item['price_before_discount'],
                    'product_discount': item['raw_discount'],
                    'currency': item['currency'],
                    'stock': item['stock'],
                    'sold': item['sold'],
                    'is_on_flash_sale': item['is_on_flash_sale'],
                    'rating_star': item['item_rating']['rating_star'],
                    'rating_count': item['item_rating']['rating_count'],
                    'rating_with_context': item['item_rating']['rcount_with_context'],
                    'rating_with_image': item['item_rating']['rcount_with_image'],
                    'is_freeship': item['show_free_shipping'],
                    'feedback_count': item['cmt_count'],
                    'liked_count': item['liked_count'],
                    'view_count': item['view_count'],
                    'shop_id': item['shopid'],
                    'shop_location': item['shop_location'],
                    'shopee_verified': item['shopee_verified'],
                    'is_official_shop': item['is_official_shop'],
                    'updated_at': item['ctime'],
                    'fetched_time': datetime.timestamp(datetime.utcnow())
                }
            )
    except Exception as e:
        logger.error(e)

    return results

def crawl_by_cat_url(cat_url:str, limit:int=60, max_workers:int=32) -> list:

    cat_id, cat_name = get_category_info(cat_url)
    total_count = get_total(cat_id)
    logger.info(f"There are {total_count} products in {cat_name}({cat_id})")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for newest in range(0, total_count, limit):
            url = 'https://shopee.vn/api/v4/search/search_items?by=relevancy&limit={}&match_id={}&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2'.format(limit, cat_id, newest)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    all_data = get_neccesary_data(results)
    length = len(all_data)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} products from {cat_name} ({cat_id})")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} products from {cat_name} ({cat_id})")

    return all_data