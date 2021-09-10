from .curl import curl
import concurrent.futures


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_total():
    url = "https://banhang.shopee.vn/help/api/v3/global_category/list/?page=1&size=16"

    return curl(url)['data']['total']

def get_all_data(url):
    data = curl(url)['data']
    results = []
    try:
        for d in data['global_cats']:
            results.append(d)
    except Exception as e:
        # logger.error(e)
        pass

    return results

def crawl_cat_list(limit:int=16, max_workers:int=32) -> list:

    total_count = get_total()
    pages = (total_count // limit) + 1
    logger.info(f"There are {total_count} categories")
    futures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(1, pages+1):
            url = "https://banhang.shopee.vn/help/api/v3/global_category/list/?page={}&size={}".format(page, limit)
            futures.append(executor.submit(get_all_data, url))

    for future in concurrent.futures.as_completed(futures):
        results.extend(future.result())
        
    length = len(results)
    if length == total_count:
        logger.info(f"Successfully crawl all {total_count} categories")
    elif length < total_count:
        logger.info(f"Successfully crawl {length} categories")

    return results