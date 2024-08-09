import config
import time

from conditions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

def actions():
    return ActionChains(config.browser)


class WaitingFinder(object):

    def __init__(self):
        self.locator = None
        self.default_conditions = {}

    def finder(self):
        pass

    def __getattr__(self, item):
        for condition_class, condition_args in self.default_conditions.items():
            self.assure(condition_class, *condition_args)
        return getattr(self.finder(), item)

    def assure(self, condition_class, *condition_args):
        condition = condition_class(self, *condition_args)
        WebDriverWait(config.browser, config.timeout).until(condition, condition)
        return self

    def __str__(self):
        return self.locator


class RootSElement(object):
    def __getattr__(self, item):
        return getattr(config.browser, item)


class SmartElement(WaitingFinder):
    def __init__(self, css_selector, context=RootSElement()):
        self.locator = css_selector
        self.context = context
        self.default_conditions = {visible: []}

    def __str__(self):
        return f'Context: {self.context}/nLocator: {self.locator}'

    def finder(self):
        return self.context.find_element_by_css_selector(self.locator)

    def within(self, context):
        self.context = context
        return self

    def s(self, css_locator):
        return SmartElement(css_locator, self)

    def left_click(self):
      #  time.sleep(1)
        self.click()
        return self

    def set_value(self, new_text_value):
        self.send_keys(new_text_value)
        return self

    def press_enter(self):
        self.send_keys(Keys.ENTER)
        return self
    
    def get_value(self, attribute):
        return self.get_attribute(attribute)

    def press_esc(self):
        self.send_keys(Keys.ESCAPE)
        return self