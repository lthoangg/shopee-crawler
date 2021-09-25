from .curl import curl
from datetime import datetime



import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def get_neccesary_data(origin, data: list) -> list:
    results = []
    try:
        for item in data:
            results.append(
                {
                    'product_id': item['itemid'],
                    'product_name': item['name'],
                    'product_image': r'https://cf.{}/file/{}_tn'.format(origin, item['image']),
                    'product_link': r'https://{}/{}-i.{}.{}'.format(origin, item['name'], item['shopid'], item['itemid']),
                    'category_id': item['catid'],
                    'label_ids': item['label_ids'],
                    'product_brand': item['brand'],
                    'product_price': item['price'] if item['raw_discount'] == 0 else item['price_before_discount'],
                    'product_discount': item['raw_discount'],
                    'currency': item['currency'],
                    'stock': item['stock'],
                    'sold': item['historical_sold'],
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
        # logger.error(e)
        pass

    return results