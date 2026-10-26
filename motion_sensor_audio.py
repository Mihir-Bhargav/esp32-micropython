from machine import Pin, PWM
import time

# Initialize Speaker on GPIO 18
speaker = PWM(Pin(18))

# Initialize Obstacle Avoidance Sensor on GPIO 4
sensor = Pin(4, Pin.IN)

# "Deck the Halls" melody array (frequency in Hz, duration in ms)
melody = [
    (587, 250), (494, 250), (440, 250), (392, 250), 
    (440, 250), (494, 250), (523, 250), (494, 250)
]

def play_note(freq, duration_ms):
    if freq > 0:
        speaker.freq(freq)
        speaker.duty(512)
    else:
        speaker.duty(0)
    time.sleep_ms(duration_ms)
    speaker.duty(0)
    time.sleep_ms(15)

print("Music box armed! Wave your hand in front of the obstacle sensor.")

try:
    while True:
        # The sensor output goes LOW (0) when your hand blocks the IR beam
        if sensor.value() == 0:
            print("Obstacle detected! Playing melody...")
            for note, duration in melody:
                play_note(note, duration)
            time.sleep(1) # Cooldown to avoid continuous re-triggering
        time.sleep(0.05)
except KeyboardInterrupt:
    speaker.deinit()
    print("Stopped.")