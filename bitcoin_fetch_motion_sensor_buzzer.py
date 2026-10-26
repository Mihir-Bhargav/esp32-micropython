# Wi-Fi credentials live in secrets.py (gitignored). Copy secrets.py.example
# to secrets.py on the board and fill in your own values.
from secrets import WIFI_SSID, WIFI_PASS
import network
import time
from machine import Pin, PWM
import urequests


# Hardware Setup
speaker = PWM(Pin(18))
sensor = Pin(4, Pin.IN)
red_led = Pin(17, Pin.OUT)   # Updated to GPIO 17
green_led = Pin(21, Pin.OUT)

last_price = None

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected successfully! IP:", wlan.ifconfig()[0])

def play_tone(freq, duration_ms, duty=512):
    if freq > 0:
        speaker.freq(freq)
        speaker.duty(duty)
    else:
        speaker.duty(0)
    time.sleep_ms(duration_ms)
    speaker.duty(0)
    time.sleep_ms(15)

def say_bullish():
    print("Synthesizing: BULLISH 📈")
    green_led.value(1)
    red_led.value(0)
    play_tone(220, 120)
    play_tone(294, 120)
    play_tone(587, 180)
    play_tone(784, 200)

def say_bearish():
    print("Synthesizing: BEARISH 📉")
    green_led.value(0)
    red_led.value(1)
    play_tone(440, 150)
    play_tone(330, 150)
    play_tone(220, 250)

connect_wifi()
print("Market System with LED Feedback Active. Wave hand to test.")

try:
    while True:
        if sensor.value() == 0:
            print("Fetching live Bitcoin price...")
            try:
                response = urequests.get("http://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
                data = response.json()
                current_price = float(data['price'])
                print(f"Live BTC Price: ${current_price}")
                
                if last_price is not None:
                    if current_price >= last_price:
                        say_bullish()
                    else:
                        say_bearish()
                else:
                    print("First reading captured. Wave again to compare delta.")
                    say_bullish()
                
                last_price = current_price
                response.close()
            except Exception as e:
                print("API Error:", e)
                say_bearish()
                
            time.sleep(2)
        time.sleep(0.05)
except KeyboardInterrupt:
    speaker.deinit()
    red_led.value(0)
    green_led.value(0)
    print("System halted.")