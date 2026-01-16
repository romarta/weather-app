from config import Config
from services.openweather_api import fetch_weather
import time

# zapis do excel
# zapis do db
# zapis wykresy i interfejs


while True:
    weather = fetch_weather()
    print(weather)
    time.sleep(5)
