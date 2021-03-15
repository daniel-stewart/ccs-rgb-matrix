import time
import random
from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
PINK = (255, 128, 128)
BLACK = (0, 0, 0)

'''
There will be a list that has:
        * An image list (from which one will be chosen randomly) with x and y coords
        * A series of (x,y) & text strings in  a tuple
            * (x, y, "Text String", font_path, color)
Example:
        [ [(3, 6, '/home/pi/icons/PixelArtIconPack/Helm03.png',), (16, 15, "Hello World", "/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf", GREEN)] ]
'''

class MatrixImagePlayground(MatrixBase):
    def __init__(self, level):
        if level == -1:
          self.level = random.randint(1,4)
        else:
          self.level = level
        now = datetime.now()
        if self.level == -2:
        # What day is it?
          if now.weekday() == 1:
              self.level = 9
          elif now.weekday() == 2:
              self.level = 5
          elif now.weekday() == 3:
              self.level = 6
          elif now.weekday() == 4:
              self.level = 8
          elif now.weekday() == 5:
              self.level = 7
          else:
              self.level = random.randint(1,4)
    
    def initialize(self, width, height, double_buffer):
        entries = [
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/CCSKnight.png'),),
              (33, 12, 'Go', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE),
              (23, 28, 'Knights', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE) ],
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/cupcake2.png'),),
              (23, 14, 'Need a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),
              (3, 28, 'Cupcake?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/lightbulb.png'),),
              (48, 10, 'I', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (37, 21, 'have', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (15, 32, 'an idea!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            [ ((37,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/juice-carton.png'),),
              (0, 9, 'Orange', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (9, 20, 'juice', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 29, 'is good!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),],
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/onion-rings.png'),),
              (0, 9, 'Mmm...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', BLUE),
              (0, 20, 'Onion', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 29, 'Rings!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            [ ((36,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/straw-drink.png'),),
              (0, 12, 'Tropical', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),
              (0, 28, 'Smoothie!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            [ ((36,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/chicken-strips.png'),),
              (0, 12, 'Chik-', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, 'Fil-A!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/pizza32x32.png'),),
              (0, 15, 'Pizza!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/taco32x32.png'),),
              (0, 15, 'Taco', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 28, 'Day!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/sandwich32x32.png'),),
              (0, 20, 'Panera', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
        ]

        fontList = set({})
        for entry in entries:
            numEntries = len(entry)
            for i in range(1,numEntries):
                fontList.add(entry[i][3])
        fonts = dict({})
        for font in fontList:
            print(font)
            f = graphics.Font()
            f.LoadFont(font)
            fonts[font] = f
        print(fonts.values())
        self.level = self.level % len(entries)
        icon = random.randint(0, len(entries[self.level][0])-1)
        print(entries[self.level][0])
        baseImage = Image.new('RGBA', (32, 32), (0,0,0,0))
        image = Image.open(entries[self.level][0][icon][2])
        baseImage.alpha_composite(image, (0,0))
        baseImage = baseImage.convert('RGB')
        double_buffer.SetImage(baseImage, entries[self.level][0][icon][0], entries[self.level][0][icon][1])
        for i in range(1, len(entries[self.level])):
            entry = entries[self.level][i]
            print(entry[3])
            print(fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(double_buffer, fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        return
        
    def run(self, double_buffer):
        return False
