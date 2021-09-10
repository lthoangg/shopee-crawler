from .curl import curl
from datetime import datetime
import concurrent.futures


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_total(keyword):
    url = "https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2".format(keyword)

    return curl(url)['total_count']

def get_keyword_encoded(keyword):
    return "%20".join(key for key in keyword.split())

def get_all_data(url: str) -> list:
    data = curl(url)
    results = []
    try:
        for d in data['items']:
            results.append(d['item_basic'])
    except Exception as e:
        # logger.error(e)
        pass

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

def crawl_by_search(keyword:str, limit:int=60, max_workers:int=32) -> list:

    temp = get_keyword_encoded(keyword=keyword)

    total_count = get_total(temp)
    logger.info(f"There are {total_count} products in \"{keyword}\"")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for newest in range(0, total_count, limit):
            url = "https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&limit={}&newest={}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2".format(temp, limit, newest)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    all_data = get_neccesary_data(results)
    length = len(all_data)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} products from \"{keyword}\"")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} products from \"{keyword}\"")

    return all_data