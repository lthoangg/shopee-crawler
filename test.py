import time
import unittest
from shopee_crawler import Crawler

class TestCrawlingMethods(unittest.TestCase):
    crawler = Crawler()
    crawler.set_origin("shopee.vn")
    
    def test_crawl_by_cat_url(self):
        url = "https://shopee.vn/M%C3%A1y-T%C3%ADnh-Laptop-cat.11035954"
        
        self.assertTrue(type(self.crawler.crawl_by_cat_url(url)) is list)

    def test_crawl_by_shop_url(self):
        url = "https://shopee.vn/lg_official_store"
        self.assertTrue(type(self.crawler.crawl_by_shop_url(url)) is list)

    def test_crawl_by_search(self):
        keyword = "điện thoại samsung"
        self.assertTrue(type(self.crawler.crawl_by_search(keyword)) is list)

    def test_crawl_cat_list(self):
        self.assertTrue(type(self.crawler.crawl_cat_list()) is list)

if __name__ == '__main__':
    # Start time
    start = time.time()

    # Start testing
    unittest.main()

    # End time
    end = time.time()

    # Time testing
    print("Time : ",end - start, "seconds")