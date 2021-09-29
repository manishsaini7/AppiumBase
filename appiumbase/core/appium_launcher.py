from appium.webdriver.appium_service import AppiumService

appium_service = AppiumService()


def launch_appium_service():
    appium_service.start()

