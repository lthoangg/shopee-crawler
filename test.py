import time
from shopee_crawler.crawler import crawl_by_cat_url, crawl_by_shop_url, crawl_by_search

keyword='điện thoại samsung'

# Start time
start = time.time()

# Crawl
crawl_by_search(keyword=keyword)

# End time
end = time.time()

# Time crawling
print("Time : ",end - start, "seconds")





