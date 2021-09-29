import unittest
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from appiumbase.fixtures.base_case import BaseCase
import pytest


class Demo_test(BaseCase):
    @pytest.mark.test1
    def test_demo(self):
        000000000000000000000
        self.click("//*[@text='Mulai Sekarang']")

class Untitled(BaseCase):
    def testUntitled(self):
        self.launch()
        self.click()
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='android.widget.EditText']")))
        self.driver.find_element_by_xpath("xpath=//*[@class='android.widget.EditText']").send_keys('844')
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='android.widget.EditText']")))
        self.driver.find_element_by_xpath("xpath=//*[@class='android.widget.EditText']").send_keys('2345167')
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
            (By.XPATH, "//*[@class='android.view.ViewGroup' and ./*[@text='SELANJUTNYA']]")))
        self.driver.find_element_by_xpath("xpath=//*[@class='android.view.ViewGroup' and ./*[@text='SELANJUTNYA']]").send_keys('1234123456')
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='android.widget.ImageView' and ./parent::*[@class='android.view.ViewGroup'] and (./preceding-sibling::* | ./following-sibling::*)[@text='Moderate']]")))
        self.driver.find_element_by_xpath("xpath=//*[@class='android.widget.ImageView' and ./parent::*[@class='android.view.ViewGroup'] and (./preceding-sibling::* | ./following-sibling::*)[@text='Moderate']]").click()

    def tearDown(self):
        self.driver.quit()

    if __name__ == '__main__':
        unittest.main()
