from .optimizer import retry_with_backoff

@retry_with_backoff()
def curl(url: str, timeout: int=10) -> dict:
    return requests.get(
        url,
        headers=get_header(),
        timeout=timeout
    ).json()