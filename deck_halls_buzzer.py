from machine import Pin, PWM
import time

# Initialize speaker on GPIO 18
speaker = PWM(Pin(18))

# "Deck the Halls" melody array: (frequency in Hz, duration in ms)
melody = [
    # Deck the halls with boughs of holly
    (587, 300), (494, 300), (440, 300), (392, 300), 
    (440, 300), (494, 300), (523, 300), (494, 300),
    (440, 300), (392, 300), (370, 300), (392, 300), 
    (440, 600), (370, 300), (329, 300), (294, 600),
    # Pause between loops
    (0, 1000)
]

def play_note(freq, duration_ms):
    if freq > 0:
        speaker.freq(freq)
        speaker.duty(512) # 50% duty cycle
    else:
        speaker.duty(0)
    time.sleep_ms(duration_ms)
    speaker.duty(0)
    time.sleep_ms(20) # Brief gap between notes

print("Playing 'Deck the Halls' in a loop... Press Stop in Thonny to exit.")

try:
    while True:
        for note, duration in melody:
            play_note(note, duration)
        time.sleep_ms(1500) # Pause before repeating
except KeyboardInterrupt:
    speaker.deinit()
    print("Playback stopped.")
