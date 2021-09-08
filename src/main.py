import json
import concurrent.futures 

from crawl_by_shop_url import (
    get_shop_info,
    get_total,
    get_neccesary_data
)


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def crawl_by_shop_url(shop_url:str, limit=30, max_workers=8) -> json:

    shop_id, shop_name = get_shop_info(shop_url)
    total_count = get_total(shop_id)
    logger.info(f"There are {total_count} in {shop_name}({shop_id})")
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
        logger.info(f"Successfully crawl all {total_count} from {shop_name}({shop_id})")
    elif length < total_count:
        logger.info(f"Successfully crawl {total_count} products from {shop_name}({shop_id})")

    return all_data