import os


def enable_dev() -> bool:
    dev_enabled = os.getenv('DEV', None)
    return dev_enabled and int(dev_enabled) == 1


def get_headers() -> dict:
    return {'proxy_url': 'socks5h://163.172.152.192:1080'} if enable_dev() \
        else None
