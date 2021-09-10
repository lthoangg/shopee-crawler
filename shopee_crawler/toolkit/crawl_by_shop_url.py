from .curl import curl
from datetime import datetime
import concurrent.futures

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_shop_info(shop_url):
    shop_name = shop_url.split("/")[-1]
    url = f"https://shopee.vn/api/v4/shop/get_shop_detail?username={shop_name}"
    return curl(url)['data']['shopid'], shop_name

def get_total(id):
    url = 'https://shopee.vn/api/v4/search/search_items?by=pop&limit=1&match_id={}&newest=0&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2'.format(id)

    return curl(url)['total_count']

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

def crawl_by_shop_url(shop_url:str, limit:int=60, max_workers:int=32) -> list:
    
    shop_id, shop_name = get_shop_info(shop_url)
    total_count = get_total(shop_id)
    logger.info(f"There are {total_count} products in {shop_name}({shop_id})")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for newest in range(0, total_count, limit):
            url = 'https://shopee.vn/api/v4/search/search_items?by=pop&limit={}&match_id={}&newest={}&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2'.format(limit, shop_id, newest)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    all_data = get_neccesary_data(results)
    length = len(all_data)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} products from {shop_name}({shop_id})")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} products from {shop_name}({shop_id})")

    return all_data