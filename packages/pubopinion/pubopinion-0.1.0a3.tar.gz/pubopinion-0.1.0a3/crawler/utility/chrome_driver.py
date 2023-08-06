import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from crawler.settings import WEB_DRIVER


class ChromeBrowser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=WEB_DRIVER)

    def close_web_driver(self):
        self.driver.quit()

    def get(self, request, crawler=None):
        d = self.driver
        d.get(request.url)


if __name__ == '__main__':
    driver = webdriver.Chrome(WEB_DRIVER)  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/')
    time.sleep(5)  # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5)  # Let the user actually see something!
    driver.quit()
