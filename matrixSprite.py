'''
RASTER EYES for Adafruit Matrix Portal: animated spooky eyes.
Stolen from Adafruit's code for Matrix Portal and ported to RPi.
'''

import math
import random
import time
from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase

# UTILITY FUNCTIONS AND CLASSES --------------------------------------------
class MatrixSprite(MatrixBase):
    def __init__(self, level):
        """Create Sprite object from color-paletted BMP file, optionally
           set one color to transparent (pass as RGB tuple or list to locate
           nearest color, or integer to use a known specific color index).
        """
        print("Initializing")
        self.level = level % 5

    def initialize(self, width, height, double_buffer):
        if self.level == 3:
            from eyes.werewolf.data import EYE_DATA
        elif self.level == 1:
            from eyes.cyclops.data import EYE_DATA
        elif self.level == 2:
            from eyes.kobold.data import EYE_DATA
        elif self.level == 0:
            from eyes.adabot.data import EYE_DATA
        elif self.level == 4:
            from eyes.skull.data import EYE_DATA
        else:
            error("Invalid number")
        
        self.EYE_DATA = EYE_DATA
        self.EYE_CENTER = (int((EYE_DATA['eye_move_min'][0] +           # Pixel coords of eye
                       EYE_DATA['eye_move_max'][0]) / 2),       # image when centered
                      int((EYE_DATA['eye_move_min'][1] +           # ('neutral' position)
                       EYE_DATA['eye_move_max'][1]) / 2))
        self.EYE_RANGE = (abs(EYE_DATA['eye_move_max'][0] -         # Max eye image motion
                         EYE_DATA['eye_move_min'][0]) / 2,     # delta from center
                     abs(EYE_DATA['eye_move_max'][1] -
                         EYE_DATA['eye_move_min'][1]) / 2)
        self.UPPER_LID_MIN = (min(EYE_DATA['upper_lid_open'][0],    # Motion bounds of
                             EYE_DATA['upper_lid_closed'][0]), # upper and lower
                         min(EYE_DATA['upper_lid_open'][1],    # eyelids
                             EYE_DATA['upper_lid_closed'][1]))
        self.UPPER_LID_MAX = (max(EYE_DATA['upper_lid_open'][0],
                             EYE_DATA['upper_lid_closed'][0]),
                         max(EYE_DATA['upper_lid_open'][1],
                             EYE_DATA['upper_lid_closed'][1]))
        self.LOWER_LID_MIN = (min(EYE_DATA['lower_lid_open'][0],
                             EYE_DATA['lower_lid_closed'][0]),
                         min(EYE_DATA['lower_lid_open'][1],
                             EYE_DATA['lower_lid_closed'][1]))
        self.LOWER_LID_MAX = (max(EYE_DATA['lower_lid_open'][0],
                             EYE_DATA['lower_lid_closed'][0]),
                         max(EYE_DATA['lower_lid_open'][1],
                             EYE_DATA['lower_lid_closed'][1]))
        
        self.EYE_POS = (0,0)             
        # Initial estimate of 'tracked' eyelid positions
        self.UPPER_LID_POS = (EYE_DATA['upper_lid_center'][0] + self.EYE_POS[0],
                         EYE_DATA['upper_lid_center'][1] + self.EYE_POS[1])
        self.LOWER_LID_POS = (EYE_DATA['lower_lid_center'][0] + self.EYE_POS[0],
                         EYE_DATA['lower_lid_center'][1] + self.EYE_POS[1])
        # Then constrain these to the upper/lower lid motion bounds
        self.UPPER_LID_POS = (min(max(self.UPPER_LID_POS[0],
                                 self.UPPER_LID_MIN[0]), self.UPPER_LID_MAX[0]),
                         min(max(self.UPPER_LID_POS[1],
                                 self.UPPER_LID_MIN[1]), self.UPPER_LID_MAX[1]))
        self.LOWER_LID_POS = (min(max(self.LOWER_LID_POS[0],
                                 self.LOWER_LID_MIN[0]), self.LOWER_LID_MAX[0]),
                         min(max(self.LOWER_LID_POS[1],
                                 self.LOWER_LID_MIN[1]), self.LOWER_LID_MAX[1]))
        # Then interpolate between bounded tracked position to closed position
        self.UPPER_LID_POS = (self.UPPER_LID_POS[0], self.UPPER_LID_POS[1])
        self.LOWER_LID_POS = (self.LOWER_LID_POS[0], self.LOWER_LID_POS[1])
                     
        
        self.EYE_PREV = (0, 0)
        self.EYE_NEXT = (0, 0)
        self.MOVE_STATE = False                                     # Initially stationary
        self.MOVE_EVENT_DURATION = random.uniform(0.1, 3)           # Time to first move
        self.BLINK_STATE = 2                                        # Start eyes closed
        self.BLINK_EVENT_DURATION = random.uniform(0.25, 0.5)       # Time for eyes to open
        self.TIME_OF_LAST_MOVE_EVENT = self.TIME_OF_LAST_BLINK_EVENT = time.monotonic()
        
        self.stencil = Image.open(EYE_DATA['stencil_image'])
        self.stencil = self.stencil.convert('RGBA')
        stencil_width, stencil_height = self.stencil.size
        self.eyes = Image.open(EYE_DATA['eye_image'])
        self.eyes = self.eyes.convert('RGBA')
        eyes_width, eyes_height = self.eyes.size
        self.lowerLid = Image.open(EYE_DATA['lower_lid_image'])
        self.lowerLid = self.lowerLid.convert('RGBA')
        lowerLid_width, lowerLid_height = self.lowerLid.size
        self.upperLid = Image.open(EYE_DATA['upper_lid_image'])
        self.upperLid = self.upperLid.convert('RGBA')
        upperLid_width, upperLid_height = self.upperLid.size
        self.background = Image.new('RGB', self.stencil.size, (0,0,0))
        self.background.paste(self.eyes, self.EYE_CENTER, self.eyes)
        print(self.EYE_CENTER)
        self.background.paste(self.lowerLid, tuple(int(c) for c in self.LOWER_LID_POS), self.lowerLid)
        self.background.paste(self.upperLid, tuple(int(c) for c in self.UPPER_LID_POS), self.upperLid)
        self.background.paste(self.stencil, (0,0), self.stencil)
        self.background.convert('RGB')
        
        double_buffer.SetImage(self.background, 0)

    def run(self, double_buffer):
        NOW = time.monotonic()

        # Eye movement ---------------------------------------------------------

        if NOW - self.TIME_OF_LAST_MOVE_EVENT > self.MOVE_EVENT_DURATION:
            self.TIME_OF_LAST_MOVE_EVENT = NOW # Start new move or pause
            self.MOVE_STATE = not self.MOVE_STATE   # Toggle between moving & stationary
            if self.MOVE_STATE:                # Starting a new move?
                self.MOVE_EVENT_DURATION = random.uniform(0.08, 0.17) # Move time
                ANGLE = random.uniform(0, math.pi * 2)
                self.EYE_NEXT = (math.cos(ANGLE) * self.EYE_RANGE[0], # (0,0) in center,
                            math.sin(ANGLE) * self.EYE_RANGE[1]) # NOT pixel coords
            else:                         # Starting a new pause
                self.MOVE_EVENT_DURATION = random.uniform(0.04, 3)    # Hold time
                self.EYE_PREV = self.EYE_NEXT

        # Fraction of move elapsed (0.0 to 1.0), then ease in/out 3*e^2-2*e^3
        RATIO = (NOW - self.TIME_OF_LAST_MOVE_EVENT) / self.MOVE_EVENT_DURATION
        RATIO = 3 * RATIO * RATIO - 2 * RATIO * RATIO * RATIO
        self.EYE_POS = (self.EYE_PREV[0] + RATIO * (self.EYE_NEXT[0] - self.EYE_PREV[0]),
                   self.EYE_PREV[1] + RATIO * (self.EYE_NEXT[1] - self.EYE_PREV[1]))

        # Blinking -------------------------------------------------------------

        if NOW - self.TIME_OF_LAST_BLINK_EVENT > self.BLINK_EVENT_DURATION:
            self.TIME_OF_LAST_BLINK_EVENT = NOW # Start change in blink
            self.BLINK_STATE += 1               # Cycle paused/closing/opening
            if self.BLINK_STATE == 1:           # Starting a new blink (closing)
                self.BLINK_EVENT_DURATION = random.uniform(0.03, 0.07)
            elif self.BLINK_STATE == 2:         # Starting de-blink (opening)
                self.BLINK_EVENT_DURATION *= 2
            else:                          # Blink ended,
                self.BLINK_STATE = 0            # paused
                self.BLINK_EVENT_DURATION = random.uniform(self.BLINK_EVENT_DURATION * 3, 4)

        if self.BLINK_STATE: # Currently in a blink?
            # Fraction of closing or opening elapsed (0.0 to 1.0)
            RATIO = (NOW - self.TIME_OF_LAST_BLINK_EVENT) / self.BLINK_EVENT_DURATION
            if self.BLINK_STATE == 2:    # Opening
                RATIO = 1.0 - RATIO # Flip ratio so eye opens instead of closes
        else:           # Not blinking
            RATIO = 0

        # Eyelid tracking ------------------------------------------------------

        # Initial estimate of 'tracked' eyelid positions
        self.UPPER_LID_POS = (self.EYE_DATA['upper_lid_center'][0] + self.EYE_POS[0],
                         self.EYE_DATA['upper_lid_center'][1] + self.EYE_POS[1])
        self.LOWER_LID_POS = (self.EYE_DATA['lower_lid_center'][0] + self.EYE_POS[0],
                         self.EYE_DATA['lower_lid_center'][1] + self.EYE_POS[1])
        # Then constrain these to the upper/lower lid motion bounds
        self.UPPER_LID_POS = (min(max(self.UPPER_LID_POS[0],
                                 self.UPPER_LID_MIN[0]), self.UPPER_LID_MAX[0]),
                         min(max(self.UPPER_LID_POS[1],
                                 self.UPPER_LID_MIN[1]), self.UPPER_LID_MAX[1]))
        self.LOWER_LID_POS = (min(max(self.LOWER_LID_POS[0],
                                 self.LOWER_LID_MIN[0]), self.LOWER_LID_MAX[0]),
                         min(max(self.LOWER_LID_POS[1],
                                 self.LOWER_LID_MIN[1]), self.LOWER_LID_MAX[1]))
        # Then interpolate between bounded tracked position to closed position
        self.UPPER_LID_POS = (self.UPPER_LID_POS[0] + RATIO *
                         (self.EYE_DATA['upper_lid_closed'][0] - self.UPPER_LID_POS[0]),
                         self.UPPER_LID_POS[1] + RATIO *
                         (self.EYE_DATA['upper_lid_closed'][1] - self.UPPER_LID_POS[1]))
        self.LOWER_LID_POS = (self.LOWER_LID_POS[0] + RATIO *
                         (self.EYE_DATA['lower_lid_closed'][0] - self.LOWER_LID_POS[0]),
                         self.LOWER_LID_POS[1] + RATIO *
                         (self.EYE_DATA['lower_lid_closed'][1] - self.LOWER_LID_POS[1]))

        # Move eye sprites -----------------------------------------------------
        
        eyeCenter = (int(self.EYE_CENTER[0] + self.EYE_POS[0] + 0.5), int(self.EYE_CENTER[1] + self.EYE_POS[1] + 0.5))
        upperLidCenter = (int(self.UPPER_LID_POS[0] + 0.5), int(self.UPPER_LID_POS[1] + 0.5))
        lowerLidCenter= (int(self.LOWER_LID_POS[0] + 0.5), int(self.LOWER_LID_POS[1] + 0.5))

        self.background = Image.new('RGB', self.stencil.size, (0,0,0))
        self.background.paste(self.eyes, eyeCenter, self.eyes)
        self.background.paste(self.lowerLid, lowerLidCenter, self.lowerLid)
        self.background.paste(self.upperLid, upperLidCenter, self.upperLid)
        self.background.paste(self.stencil, (0,0), self.stencil)
        self.background.convert('RGB')
        double_buffer.SetImage(self.background, 0)
        return True

