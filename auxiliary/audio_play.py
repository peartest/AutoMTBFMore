# coding:utf-8
import pyttsx3

class AudioPlay():

    def __init__(self):
        self.engine = pyttsx3.init()


    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    a=AudioPlay()
    a.say('小度小度')
