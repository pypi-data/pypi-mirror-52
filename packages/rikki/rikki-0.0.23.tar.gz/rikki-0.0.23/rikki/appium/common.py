from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as conditions
from rikki.behave.context import Context
from typing import Optional
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class AppiumUtils:

    def __init__(self, wait_time: int = 1) -> None:
        super().__init__()
        self.wait_time = wait_time

    def tap(self, context: Context, by: By, locator: str, wait_time: Optional[int] = None):
        wait = self._configure_wait(context, wait_time)
        wait.until(conditions.presence_of_element_located((by, locator))).click()

    def enter(self, context: Context, by: By, locator: str, text: str, wait_time: Optional[int] = None):
        wait = self._configure_wait(context, wait_time)
        wait.until(conditions.presence_of_element_located((by, locator))).send_keys(text)

    def wait(self, context: Context, by: By, locator: str, wait_time: Optional[int] = None):
        wait = self._configure_wait(context, wait_time)
        wait.until(by, locator)

    def swipe(self, context: Context, direction: Direction):
        assert False, "Swipe is not supported:"

    def _configure_wait(self, context: Context, wait_time: Optional[int] = None):
        delay = self.wait_time
        if wait_time:
            delay = wait_time
        return WebDriverWait(context.browser, delay)

    def support(self, context: Context) -> bool:
        """
        :param context:
        :return: True if this instance of the utils support the context
        """
        return True
