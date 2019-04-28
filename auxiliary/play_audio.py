# coding:utf-8
# 作者：    Han Sanyang
# 创建时间：2019/4/28 16:43
# 文件名：  play_audio

'''
播放音频文档
'''


import pygame
import os
import time

def play_audio(path, file):
    pygame.mixer.init()
    file_path = os.path.join(path, file)
    print("播放：%s"%file)
    time_data = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print('开始时间：%s'%time_data)
    track = pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    busy_flag = pygame.mixer.music.get_busy()
    while busy_flag ==1:
        time.sleep(1)
        busy_flag = pygame.mixer.music.get_busy()
    time_data = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print('结束时间：%s' % time_data)
    pygame.mixer.music.stop()