# -*- encoding:utf-8 -*-
from appium import webdriver
import os
import time

class BasicAction():
    def __init__(self, appium_port, udid):
        self.desired_cups = {}
        #设备平台
        self.desired_cups['platformName'] = 'Android'
        #设备名称
        self.desired_cups['deviceName'] = 'pateo'

        # self.desired_cups['appPackage'] = 'com.qinggan.app.setting'
        # self.desired_cups['appActivity'] = 'com.qinggan.app.setting.activity.MainActivity'
        PATH = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        # self.desired_cups['app'] = PATH('D:\\pyworkspace\\pateo_test\\apk\\app-debug.apk')
        print(os.path.join(script_path, '..', 'apk', 'app-debug.apk'))
        self.desired_cups['app'] = os.path.join(script_path, '..', 'apk', 'app-debug.apk')
        self.desired_cups['udid'] = udid
        self.desired_cups['autoLaunch'] = False
        self.serive_port = appium_port
        # desired_cups

        #启动app
        self.driver = webdriver.Remote('http://localhost:%s/wd/hub'%(self.serive_port),self.desired_cups)

        #启动app时，需要一定时间进入引导页，所以必须设置等待时间，不然下面会一直报错定位不到元素
        time.sleep(5)

    def tearDown(self):
        pass

    def click_by_text(self, text):
        find_text = self.driver.find_element_by_android_uiautomator('text("{text}")'.format(text=text))
        find_text.click()

    def click_by_id(self, id):
        find_id = self.driver.find_element_by_id(id)
        find_id.click()

    def swipe(self, start_x, start_y, end_x, end_y):
        self.driver.swipe(start_x, start_y, end_x, end_y)



    def test(self):
        self.click_by_text('导航')
        time.sleep(5)
        search_key = self.driver.find_element_by_id('com.pateonavi.naviapp:id/iv_search_main')
        search_key.click()


if __name__ == '__main__':
    a=BasicAction(4723, '172.17.235.2:5578')
    a.test()