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
        self.origLevel = level
        if level == -1:
          self.level = random.randint(1,4)
        elif level == -3:
          self.level = random.randint(11,15)
        else:
          self.level = level
        now = datetime.now()
        if self.level == -2:
          # What day is it?
          print("Today is", now.weekday())
          if now.weekday() == 0:
              self.level = 9
          elif now.weekday() == 1:
              self.level = 5
          elif now.weekday() == 2:
              self.level = 6
          elif now.weekday() == 3:
              self.level = 8
          elif now.weekday() == 4:
              self.level = 7
          else:
              self.level = random.randint(1,4)
    
    def initialize(self, width, height, double_buffer):
        self.entries = [
            #0
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/CCSKnight.png'),),
              (33, 12, 'Go', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE),
              (23, 28, 'Knights', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE) ],
            #1
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/cupcake2.png'),),
              (23, 14, 'Need a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),
              (3, 28, 'Cupcake?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            #2
            [ ((0,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/lightbulb.png'),),
              (48, 10, 'I', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (37, 21, 'have', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (15, 32, 'an idea!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            #3
            [ ((37,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/juice-carton.png'),),
              (0, 9, 'Orange', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (9, 20, 'juice', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 29, 'is good!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),],
            #4
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/onion-rings.png'),),
              (0, 9, 'Mmm...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', BLUE),
              (0, 20, 'Onion', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 29, 'Rings!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            #5
            [ ((36,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/straw-drink.png'),),
              (0, 12, 'Tropical', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),
              (0, 28, 'Smoothie!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            #6
            [ ((36,0,'/home/pi/ccs-rgb-matrix/icons/MVIconsPixelDailies/chicken-strips.png'),),
              (0, 12, 'Chick-', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, 'Fil-A!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #7
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/pizza32x32.png'),),
              (0, 15, 'Pizza!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #8
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/subsandwich.png'),),
              (0, 15, 'Jersey', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 28, "Mike's", '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #9
            [ ((32,0,'/home/pi/ccs-rgb-matrix/icons/sandwich32x32.png'),),
              (0, 20, 'Panera', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #10
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/christmas_tree.png'),),
              (0, 15, 'Merry', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, 'Christmas!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #11
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/school.png'),),
              (0, 15, 'Welcome', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),
              (0, 28, 'to CCS!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),],
            #12
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/education.png'),),
              (0, 15, 'School', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 28, 'Again...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),],
            #13
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/thumbsUp.png'),),
              (0, 15, 'Have a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, 'Great Day!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #14
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/youreback.png'),),
              (0, 15, "You're", '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 28, 'Back!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #15
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/checked.png'),),
              (0, 15, 'Ready for', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),
              (0, 28, 'the Day?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            #16
            [ ((32, 0, '/home/pi/ccs-rgb-matrix/icons/valentines-day.png'),),
              (0, 15, 'Valentines', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, 'Day!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
        ]

        fontList = set({})
        for entry in self.entries:
            numEntries = len(entry)
            for i in range(1,numEntries):
                fontList.add(entry[i][3])
        self.fonts = dict({})
        for font in fontList:
            print(font)
            f = graphics.Font()
            f.LoadFont(font)
            self.fonts[font] = f
        print(self.fonts.values())
        self.level = self.level % len(self.entries)
        icon = random.randint(0, len(self.entries[self.level][0])-1)
        print(self.entries[self.level][0])
        baseImage = Image.new('RGBA', (32, 32), (0,0,0,0))
        image = Image.open(self.entries[self.level][0][icon][2])
        baseImage.alpha_composite(image, (0,0))
        baseImage = baseImage.convert('RGB')
        double_buffer.SetImage(baseImage, self.entries[self.level][0][icon][0], self.entries[self.level][0][icon][1])
        for i in range(1, len(self.entries[self.level])):
            entry = self.entries[self.level][i]
            print(entry[3])
            print(self.fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(double_buffer, self.fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        return
    
    def restart(self, doubleBuffer):
        if self.origLevel == -1:
          self.level = random.randint(1,4)
        elif self.origLevel == -3:
          self.level = random.randint(11,15)
        else:
          self.level = self.origLevel
        now = datetime.now()
        if self.level == -2:
        # What day is it?
          print("Today is", now.weekday())
          if now.weekday() == 0:
              self.level = 9
          elif now.weekday() == 1:
              self.level = 5
          elif now.weekday() == 2:
              self.level = 6
          elif now.weekday() == 3:
              self.level = 8
          elif now.weekday() == 4:
              self.level = 7
          else:
              self.level = random.randint(1,4)
        icon = random.randint(0, len(self.entries[self.level][0])-1)
        print(self.entries[self.level][0])
        baseImage = Image.new('RGBA', (32, 32), (0,0,0,0))
        image = Image.open(self.entries[self.level][0][icon][2])
        baseImage.alpha_composite(image, (0,0))
        baseImage = baseImage.convert('RGB')
        doubleBuffer.SetImage(baseImage, self.entries[self.level][0][icon][0], self.entries[self.level][0][icon][1])
        for i in range(1, len(self.entries[self.level])):
            entry = self.entries[self.level][i]
            print(entry[3])
            print(self.fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(doubleBuffer, self.fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        return
        
    def run(self, double_buffer):
        return False
