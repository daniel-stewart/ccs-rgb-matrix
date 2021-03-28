from PIL import Image, ImageSequence, ImagePalette
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime
import time
import random

class MatrixGifPlayer(MatrixBase):
    def __init__(self, level):
        self.level = level
    
    def initialize(self, width, height, doubleBuffer):
        self.gifList = [
            '/home/pi/ccs-rgb-matrix/icons/blobbo.gif',
            #'/home/pi/ccs-rgb-matrix/icons/sine_tube.gif',
            '/home/pi/ccs-rgb-matrix/icons/flag64x32RGB.gif',
            #'/home/pi/ccs-rgb-matrix/icons/wizardBoy.gif',
            '/home/pi/ccs-rgb-matrix/icons/matrix.gif',
            '/home/pi/ccs-rgb-matrix/icons/heart2.gif',
            '/home/pi/ccs-rgb-matrix/icons/box2.gif',
            '/home/pi/ccs-rgb-matrix/icons/burger4.gif',
            '/home/pi/ccs-rgb-matrix/icons/heart5.gif',
            '/home/pi/ccs-rgb-matrix/icons/bricks.gif',
            '/home/pi/ccs-rgb-matrix/icons/circles-menu.gif',
            #'/home/pi/ccs-rgb-matrix/icons/angel.gif',
            #'/home/pi/ccs-rgb-matrix/icons/laughing.gif',
            #'/home/pi/ccs-rgb-matrix/icons/wink.gif',
            '/home/pi/ccs-rgb-matrix/icons/candy.gif',
            '/home/pi/ccs-rgb-matrix/icons/star.gif',
            '/home/pi/ccs-rgb-matrix/icons/wifi.gif',
            '/home/pi/ccs-rgb-matrix/icons/explode2.gif',
            '/home/pi/ccs-rgb-matrix/icons/0rain.gif',
            '/home/pi/ccs-rgb-matrix/icons/0robotfactory.gif',
            '/home/pi/ccs-rgb-matrix/icons/0tree.gif',
            '/home/pi/ccs-rgb-matrix/icons/amigaball.gif',
            '/home/pi/ccs-rgb-matrix/icons/amigaball2.gif',
            '/home/pi/ccs-rgb-matrix/icons/balloon2.gif',
            '/home/pi/ccs-rgb-matrix/icons/bike.gif',
            '/home/pi/ccs-rgb-matrix/icons/bluerobin.gif',
            '/home/pi/ccs-rgb-matrix/icons/bubbles.gif',
            '/home/pi/ccs-rgb-matrix/icons/demo.gif',
            '/home/pi/ccs-rgb-matrix/icons/earth.gif',
            '/home/pi/ccs-rgb-matrix/icons/gameboy1.gif',
            '/home/pi/ccs-rgb-matrix/icons/gameboy2.gif',
            '/home/pi/ccs-rgb-matrix/icons/heartbeat.gif',
            '/home/pi/ccs-rgb-matrix/icons/mfrog_mixedmedia.gif',
            '/home/pi/ccs-rgb-matrix/icons/orangeball.gif',
            '/home/pi/ccs-rgb-matrix/icons/pong.gif',
            '/home/pi/ccs-rgb-matrix/icons/rainfast.gif',
            '/home/pi/ccs-rgb-matrix/icons/rainmbowcube.gif',
            '/home/pi/ccs-rgb-matrix/icons/rspray.gif',
            '/home/pi/ccs-rgb-matrix/icons/sakura.gif',
            '/home/pi/ccs-rgb-matrix/icons/shuttle.gif',
            '/home/pi/ccs-rgb-matrix/icons/squid.gif',
            '/home/pi/ccs-rgb-matrix/icons/sunny.gif',
            '/home/pi/ccs-rgb-matrix/icons/treasurechest.gif',
            '/home/pi/ccs-rgb-matrix/icons/triball.gif',
            '/home/pi/ccs-rgb-matrix/icons/usnowy.gif',
            '/home/pi/ccs-rgb-matrix/icons/water_tub.gif',
            '/home/pi/ccs-rgb-matrix/icons/windmill.gif',
            '/home/pi/ccs-rgb-matrix/icons/worm.gif',
            '/home/pi/ccs-rgb-matrix/icons/fire64x32RGB.gif',
            '/home/pi/ccs-rgb-matrix/icons/invadpt2.gif',
            '/home/pi/ccs-rgb-matrix/icons/galaxian.gif',
        ]
        if self.level == -1:
            self.level = random.randint(0, len(self.gifList)-1)
        self.width = width
        self.height = height
        self.gif = Image.open(self.gifList[self.level%len(self.gifList)])
        if self.gif.width != 32:
            baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0))
        else:
            if self.level > 8:
                baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            else:
                baseImage = Image.new('RGBA', (self.width, self.height), (255,255,255,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
        self.now = time.monotonic()
        doubleBuffer.SetImage(baseImage.convert('RGB'))
        return
    
    def run(self, doubleBuffer):
        if time.monotonic() - self.now > 0.1:
            
            if self.gif.tell() == self.gif.n_frames - 1:
                    self.gif.seek(0)
            else:
                self.gif.seek(self.gif.tell() + 1)
            
            self.now = time.monotonic()
            if self.gif.width != 32:
                baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
                baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0))
            else:
                if self.level > 8:
                    baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
                else:
                    baseImage = Image.new('RGBA', (self.width, self.height), (255,255,255,0))
                baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
            doubleBuffer.SetImage(baseImage.convert('RGB'))
            return True
        else:
            return False