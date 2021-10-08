from appium.webdriver.appium_service import AppiumService
appium_service = AppiumService()
from appiumbase import config as ab_config

def start_appium_service():
    if (appium_service.is_running() and appium_service.is_listening()):
        pass
        #appium service is already running and listening
    else:
        appium_service.start()
    ab_config.appium_server_running = appium_service.is_listening()

def stop_appium_service():
    appium_service.stop()
