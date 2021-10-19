from appium.webdriver.appium_service import AppiumService
appium_service = AppiumService()
from appiumbase import config as ab_config
import requests

def start_appium_service():
    try:
        res = requests.get("http://0.0.0.0:4723/wd/hub/sessions")
    except requests.exceptions.ConnectionError as e:
        appium_service.start()

def stop_appium_service():
    appium_service.stop()