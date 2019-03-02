# -*- encoding:utf-8 -*-

import os
import threading
import subprocess

class StartService(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def start_appium_server(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        main_js_path = os.path.join(script_path, '..', 'node_modules', 'appium', 'build', 'lib', 'main.js')
        cmd_string = 'node %s --address 0.0.0.0 --port %s' % (main_js_path, self.port)
        run_server = subprocess.Popen(cmd_string,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            line = run_server.stdout.readline()
            if line == b'' and run_server.poll() != None:
                break
            else:
                pass
                # print(line)

    def run(self):
        self.start_appium_server()



if __name__ == '__main__':
    a = StartService(4723)
    a.start()

