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

data = crawl_by_shop_url('shop_url')
# print(data)
```

* Crawl by category url
```python
from shopee_crawler import crawl_by_cat_url

data = crawl_by_cat_url('cat_url')
# print(data)
```