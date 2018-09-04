import os
from io import BytesIO
from threading import Lock
from time import sleep
from urllib.parse import urlsplit

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


class IllegalURL(Exception):
    pass


class Capturer:
    def __init__(self) -> None:
        self.start_driver()
        self.lock = Lock()

    def start_driver(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

        self.drv = webdriver.Chrome(os.getenv('GOOGLE_CHROME_DRIVER'),
                                    chrome_options=chrome_options)

        self.drv.set_window_size(1280, 1024)
        self.drv.implicitly_wait(5)

    def reboot(self) -> None:
        self.drv.quit()
        self.start_driver()

    @staticmethod
    def check_url(url: str) -> None:
        spl = urlsplit(url)
        if not (spl.netloc in ('n.maps.yandex.ru', 'mapeditor.yandex.com') or
                spl.netloc == 'yandex.ru' and spl.path.startswith('/maps')):
            raise IllegalURL

    def take_screenshot(self, url: str) -> BytesIO:
        self.lock.acquire()
        try:
            self.check_url(url)
            self.drv.get(url)
            self.drv.refresh()
            sleep(4)
        except WebDriverException as e:
            print(e)
            self.reboot()
        finally:
            self.lock.release()
        return BytesIO(self.drv.get_screenshot_as_png())

    def __del__(self) -> None:
        self.drv.quit()
