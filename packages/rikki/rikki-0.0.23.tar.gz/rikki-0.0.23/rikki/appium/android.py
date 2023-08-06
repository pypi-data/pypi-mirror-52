from rikki.appium.common import AppiumUtils, Direction
from rikki.behave.context import Context


class AppiumAndroidEspressoUtils(AppiumUtils):

    def swipe(self, context: Context, direction: Direction):
        if direction == Direction.UP:
            context.browser.execute_script('mobile: swipe', {'element': 2, 'direction': 'up'})
        if direction == Direction.DOWN:
            context.browser.execute_script('mobile: swipe', {'element': 2, 'direction': 'down'})
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            assert False, "Directions START and END are not supported yet"

    def support(self, context: Context) -> bool:
        platform = context.browser.desired_capabilities['platformName']
        automation = context.browser.desired_capabilities['automationName']

        return platform == "Android" and automation == "Espresso"


