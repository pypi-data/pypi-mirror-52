from selenium.webdriver.remote.webdriver import WebDriver

from rikki.appium.common import AppiumUtils, Direction


class AppiumAndroidEspressoUtils(AppiumUtils):

    def swipe(self, direction: Direction):
        if direction == Direction.UP:
            self._driver.execute_script('mobile: swipe', {'element': 2, 'direction': 'up'})
        if direction == Direction.DOWN:
            self._driver.execute_script('mobile: swipe', {'element': 2, 'direction': 'down'})
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            assert False, "Directions START and END are not supported yet"

    def support(self, driver: WebDriver) -> bool:
        platform = driver.desired_capabilities['platformName']
        automation = driver.desired_capabilities['automationName']

        return platform == "Android" and automation == "Espresso"


