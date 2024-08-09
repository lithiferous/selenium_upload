from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import config
import time

class Condition(object):
    def __call__(self, driver):
        self.driver = driver
        try:
            return self.apply()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def __str__(self):
        try:
            return """
            failed while waiting %s seconds
            for %s found by: %s
            to assert %s%s%s
        """ % (config.timeout,
               self.identity(),
               self.entity(),
               self.__class__.__name__,
               """:
            expected: """ + str(self.expected()) if self.expected() else "",
               """
              actual: """ + str(self.actual()) if self.actual() else "")
        except Exception as e:
            return "\n type: %s \n msg: %s \n" % (type(e), e)

    def identity(self):
        return "element"

    def entity(self):
        return self.element

    def expected(self):
        return None

    def actual(self):
        return None

    def apply(self):
        return False

class visible(Condition):
    def __init__(self, element):
        self.element = element

    def apply(self):
        time.sleep(1)
        return self.element.finder().is_displayed()