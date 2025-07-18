import RPi.GPIO as GPIO
import time
import random

# === CONFIG ===
LED_PINS = [3, 5, 7, 11, 13, 15, 19]     # BOARD mode pins
SWITCH_PINS = [21, 23, 29, 31, 33, 35, 37]
BOUNCE_TIME = 200  # in ms

# === INIT ===
GPIO.setmode(GPIO.BOARD)

for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # LEDs off by default (sinking setup)

for pin in SWITCH_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# === ACTIVE GAME STATE ===
active_index = None  # Which LED/Switch is currently active


def turn_off_all_leds():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.HIGH)


def set_active_target(index):
    global active_index
    turn_off_all_leds()
    if 0 <= index < len(LED_PINS):
        GPIO.output(LED_PINS[index], GPIO.LOW)  # Turn ON selected LED
        active_index = index


def wait_for_correct_press(timeout=5):
    """
    Waits for the player to press the correct switch.
    Returns True if correct switch was pressed within timeout.
    """
    global active_index
    if active_index is None:
        return False

    target_pin = SWITCH_PINS[active_index]
    start_time = time.time()
    while time.time() - start_time < timeout:
        if GPIO.input(target_pin) == GPIO.HIGH:
            print(f"✅ Button {active_index+1} pressed.")
            return True
        time.sleep(0.01)
    print("⏱️ Timeout! Button not pressed in time.")
    return False


def cleanup():
    turn_off_all_leds()
    GPIO.cleanup()
