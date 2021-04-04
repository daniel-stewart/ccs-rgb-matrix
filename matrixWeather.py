from matrixBase import MatrixBase
from rgbmatrix import graphics
from PIL import Image
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime
from datetime import timedelta

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'owmid' equal to your OpenWeatherMap ID.
try:
    from secrets import secrets
except ImportError:
    print("OWM Id is kept in secrets.py, please add them.")
    bSecretFileExists = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE_WHITE = (128, 128, 255)
DARK_BLUE = (0, 0, 128)

class MatrixWeather(MatrixBase):
    def __init__(self, number):
        self.number = number
        self.bSecretFileExists = True
        self.OWMError = False
    
    def colorRamp(self, temp):
        if temp < 45:
            return BLUE_WHITE
        elif temp > 80:
            return ORANGE
        else:
            if temp >= 65:
                green = int(((temp - 65.0) / 15.0) * 128.0)
                return tuple((255, 255 - green, 0))
            else:
                red = green = int(((temp - 45.0) / 20.0) * 128.0)
                blue = int(((temp - 45.0) / 20.0) * 255.0)
                return tuple((128 + red, 128 + green, 255 - blue))

    def createDay(self, day, doubleBuffer, color):
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
        graphics.DrawText(doubleBuffer, font, 10, 20, color, day)
        return

    def initialize(self, width, height, doubleBuffer):
        self.iconPathPrefix = '/home/pi/icons/weatherIcons/png/24x24/'
        self.weatherTable = {
            200:['012-rain-2.png','Thndr storm','Thunderstorm with light rain'],
            201:['012-rain-2.png','Thndr storm','Thunderstorm with rain'],
            202:['012-rain-2.png','Thndr storm','Thunderstorm with heavy rain'],
            210:['021-storm-1.png','Thndr storm','Light thunderstorm'],
            211:['021-storm-1.png','Thndr storm','Thunderstorm'],
            212:['041-storm.png','Thndr storm','Heavy thunderstorm'],
            221:['041-storm.png','Thndr storm','Ragged thunderstorm'],
            230:['012-rain-2.png','Thndr storm','Thunderstorm with light drizzle'],
            231:['012-rain-2.png','Thndr storm','Thunderstorm with drizzle'],
            232:['012-rain-2.png','Thndr storm','Thunderstorm with heavy drizzle'],
            300:['037-umbrella.png','Lt Drizzle','Light intensity drizzle'],
            301:['038-rain-1.png',  '   Drizzle','Drizzle'],
            302:['036-umbrella-1.png','   Drizzle','Heavy intensity drizzle'],
            310:['036-umbrella-1.png','   Drizzle','Light intensity drizzle rain'],
            311:['036-umbrella-1.png','   Drizzle','Drizzle rain'],
            312:['036-umbrella-1.png','   Drizzle','Heavy intensity drizzle rain'],
            313:['040-rain.png',   '    Drizzle','Shower rain and drizzle'],
            314:['036-umbrella-1.png','   Drizzle','Heavy shower rain and drizzle'],
            321:['036-umbrella-1.png','   Drizzle','Shower drizzle'],
            500:['002-drop.png',    'Light Rain','Light rain'],
            501:['010-rain-3.png',  '      Rain','Moderate rain'],
            502:['040-rain.png',    'Heavy Rain','Heavy intensity rain'],
            503:['040-rain.png',    'Heavy Rain','Very heavy rain'],
            504:['040-rain.png',    'Extrm. Rain','Extreme rain'],
            511:['010-rain-3.png',  '      Rain','Freezing rain'],
            520:['010-rain-3.png',  '      Rain','Light intensity shower rain'],
            521:['010-rain-3.png',  '      Rain','Shower rain'],
            522:['040-rain.png',    'Heavy Rain','Heavy intensity shower rain'],
            531:['010-rain-3.png',  '      Rain','Ragged shower rain'],
            600:['snowflake.png',   'Light Snow','Light snow'],
            601:['008-snow-1.png',  '      Snow','Snow'],
            602:['042-snow.png',    'Heavy Snow','Heavy snow'],
            611:['008-snow-1.png',  '     Sleet','Sleet'],
            612:['008-snow-1.png',  'Light Sleet','Light shower sleet'],
            613:['008-snow-1.png',  '      Snow','Shower sleet'],
            615:['snowflake.png',   '      Snow','Light rain and snow'],
            616:['042-snow.png',    'Rain & Snow','Rain and snow'],
            620:['snowflake.png',   'Light Snow','Light shower snow'],
            621:['008-snow-1.png',  'Shower Snow','Shower snow'],
            622:['042-snow.png',    'Heavy Snow','Heavy shower snow'],
            701:['015-clouds-3.png','      Mist','Mist'],
            711:['023-clouds-2.png','     Smoke','Smoke'],
            721:['015-clouds-3.png','      Haze','Haze'],
            731:['015-clouds-3.png','      Dust','Sand/dust whirls'],
            741:['023-clouds-2.png','      Fog','Fog'],
            751:['023-clouds-2.png','      Sand','Sand'],
            761:['023-clouds-2.png','      Dust','Dust'],
            762:['023-clouds-2.png','      Ash','Volcanic ash'],
            771:['022-wind.png',    '   Squalls','Squalls'],
            781:['013-tornado.png', '   Tornado','Tornado'],
            800:['050-sun.png',     ' Clear Sky','Clear sky'],
            801:['027-cloudy-1.png','Few Clouds','Few clouds: 11-25%'],
            802:['003-cloudy-4.png','    Cloudy','Scattered clouds: 25-50%'],
            803:['005-cloudy-3.png','    Cloudy','Broken clouds: 51-84%'],
            804:['049-clouds.png',  '  Overcast','Overcast clouds: 85-100%'],
        }
        if self.bSecretFileExists:
            try:
                self.owm = OWM(secrets['owmid'])
                self.mgr = self.owm.weather_manager()
                observation = self.mgr.weather_at_place(secrets['owm_place'])
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.OWMError = True
            if self.OWMError:
                f = graphics.Font()
                f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
                white = graphics.Color(*WHITE)
                graphics.DrawText(doubleBuffer, f, 8,22, white, "Hello")
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
                graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
                graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
                graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
                graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
                graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
                graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
                graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
                return
            w = observation.weather
            self.wid = w.weather_code
            status = w.detailed_status
            temp = w.temperature('fahrenheit') # {'temp_max':10.5, 'temp':9.7, 'temp_min':4.5}
            self.currentTemp = round(temp['temp'])
        else:
            f = graphics.Font()
            f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
            white = graphics.Color(*WHITE)
            graphics.DrawText(doubleBuffer, f, 8,22, white, "Hello")
            graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
            graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
            graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
            graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
            graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
            graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
            graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
            graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
            return

        self.now = datetime.now() + timedelta(minutes=10)
        print(self.wid)
        print(status)
        print(self.currentTemp)
        print(self.weatherTable[self.wid][2])
        icon = self.iconPathPrefix + self.weatherTable[self.wid][0]
        image = Image.open(icon).convert('RGB')
        doubleBuffer.Clear()
        doubleBuffer.SetImage(image,0)
        self.font = graphics.Font()
        self.font.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
        self.font2 = graphics.Font()
        self.font2.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf')
        graphics.DrawText(doubleBuffer, self.font, 35, 18, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
        graphics.DrawText(doubleBuffer, self.font2, 0, 30, graphics.Color(*WHITE), self.weatherTable[self.wid][1])
        return
    
    def restart(self, doubleBuffer):
        if not self.bSecretFileExists:
            f = graphics.Font()
            f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
            white = graphics.Color(*WHITE)
            graphics.DrawText(doubleBuffer, f, 8,22, white, "Hello")
            graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
            graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
            graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
            graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
            graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
            graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
            graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
            graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
            return
        if self.OWMError:
            self.OWMError = False
            try:
                self.owm = OWM(secrets['owmid'])
                self.mgr = self.owm.weather_manager()
                observation = self.mgr.weather_at_place(secrets['owm_place'])
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.OWMError = True
            if self.OWMError:
                f = graphics.Font()
                f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
                white = graphics.Color(*WHITE)
                graphics.DrawText(doubleBuffer, f, 8,22, white, "Hello")
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
                graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
                graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
                graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
                graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
                graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
                graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
                graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
                return
            w = observation.weather
            self.wid = w.weather_code
            status = w.detailed_status
            temp = w.temperature('fahrenheit') # {'temp_max':10.5, 'temp':9.7, 'temp_min':4.5}
            self.currentTemp = round(temp['temp'])
        if self.now < datetime.now():
            try:
                observation = self.mgr.weather_at_place(secrets['owm_place'])
                print("Jsut got the weather again.")
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.OWMError = True
                f = graphics.Font()
                f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
                white = graphics.Color(*WHITE)
                green = graphics.Color(*GREEN)
                graphics.DrawText(doubleBuffer, f, 8,22, green, "Hello")
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
                graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
                graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
                graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
                graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
                graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
                graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
                graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
                return
            w = observation.weather
            status = w.detailed_status
            self.wid = w.weather_code
            temp = w.temperature('fahrenheit')
            self.currentTemp = round(temp['temp'])
            self.now = datetime.now() + timedelta(minutes=10)
        print(self.wid)
        print(self.currentTemp)
        print(self.weatherTable[self.wid][2])
        icon = self.iconPathPrefix + self.weatherTable[self.wid][0]
        image = Image.open(icon).convert('RGB')
        doubleBuffer.Clear()
        doubleBuffer.SetImage(image,0)
        graphics.DrawText(doubleBuffer, self.font, 35, 18, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
        graphics.DrawText(doubleBuffer, self.font2, 0, 30, graphics.Color(*WHITE), self.weatherTable[self.wid][1])
        return

    def run(self, doubleBuffer):
        if not self.bSecretFileExists:
            return False
        if self.OWMError:
            return False
        if self.now < datetime.now():
            try:
                observation = self.mgr.weather_at_place(secrets['owm_place'])
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.OWMError = True
                f = graphics.Font()
                f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
                white = graphics.Color(*WHITE)
                green = graphics.Color(*GREEN)
                graphics.DrawText(doubleBuffer, f, 8,22, green, "Hello")
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
                graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
                graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
                graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
                graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
                graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
                graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
                graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
                return
            w = observation.weather
            status = w.detailed_status
            wid = w.weather_code
            temp = w.temperature('fahrenheit')
            currentTemp = round(temp['temp'])
            self.now = datetime.now() + timedelta(minutes=10)
            print(wid)
            print(status)
            print(currentTemp)
            print(self.weatherTable[wid][2])
            icon = self.iconPathPrefix + self.weatherTable[wid][0]
            image = Image.open(icon).convert('RGB')
            doubleBuffer.Clear()
            doubleBuffer.SetImage(image,0)
            graphics.DrawText(doubleBuffer, self.font, 35, 18, graphics.Color(*self.colorRamp(currentTemp)), str(currentTemp)+"\u00B0")
            graphics.DrawText(doubleBuffer, self.font2, 0, 30, graphics.Color(*WHITE), self.weatherTable[wid][1])
            return True
        return False
