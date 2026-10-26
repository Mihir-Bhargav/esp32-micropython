import time
from machine import Pin, PWM

user_input = input("Do you want the light on, off, blink or dynamic?\n")
led = Pin(4, Pin.OUT)

if user_input == "ON":
    led.value(1)

elif user_input == "OFF":
    led.value(0)

elif user_input == "blink":
    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)

elif user_input == "dynamic":
    led_pwm = PWM(Pin(4), freq=1000)
    
    # Turn fully on first
    led_pwm.duty(1023)
    time.sleep(1)

    # Fade down loop
    for duty in range(1023, -1, -1):
        led_pwm.duty(duty)
        time.sleep(3 / 1023)

    time.sleep(1)

else:
    print("please answer correctly; ON, OFF, blink, or dynamic?")

