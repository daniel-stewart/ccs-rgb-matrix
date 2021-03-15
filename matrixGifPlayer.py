from PIL import Image, ImageSequence, ImagePalette
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime
import time

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
        ]
        self.width = width
        self.height = height
        self.gif = Image.open(self.gifList[self.level%len(self.gifList)])
        if self.gif.width != 32:
            baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0))
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
                baseImage = Image.new('RGBA', (self.width, self.height), (255,255,255,0))
                baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
            doubleBuffer.SetImage(baseImage.convert('RGB'))
            return True
        else:
            return False