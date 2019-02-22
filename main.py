# coding:utf-8

from pateo_test.service.start_service import StartService
from pateo_test.action.basicaction import BasicAction
import time

a = StartService(4723)
a.start()
time.sleep(5)

b=BasicAction(4723, '172.17.235.4:5578')
while True:
    id_list = ['com.qinggan.app.messagecenter:id/widget_weather_icon', 'com.qinggan.now.ui:id/navi_default_road_name',
               'com.qinggan.app.music:id/title','']
    b.click_by_id('com.qinggan.app.messagecenter:id/widget_weather_icon')
    time.sleep(5)
    b.click_by_id('com.pateonavi.naviapp:id/iv_search_main')





