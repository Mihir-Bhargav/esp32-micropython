from machine import Pin
import time

button = Pin(4, Pin.IN, Pin.PULL_UP)
led = Pin(23, Pin.OUT)

led.value(0)
light_state = False
last_button_state = button.value()
print("System is ready, Toggle for Light!")


while True:
    current_button_state = button.value()    
    
    if last_button_state == 0 and current_button_state == 1:
        light_state = not light_state
        led.value(light_state)
        print(f"Button Pressed! Light is now {'ON' if light_state else 'OFF'}")
        time.sleep(0.2)
        
    last_button_state = current_button_state
    time.sleep(0.01)
    
    

        
        
        
        
        
    
