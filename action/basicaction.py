# -*- encoding:utf-8 -*-
from appium import webdriver
import os
import time
import subprocess
import re

class BasicAction():
    def __init__(self, appium_port, udid):
        self.desired_cups = {}
        #设备平台
        self.desired_cups['platformName'] = 'Android'
        #设备名称
        self.desired_cups['deviceName'] = 'pateo'
        apk_activity = os.popen('adb -s {udid} shell dumpsys activity | grep "mFocusedActivity"'.format(udid = udid))
        activity_read = apk_activity.read()
        app_package = re.search('\s(com[\s\S]*?)/', activity_read)
        if app_package != None:
            app_package = app_package.group(1)
        app_activity = re.search('(/[\s\S]*?)\s', activity_read)
        if app_package != None:
            app_activity = app_package.group(1)
        if app_package == None:
            print(os.path.join(os.getcwd(), 'node_modules', 'io.appium.settings', 'apks', 'settings_apk-debug.apk'))
            self.desired_cups['app'] = os.path.join(os.getcwd(), 'node_modules', 'io.appium.settings', 'apks',
                                                    'settings_apk-debug.apk')
        else:
            self.desired_cups['appPackage'] = app_package
            self.desired_cups['appActivity'] = app_activity


        self.udid = udid
        self.desired_cups['udid'] = udid
        self.desired_cups['autoLaunch'] = False
        # self.desired_cups["unicodeKeyboard"] = True
        # self.desired_cups["resetKeyboard"] = True
        self.serive_port = appium_port

        #启动
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

    def click_by_point(self, x, y, duration=10):
        self.driver.tap([(x,y)], duration)

    def find_by_id(self, id):
        try:
            return self.driver.find_element_by_id(id)
        except:
            return False
    def get_child(self, id):
        pass

    def find_by_uiautomator(self, string):
        """new UiSelector().resourceId("com.qinggan.app.radio:id/freq_tv").childSelector(new UiSelector().className("android.widget.TextView").index(0))"""
        self.driver.find_element_by_android_uiautomator(string)


    def get_text_by_id(self, id):
        try:
            find_id = self.driver.find_element_by_id(id)
            text = find_id.text
            return text
        except:
            return False

    def swipe(self, start_x, start_y, end_x, end_y):
        self.driver.swipe(start_x, start_y, end_x, end_y, 500)

    def home(self):
        self.driver.press_keycode(3)

    def back(self):
        self.driver.back()

    def check_key_in_logcat(self, key):
        adb_shell_pipe = subprocess.Popen('adb -s {id} logcat | grep {key}'.format(key=key, id=self.udid), stdout=subprocess.PIPE, shell=True)

    def start_catch_logcat(self):
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
        os.system('adb -s % logcat -c' % self.udid)

        adb_shell_pipe = subprocess.Popen('adb -s %s shell' % self.udid, stdout=subprocess.PIPE, shell=True)
        subprocess.Popen('echo %s > /data/logs/logcat.log' % timestamp, stdin=adb_shell_pipe.stdout,
                                  stdout=subprocess.PIPE)
        subprocess.Popen('echo %s > /data/logs/top.log' % timestamp, stdin=adb_shell_pipe.stdout,
                         stdout=subprocess.PIPE)
        subprocess.Popen('logcat –v threadtime *:V >> /data/logs/logcat.log 2>&1 &', stdin=adb_shell_pipe.stdout,
                         stdout=subprocess.PIPE)
        subprocess.Popen('top -d 20 -n 10000 -b >> /data/logs/top.log 2>&1 &', stdin=adb_shell_pipe.stdout,
                         stdout=subprocess.PIPE)
        time.sleep(1)


    def stop_catch_logcat(self):
        self.stop_process_on_device('logcat')
        self.stop_process_on_device('top')
        log_path = os.path.join('', '')

        if not os.path.exists(log_path):
            os.makedirs(log_path)
        os.system('adb -s %s push /data/logs/logcat.log %s' % (self.udid, os.path.join(log_path, 'logcat.log')))
        os.system('adb -s %s push /data/logs/top.log %s' % (self.udid, os.path.join(log_path, 'top.log')))


    def stop_process_on_device(self, process_name):
        pid_expression = re.compile(r' \d+')
        adb_shell_pipe = subprocess.Popen('adb -s %s shell' %self.udid, stdout=subprocess.PIPE, shell=True)
        result =  subprocess.Popen('ps | grep %s | grep -v grep' % process_name, stdin=adb_shell_pipe.stdout,
                         stdout=subprocess.PIPE)
        for line in result.stdout.readlines():
            for re_result in pid_expression.finditer(str(line)):
                pid = re_result.group()
                subprocess.Popen('kill -9 %s' % pid, stdin=adb_shell_pipe.stdout,
                                 stdout=subprocess.PIPE)
                break
            time.sleep(1)

    def test(self):
        self.click_by_text('导航')
        time.sleep(5)
        search_key = self.driver.find_element_by_id('com.pateonavi.naviapp:id/iv_search_main')
        search_key.click()


if __name__ == '__main__':
    a=BasicAction(4723, '172.17.235.2:5578')
    a.test()