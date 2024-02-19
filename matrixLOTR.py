import time
import base64
from rgbmatrix import graphics
from matrixbase import MatrixBase
from PIL import Image
from PIL import ImageDraw

WHITE = (255, 255, 255)

class MatrixLOTR(MatrixBase):
    ARAGORN_IMG = base64.b64decode("""
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAUGVYSWZNTQAqAAAACAACARIAAwAAAAEAAQAAh2kABAAAAAEAAAAmAAAAAAADoAEAAwAAAAEAAQAAoAIABAAAAAEAAAAQoAMABAAAAAEAAAAQAAAAACaIX+wAAAIwaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA2LjAuMCI+CiAgIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4zMjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4zMjwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOkNvbG9yU3BhY2U+MTwvZXhpZjpDb2xvclNwYWNlPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KuC+kEAAAAUVJREFUOBGFkqFLBEEUxr93QbgogkGwGQQFF/wLTDaTeGBbg8VgNBguiE2sJxduk2GN/gParCt4YDeLSTws43xv9w3jOes+ePvevHnfb2ZnRpA2ly6HqlgWEiv46DYWo1EinX5oUbXzgE6x8QzSs0JbfHkodYrR8rg33sGf1SnY3BmkhdmAHGndga2mcesAoNMs1iO0App5FYgI6DSNEaQbEEjppBvwfAfnnDoRzOFrKeMhqrPPcleVjh6POW9ut+BOzs7xOL7EtJfV8PcK8YOyQ+WtXF+s4P4tx/b6GghQca0C9lYL7A6XA8TqBovFnJNJUfx690d5Diw1u/AN1biP7PjLOFj4fMXNaBTG4pvd5OpUCypm1gAoNjMIAbTv2UyjAjTjx/+3mgfYyvORgH2pxeyVw76eKG6fSkj9PP/dARfxmmA/xvaF5m8/lV0AAAAASUVORK5CYII=
""")

    def __init__(self, level):
        self.level = level % 2

    def breakText(self, text):
        textArray = []
        # Assume the text is a 6x10 based text, so we can break the text up more easily.
        lineCount = 0
        startCount = 0
        for i in range(len(text)):
            if text[i] == ' ':
                breakCount = i
            elif lineCount > 9:
                textArray.append(text[startCount:breakCount])
                lineCount = 0
            lineCount += 1
            startCount = i
        textArray.append(text[startCount:])
        return textArray
    
    def initialize(self, width, height, double_buffer):
        self.font1 = graphics.Font()
        self.font2 = graphics.Font()
        self.font3 = graphics.Font()
        self.font1.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR14.bdf")
        self.font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/RingbearerMedium-12.bdf")
        self.font3.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/6x10.bdf")
        self.pos = double_buffer.height - 11
        self.image = Image.new("RGB", 64, 21)
        self.draw = ImageDraw.Draw(image)

    def run(self, double_buffer):
        # Look into whether a direct use of PIL text functions can be used to write to an image that is smaller than the entire double_buffer.
        double_buffer.Clear()
        text = "All we have to decide is what to do with the time that is given us."
        textArray = breakText(text)
        numberOfLines = len(textArray)
        numberOfPixelRows = numberOfLines * 11
        pos = 0
        for t in textArray:
            if self.pos+pos < 0 or self.pos+pos > 24:
                continue
            len = graphics.DrawText(double_buffer, self.font2, 2, self.pos+pos, graphics.Color(WHITE), t)
            pos += 11
        self.draw.rectangle((0,0,63,20), fill=(0,0,0), outline=(0,0,0))
        double_buffer.SetImage(self.draw, 21, 0)
        self.pos -= 1
        # double_buffer.height is the height of the display
        # The number 11 is the height (including a space line) of a character (for 6x10 characters).
        if self.pos < -(numberOfPixelRows - 11):
            return True
        time.sleep(0.04)
        return True