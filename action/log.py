# coding:utf-8
# 作者：    Han Sanyang
# 创建时间：2019/3/21 17:28
# 文件名：  log

import time
import os
import serial
import subprocess

def adb_log():
    cmd_string = 'adb shell logcat'
    run_server = subprocess.Popen(cmd_string, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    while True:
        line = run_server.stdout.readline()
        if line == b'' and run_server.poll() != None:
            break
        else:
            print(line)

def open_serial(portx, bps, timex):
    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    # 打开串口，并得到串口对象
    ser = serial.Serial(portx, bps, timeout=timex, write_timeout=5)
    return ser

def serial_log(portx, bps, timex, timeout):
    ser = open_serial(portx, bps, timex)
    ser.write('logcat -c\n'.encode())
    time.sleep(1)
    ser.write('logcat\n'.encode())
    time.sleep(timeout)
    ser.write(0x03)
    time.sleep(2)
    ser.write('\n'.encode())
    time.sleep(2)
    ser.read(1)
    print(ser.read(ser.in_waiting).decode())

def check_list(string, list):
    for key in list:
        print(key.decode())
        if string in key.decode():
            return True
    return False

def keep_in_screen(string, activity, portx, bps):
    '''
    dumpsys activity 查看界面是否在测试界面，如果不存在am start activity界面
    keep_in_screen('wifi', 'com.qinggan.app.launcher/.wifi.WifiListActivity', "COM5", 115200)
    :return: None
    '''
    try:
        timex = 2
        ser = open_serial(portx, bps, timex)
        while True:
            ser.write('dumpsys activity | grep "mFocusedActivity"\n'.encode())
            time.sleep(5)
            wifi_screen = ser.readlines()
            result = check_list(string, wifi_screen)
            if result ==False:
                command = 'am start %s\n' % activity
                ser.write(command.encode())
                time.sleep(10)
                for line in ser.readlines():
                    print(line.decode())
        ser.close()  # 关闭串口
    except Exception as e:
        print("---异常---：", e)

def read_df_log(path):
    log_file_path = os.path.join(path, 'df.log')
    data_file_path = os.path.join(path, 'data.log')
    dp = open(data_file_path, 'a+')
    with open(log_file_path, 'rb') as fp:
        lines = fp.readlines()
        # print(lines)
        for line in lines:
            if 'timestamp' in str(line):
                timestamp = str(line.decode().replace('\n', '')) + ' '
            if '/data ' in str(line):
                dp.write(timestamp + str(line.decode()))
    dp.close()


if __name__ == '__main__':
    # read_log('F:\\h6n\\hsy\\report\\logcat.log')
    # switch_naviapp_music("COM5", 115200)
    # com.qinggan.app.launcher/.bluetooth.BluetoothListActivity
    # com.qinggan.app.launcher/.wifi.WifiListActivity
    keep_in_screen('wifi', 'com.qinggan.app.launcher/.wifi.WifiListActivity', "COM5", 115200)