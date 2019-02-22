# -*- encoding:utf-8 -*-
import unittest
from appium import webdriver
import os
import time

class Login(unittest.TestCase):
    def setUp(self):
        desired_cups = {}
        #设备平台
        desired_cups['platformName'] = 'Android'
        #设备名称
        desired_cups['deviceName'] = 'pateo'

        desired_cups['appPackage'] = 'com.qinggan.app.setting'
        desired_cups['appActivity'] = 'com.qinggan.app.setting.activity.MainActivity'

        #启动app
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_cups)

        #启动app时，需要一定时间进入引导页，所以必须设置等待时间，不然下面会一直报错定位不到元素
        time.sleep(5)

    def tearDown(self):
        self.driver.find_element_by_xpath('//android.widget.LinerLayout[@id="com.grandsoft.intercom:id/mainLayout"]/View[1]/ImageButton')
        self.driver.find_element_by_id('com.grandsoft.intercom:id/tv_left_menu_title').click()
        self.driver.find_element_by_id('com.grandsoft.intercom:id/account_edit').clear()
        self.driver.find_element_by_id('com.grandsoft.intercom:id/key_edit').clear()
        self.driver.quit()

    def test_login(self):
        username = self.driver.find_element_by_id('com.grandsoft.intercom:id/account_edit')
        #username.clear()
        username.send_keys('13417842429')
        password = self.driver.find_element_by_id('com.grandsoft.intercom:id/key_edit')
        #password.clear()
        password.send_keys('123456789')
        self.driver.find_element_by_id('com.grandsoft.intercom:id/login_button').click()
        title = self.driver.find_element_by_id('com.grandsoft.intercom:id/toolTitle')
        if title is not None:
            print('login is success')
        else:
            print('login is false')

if __name__ == '__main__':
    unittest.main()