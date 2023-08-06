import time
from selenium import webdriver
from collections import Counter


class GuessLogo:

    option = webdriver.ChromeOptions()
    option.add_argument("headless")

    @staticmethod
    def guess_logo_by_favicon(browser):
        try:
            item = browser.find_element_by_xpath("//link[contains(@href, 'favicon')]")
            return item.get_attribute('href')
        except Exception:
            return None
        

    @staticmethod
    def guess_logo_by_img_url(browser):
        try:
            patterns = [
                "contains(@*, 'logo')",
                "contains(@class, 'logo')",
                "contains(@*, 'Logo')",
                "contains(@class, 'Logo')",
            ]
            xpath = "//img[%s]" % " or ".join(patterns)
            item = browser.find_element_by_xpath(xpath)
            return item.get_attribute('src')
        except Exception:
            return None

    @staticmethod
    def guess_logo_by_parent(browser):
        try:
            patterns = [
                "contains(@*, 'logo')",
                "contains(@class, 'logo')",
                "contains(@*, 'Logo')",
                "contains(@class, 'Logo')",
            ]
            xpath = "//a|//div[%s]" % " or ".join(patterns)
            item = browser.find_element_by_xpath(xpath)
            return item.find_element_by_xpath('//img').get_attribute('src')
        except Exception:
            return None

    @classmethod
    def guess(cls, url):
        if not url.startswith("http"):
            url = 'http://' + url

        browser = webdriver.Chrome(chrome_options=cls.option)

        browser.get(url)
        time.sleep(3)

        logos = []

        logos.append(cls.guess_logo_by_favicon(browser))
        logos.append(cls.guess_logo_by_img_url(browser))
        logos.append(cls.guess_logo_by_parent(browser))

        logos = list(filter(lambda item: item, logos))
        browser.close()
        return dict(Counter(logos))