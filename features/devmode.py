import os


def enable_dev() -> bool:
    dev_enabled = os.getenv('DEV', None)
    return dev_enabled and int(dev_enabled) == 1
