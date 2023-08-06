import random
import os

class SayLove(object):
    def __init__(self):
      current_path = '/'.join(__file__.split('/')[:-1])
      with open('{}/love_quotes'.format(current_path)) as love_file:
        self.data = love_file.readlines()

    def say(self):
      print(random.choices(self.data)[0].strip("\n"))

