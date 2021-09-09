# Shopee-crawler
This is a crawl tool.

## Requirement
```env
python>=3.7
```

## Install

* Using `setup.py`
```
git clone https://github.com/lthoangg/shopee-crawler
python/python3 setup.py install
```

* Using `pip`
```
pip install shopee-crawler
```

## How to use
* Crawl by shop url
```python
from shopee_crawler import crawl_by_shop_url

data = crawl_by_shop_url(shop_url='shop_url')
# print(data)
```

* Crawl by category url
```python
from shopee_crawler import crawl_by_cat_url

data = crawl_by_cat_url(cat_url='cat_url')
# print(data)
```

* Crawl by keyword (search)
```python
from shopee_crawler import crawl_by_search

data = crawl_by_search(keyword='keyword')
# print(data)
```

## Usage
- About 12000 rows (products) in 2-3 seconds (32 workers)

- About 12000 rows (products) in 5-6 seconds (16 workers)

## Test yourself

```python
import time
from shopee_crawler.crawler import crawl_by_search

keyword='điện thoại samsung'

# Start time
start = time.time()

# Crawl
crawl_by_search(keyword=keyword)

# End time
end = time.time()

# Time crawling
print("Time : ",end - start, "seconds")

```