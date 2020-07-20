import kivy
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import random as r
import keyboard as key
import numpy as np
import matplotlib.pyplot as plt

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

highScore = 0


class Game(Widget):
    
    def init(self):
        self.score = 0
        self.snakeHeadX = 390
        self.snakeHeadY = 290
        self.applePos = self.newApple()
        self.posList = [(390, 290)]
        self.dir = 1
        self.firstFrame = True

        Clock.schedule_interval(self.update, 1.0 / 10.0)
        Clock.schedule_interval(self.keys, 1.0 / 60.0)


    def update(self, dt):
        global highScore

        self.canvas.clear()
        self.bgColor = [0, 0, 0, 1]

        self.moveSnake(self.dir)
        self.checkForDeath()

        with self.canvas:
            Color(*self.bgColor)
            Rectangle(pos = (0, 0), size = (self.width, self.height))

            Color(0, 1, 0, 0.9)
            i = 0
            while i < len(self.posList):
                Rectangle(pos = self.posList[i], size = (10, 10))
                i += 1

            Color(1, 0, 0, 0.9)
            Rectangle(pos = self.applePos, size = (10, 10))         
            
        if self.score > highScore:
            highScore = self.score
        
        self.firstFrame = False


    def newApple(self):
        global last_reward
        appleX = r.randint(0, 79)
        appleY = r.randint(0, 59)
        applePos = (appleX*10, appleY*10)

        return applePos

    def moveSnake(self, direction):
        global last_reward

        if direction == 1:
            velX = 0
            velY = 10
        elif direction == 2:
            velX = -10
            velY = 0
        elif direction == 3:
            velX = 0
            velY = -10
        elif direction == 4:
            velX = 10
            velY = 0
        
        oldSnakePos = self.posList[0]
        self.newSnakePos = (oldSnakePos[0]+velX, oldSnakePos[1]+velY)
        self.posList.insert(0, self.newSnakePos)

        if len(self.posList) > self.score + 1:
            del self.posList[self.score+1]

        if self.newSnakePos == self.applePos:
            self.applePos = self.newApple()
            self.score += 1
            last_reward = 1


    def checkForDeath(self):

        if self.newSnakePos[0] < 0 or self.newSnakePos[0] > 790:
            self.death()
        elif self.newSnakePos[1] < 0 or self.newSnakePos[1] > 590:
            self.death()
        
        i = 0
        while i < len(self.posList):
            j = 0
            while j < len(self.posList):
                if i != j:
                    if self.posList[i] == self.posList[j]:
                        self.death()
                j += 1
            i += 1

    
    def keys(self, dt):
        if key.is_pressed('up'):
            if self.dir != 3:
                self.dir = 1
        if key.is_pressed('left'):
            if self.dir != 4:
                self.dir = 2
        if key.is_pressed('down'):
            if self.dir != 1:
                self.dir = 3
        if key.is_pressed('right'):
            if self.dir != 2:
                self.dir = 4

    def death(self):
        self.score = 0
        self.posList = [(390, 290)]
        self.bgColor = [0.5, 0, 0, 1]
        self.applePos = self.newApple()


class SnakeApp(App):
    def build(self):
        game = Game()
        game.init()

        return game

if __name__ == '__main__':
    SnakeApp().run()
