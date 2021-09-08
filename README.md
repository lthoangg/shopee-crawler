# Shopee-crawler
This is a crawl tool.

## Requirement
```env
python>=3.7
```

## Install

* Using `setup.py`
```
python/python3 setup.py install
```

* Using `pip`
```
pip install shopee-crawler
```

## How to use
```python
from shopee_crawler import crawl_by_shop_url

data = crawl_by_shop_url('shop_url')
print(data)
```
