from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime
import time
import random

RED = (255, 0, 0)
'''
Format for sprite sheets
String - Name/location of Sprite Sheet
A tuple of width, height of each icon
A tuple with row elements, each element is the number of icons in that row.
('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7))

'''
class MatrixSpriteViewer(MatrixBase):
    def __init__(self, level):
        self.level = level

    def setBackground(file, size, x, y, doubleBuffer):
        backgroundImage = Image.open(file).convert('RGBA')
        bkCroppedImage = backgroundImage.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                        (self.index + 1) * self.spriteSheets[self.level][1][0],
                        (self.set+1) * self.spriteSheets[self.level][1][1]))
    
    def loadImages(self):
        self.grassLevel = 3
        self.grassIndex = 1    # This is basically the X index of the image set
        self.grassSet = 1      # This is basically the Y index of the image set
        backgroundImage = Image.open(self.spriteSheets[self.grassLevel][0]).convert('RGBA')
        self.grassImage = backgroundImage.crop((self.grassIndex * self.spriteSheets[self.grassLevel][1][0], self.grassSet * self.spriteSheets[self.grassLevel][1][1],
                        (self.grassIndex + 1) * self.spriteSheets[self.grassLevel][1][0],
                        (self.grassSet+1) * self.spriteSheets[self.grassLevel][1][1]))
        stumpLevel = 3
        stumpIndex = 2
        stumpSet = 1
        self.stumpImage = backgroundImage.crop((stumpIndex * self.spriteSheets[stumpLevel][1][0], stumpSet * self.spriteSheets[stumpLevel][1][1],
                        (stumpIndex + 1) * self.spriteSheets[stumpLevel][1][0],
                        (stumpSet+1) * self.spriteSheets[stumpLevel][1][1]))
        treeLevel = 3
        treeIndex = 1
        treeSet = 5
        self.treeImage = backgroundImage.crop((treeIndex * self.spriteSheets[treeLevel][1][0], treeSet * self.spriteSheets[treeLevel][1][1],
                        (treeIndex + 2) * self.spriteSheets[treeLevel][1][0],
                        (treeSet+2) * self.spriteSheets[treeLevel][1][1]))
        
        bushLevel = 6
        bushIndex = 2
        bushSet = 3
        bushImage = Image.open(self.spriteSheets[bushLevel][0]).convert('RGBA')
        self.bushImage = bushImage.crop((bushIndex * self.spriteSheets[bushLevel][1][0], bushSet * self.spriteSheets[bushLevel][1][1],
                        (bushIndex + 1) * self.spriteSheets[bushLevel][1][0],
                        (bushSet+1) * self.spriteSheets[bushLevel][1][1]))
        stoneLevel = 6
        stoneIndex = 3
        stoneSet = 3
        stoneImage = Image.open(self.spriteSheets[stoneLevel][0]).convert('RGBA')
        self.stoneImage = stoneImage.crop((stoneIndex * self.spriteSheets[stoneLevel][1][0], stoneSet * self.spriteSheets[stoneLevel][1][1],
                        (stoneIndex + 1) * self.spriteSheets[stoneLevel][1][0],
                        (stoneSet+1) * self.spriteSheets[stoneLevel][1][1]))
        bigtreeLevel = 6
        bigtreeIndex = 0
        bigtreeSet = 2
        bigtreeImage = Image.open(self.spriteSheets[bigtreeLevel][0]).convert('RGBA')
        self.bigtreeImage = bigtreeImage.crop((bigtreeIndex * self.spriteSheets[bigtreeLevel][1][0], bigtreeSet * self.spriteSheets[bigtreeLevel][1][1],
                        (bigtreeIndex + 2) * self.spriteSheets[bigtreeLevel][1][0],
                        (bigtreeSet+2) * self.spriteSheets[bigtreeLevel][1][1]))
        mushroomLevel = 3
        mushroomIndex = 2
        mushroomSet = 2
        mushroomImage = Image.open(self.spriteSheets[mushroomLevel][0]).convert('RGBA')
        self.mushroomImage = mushroomImage.crop((mushroomIndex * self.spriteSheets[mushroomLevel][1][0], mushroomSet * self.spriteSheets[mushroomLevel][1][1],
                        (mushroomIndex + 1) * self.spriteSheets[mushroomLevel][1][0],
                        (mushroomSet+1) * self.spriteSheets[mushroomLevel][1][1]))
        altgrassLevel = 3
        altgrassIndex = 0
        altgrassSet = 1
        altgrassImage = Image.open(self.spriteSheets[altgrassLevel][0]).convert('RGBA')
        self.altgrassImage = altgrassImage.crop((altgrassIndex * self.spriteSheets[altgrassLevel][1][0], altgrassSet * self.spriteSheets[altgrassLevel][1][1],
                        (altgrassIndex + 1) * self.spriteSheets[altgrassLevel][1][0],
                        (altgrassSet+1) * self.spriteSheets[altgrassLevel][1][1]))
        barrelLevel = 3
        barrelIndex = 0
        barrelSet = 0
        barrelImage = Image.open(self.spriteSheets[barrelLevel][0]).convert('RGBA')
        self.barrelImage = barrelImage.crop((barrelIndex * self.spriteSheets[barrelLevel][1][0], barrelSet * self.spriteSheets[barrelLevel][1][1],
                        (barrelIndex + 1) * self.spriteSheets[barrelLevel][1][0],
                        (barrelSet+1) * self.spriteSheets[barrelLevel][1][1]))
        flowerLevel = 3
        flowerIndex = 1
        flowerSet = 2
        flowerImage = Image.open(self.spriteSheets[flowerLevel][0]).convert('RGBA')
        self.flowerImage = flowerImage.crop((flowerIndex * self.spriteSheets[flowerLevel][1][0], flowerSet * self.spriteSheets[flowerLevel][1][1],
                        (flowerIndex + 1) * self.spriteSheets[flowerLevel][1][0],
                        (flowerSet+1) * self.spriteSheets[flowerLevel][1][1]))
        bigmushroomLevel = 3
        bigmushroomIndex = 0
        bigmushroomSet = 7
        self.bigmushroomImage = backgroundImage.crop((bigmushroomIndex * self.spriteSheets[bigmushroomLevel][1][0], bigmushroomSet * self.spriteSheets[bigmushroomLevel][1][1],
                        (bigmushroomIndex + 2) * self.spriteSheets[bigmushroomLevel][1][0],
                        (bigmushroomSet+2) * self.spriteSheets[bigmushroomLevel][1][1]))
        emptyLevel = 3
        emptyIndex = 3
        emptySet = 5
        self.emptyImage = backgroundImage.crop((emptyIndex * self.spriteSheets[emptyLevel][1][0], emptySet * self.spriteSheets[emptyLevel][1][1],
                        (emptyIndex + 1) * self.spriteSheets[emptyLevel][1][0],
                        (emptySet+1) * self.spriteSheets[emptyLevel][1][1]))
        # Each asset group should have the same size asset
        self.layer0Assets = [
            self.grassImage,
            self.altgrassImage
        ]
        self.layer1Assets = [
            self.bushImage,
            self.stoneImage,
        ]
        self.layer2Assets = [
            self.stumpImage,
            self.barrelImage,
            self.emptyImage,
            self.mushroomImage,
            self.emptyImage,
            self.emptyImage,
        ]
        self.layer3Assets = [
            self.bigtreeImage,
            #self.bigmushroomImage
        ]

    def initialize(self, width, height, doubleBuffer):
        self.error = False
        self.spriteSheets = [
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Archaeologist_Sprite_Sheet.png', (64,32), (8, 8, 7, 6, 8, 4, 5)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Torch.png', (8, 16), (10,)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Decorations.png', (16, 16), (4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Banner.png', (32,32), (4, 4)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Destructible_Objects_Sprite_Sheet.png', (64, 64), (3, 7, 3, 7, 3 ,7, 3, 6, 3, 6, 3, 5)),
            ('/home/pi/ccs-rgb-matrix/icons/spriteSheets/FreeCuteTileset/Decors.png', (56,28), (2, 2, 2, 4))
        ]
        numberOfSpriteSheets = len(self.spriteSheets)
        self.loadImages()
        self.layer0 = [
                        self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 
                        self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)],
                        self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)],
                        self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)],
                        self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)]
                      ]
        self.layer1 = [
                        self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 
                        self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 
                        self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 
                        self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 
                        self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)]
                      ]
        self.layer2 = [
                       self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)],
                       self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)],
                       self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)],
                       self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)],
                       self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)],
                      ]
        self.layer3 = [
                       self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)],
                       self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)],
                       #self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)],
                      ]
        self.level = self.level % numberOfSpriteSheets
        self.layer0X = 0
        self.layer1X = 0
        self.layer2X = 0
        self.layer3X = 0
        self.image = Image.open(self.spriteSheets[self.level][0]).convert('RGBA')
        self.set = 1
        self.index = 0
        self.width = width
        self.height = height
        self.stop = False
        self.x = -self.spriteSheets[self.level][1][0]   # This puts the character off the screen at the beginning.
        self.y = 0
        self.loadImages()
        baseImage = Image.new('RGBA', (width, height), (0,0,0,0))
        croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                              (self.index + 1) * self.spriteSheets[self.level][1][0],
                              (self.set+1) * self.spriteSheets[self.level][1][1]))
        background = Image.open('/home/pi/ccs-rgb-matrix/icons/spriteSheets/FreeCuteTileset/BG1.png')
        baseImage.alpha_composite(background, (0,0))
        #background = Image.new('RGBA', (width,height), (0, 255, 255, 255))
        #baseImage.alpha_composite(background, (0,0))
        # Layer 3, Far background objects
        baseImage.alpha_composite(self.layer3[0], (0,0), (abs(self.layer3X), 22))
        baseImage.alpha_composite(self.layer3[1], (112,0), (abs(self.layer3X), 22))
        #baseImage.alpha_composite(self.layer3[2], (112,0), (abs(self.layer3X), 24))
        # Layer 2, mid-background objects
        baseImage.alpha_composite(self.layer2[0], (0,16), (abs(self.layer2X), 0))
        baseImage.alpha_composite(self.layer2[1], (16,16), (abs(self.layer2X), 0))
        baseImage.alpha_composite(self.layer2[2], (32,16), (abs(self.layer2X), 0))
        baseImage.alpha_composite(self.layer2[3], (48,16), (abs(self.layer2X), 0))
        baseImage.alpha_composite(self.layer2[4], (64,16), (abs(self.layer2X), 0))
        # Layer 1, background objects
        baseImage.alpha_composite(self.layer1[0], (0,16), (abs(self.layer1X), 0))
        baseImage.alpha_composite(self.layer1[1], (28,16), (abs(self.layer1X), 0))
        baseImage.alpha_composite(self.layer1[2], (56,16), (abs(self.layer1X), 0))
        # Layer 0, Background objects
        baseImage.alpha_composite(self.layer0[0], (0,16), (abs(self.layer0X), 0))
        baseImage.alpha_composite(self.layer0[1], (16,16), (abs(self.layer0X), 0))
        baseImage.alpha_composite(self.layer0[2], (32,16), (abs(self.layer0X), 0))
        baseImage.alpha_composite(self.layer0[3], (48,16), (abs(self.layer0X), 0))
        baseImage.alpha_composite(self.layer0[3], (64,16), (abs(self.layer0X), 0))
        if self.x < 0:
            baseImage.alpha_composite(croppedImage, (0,self.y),(abs(self.x), 0))
        else:
            baseImage.alpha_composite(croppedImage,(self.x,self.y))
        baseImage = baseImage.convert('RGB')
        self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
        print("Width in number of sprites", self.widthInNumberSprites)
        self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
        print("Height in number of sprites", self.heightInNumberSprites)
        print("Image Height", self.image.height)
        print("Image width", self.image.width)
        if self.image.height != self.heightInNumberSprites * self.spriteSheets[self.level][1][1]:
            self.error = True
        if self.image.width != self.widthInNumberSprites * self.spriteSheets[self.level][1][0]:
            self.error = True
        if self.error:
            f = graphics.Font()
            f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
            red = graphics.Color(*RED)
            graphics.DrawText(doubleBuffer, f, 8,22, red, "Error")
            graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, red)
            graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, red)
            graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, red)
            graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, red)
            graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, red)
            graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, red)
            graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, red)
            graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, red)
            return

        doubleBuffer.SetImage(baseImage)
        self.now = time.monotonic()
        
    def run(self, doubleBuffer):
        if self.error:
            return False
        if (time.monotonic() - self.now) > 0.1:
            self.now = time.monotonic()
            self.index = (self.index + 1) % self.spriteSheets[self.level][2][self.set]
            #if self.index == 0:
            #    self.set = (self.set + 1) % self.heightInNumberSprites
            baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                                  (self.index + 1) * self.spriteSheets[self.level][1][0],
                                  (self.set+1) * self.spriteSheets[self.level][1][1]))
            #background = Image.open('/home/pi/icons/Backgrounds/Clouds_100x59.png')
            background = Image.open('/home/pi/ccs-rgb-matrix/icons/spriteSheets/FreeCuteTileset/BG1.png')
            #baseImage.alpha_composite(background, (0,0), (20,20))
            #background = Image.open('/home/pi/icons/Backgrounds/Mountains_Loopable_56x31.png')
            #background = Image.new('RGBA', (self.width,self.height), (0, 255, 255, 255))
            baseImage.alpha_composite(background, (0,0))
            # Layer 3, Far background objects
            baseImage.alpha_composite(self.layer3[0], (0,0), (abs(self.layer3X), 22))
            baseImage.alpha_composite(self.layer3[1], (112-abs(self.layer3X),0), (0, 22))
            # Layer 2, mid-background objects
            baseImage.alpha_composite(self.layer2[0], (0,16), (abs(self.layer2X), 0))
            baseImage.alpha_composite(self.layer2[1], (16-abs(self.layer2X),16), (0, 0))
            baseImage.alpha_composite(self.layer2[2], (32-abs(self.layer2X),16), (0, 0))
            baseImage.alpha_composite(self.layer2[3], (48-abs(self.layer2X),16), (0, 0))
            baseImage.alpha_composite(self.layer2[4], (64-abs(self.layer2X),16), (0, 0))
            # Layer 1, background objects
            baseImage.alpha_composite(self.layer1[0], (0,16), (abs(self.layer1X), 0))
            baseImage.alpha_composite(self.layer1[1], (28-abs(self.layer1X),16), (0, 0))
            baseImage.alpha_composite(self.layer1[2], (56-abs(self.layer1X),16), (0, 0))
            # Layer 0, Background objects
            baseImage.alpha_composite(self.layer0[0], (0,16), (abs(self.layer0X), 0))
            baseImage.alpha_composite(self.layer0[1], (16-abs(self.layer0X),16), (0, 0))
            baseImage.alpha_composite(self.layer0[2], (32-abs(self.layer0X),16), (0, 0))
            baseImage.alpha_composite(self.layer0[3], (48-abs(self.layer0X),16), (0, 0))
            baseImage.alpha_composite(self.layer0[4], (64-abs(self.layer0X),16), (0, 0))
            if self.x < 0:
                baseImage.alpha_composite(croppedImage, (0,self.y),(abs(self.x), 0))
            else:
                baseImage.alpha_composite(croppedImage,(self.x,self.y))
            if (self.spriteSheets[self.level][1][0] / 2 + self.x) < 32:
                self.x = self.x + 4
            else:
                if not self.stop:
                    self.layer0X += 4
                    if self.layer0X >= 16:
                        #self.stop = True
                        self.layer0X = 0
                        self.layer0.pop(0)
                        self.layer0.append(self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)])
                    self.layer1X += 2
                    if self.layer1X >= 28:
                        self.layer1X = 0
                        self.layer1.pop(0)
                        self.layer1.append(self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)])
                    self.layer2X += 1
                    if self.layer2X >= 16:
                        self.layer2X = 0
                        self.layer2.pop(0)
                        self.layer2.append(self.layer2Assets[random.randint(0, len(self.layer2Assets)-1)])
                    self.layer3X += 1
                    if self.layer3X >= 112:
                        self.layer3X = 0
                        self.layer3.pop(0)
                        self.layer3.append(self.layer3Assets[random.randint(0, len(self.layer3Assets)-1)])
            if self.x >= 64:
                self.x = -self.spriteSheets[self.level][1][0]
            baseImage = baseImage.convert('RGB')
            self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
            #print("Width in number of sprites", self.widthInNumberSprites)
            self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
            #print("Height in number of sprites", self.heightInNumberSprites)
            #print("Image Height", self.image.height)
            #print("Image width", self.image.width)
            doubleBuffer.SetImage(baseImage)
            return True
        return False
