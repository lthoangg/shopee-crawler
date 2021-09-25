from .toolkit import (
    crawl_by_cat_url,
    crawl_by_shop_url,
    crawl_by_search,
    crawl_cat_list
)
import requests


class Crawler:
    def __init__(self):
        self.origin = None
        
    def set_origin(self, origin="shopee.vn"):
        """Set origin website for different country

        Args:
            origin (str, optional): Enter your country. Defaults to "shopee.vn".
            
        Example if you want to crawl data from:
            - Vietnam: shopee.vn
            - Indonesia: shopee.co.id
            ... so on and so forth
        """
        if requests.get(f"https://{origin}").status_code == 200:
            self.origin = origin
            return True
        return False
    
    def crawl_cat_list(self):
        return crawl_cat_list(self.origin)
    
    def crawl_by_cat_url(self, cat_url):
        return crawl_by_cat_url(self.origin, cat_url)
    
    def crawl_by_shop_url(self, shop_url):
        return crawl_by_shop_url(self.origin, shop_url)
    
    def crawl_by_search(self, keyword):
        return crawl_by_search(self.origin, keyword)