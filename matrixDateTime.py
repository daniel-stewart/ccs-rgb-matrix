from datetime import datetime
from rgbmatrix import graphics
from matrixBase import MatrixBase

class MatrixDateTime(MatrixBase):
    def __init__(self, number):
        pass

    def initialize(self, width, height, doubleBuffer):
        self.font = graphics.Font()
        self.fontTime = graphics.Font()
        self.fontTime.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x14.bdf")
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
        self.now = datetime.now()
        currentTime = self.now.strftime("%-I:%M")
        currentMonth = self.now.strftime("%b %d")
        offset = 20
        if self.now.hour%12 == 0 or self.now.hour%12 > 9:
            offset = 13
        doubleBuffer.Clear()
        length = graphics.DrawText(doubleBuffer, self.fontTime, offset,12, graphics.Color(225, 255, 0), currentTime)
        length = graphics.DrawText(doubleBuffer, self.font, 2, 28, graphics.Color(0, 255, 0), currentMonth)
    def run(self, doubleBuffer):
        now = datetime.now()
        if self.now.minute != now.minute:
            self.now = now
            doubleBuffer.Clear()
            currentTime = self.now.strftime("%-I:%M")
            currentMonth = self.now.strftime("%b %d")
            offset = 20
            if self.now.hour%12 == 0 or self.now.hour%12 > 9:
                offset = 13
            length = graphics.DrawText(doubleBuffer, self.fontTime, offset, 12, graphics.Color(225, 255, 0), currentTime)
            length = graphics.DrawText(doubleBuffer, self.font, 2, 28, graphics.Color(0, 255, 0), currentMonth)
            return True
        return False
