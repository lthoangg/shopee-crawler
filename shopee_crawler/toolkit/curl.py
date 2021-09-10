import requests
import random
import time

def get_header():
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'content-type': 'text'
    }

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def rwb(func):
        def wrapper(url):
            x = 0
            while True:
                try:
                    return func(url)
                except:
                    if x == retries:
                        raise
                    else:
                        sleep = (backoff_in_seconds * 2 ** x +
                                 random.uniform(0, 1))
                        time.sleep(sleep)
                        x += 1
        return wrapper
    return rwb


@retry_with_backoff()
def curl(url: str, timeout: int=10) -> dict:
    return requests.get(
        url,
        headers=get_header(),
        timeout=timeout
    ).json()