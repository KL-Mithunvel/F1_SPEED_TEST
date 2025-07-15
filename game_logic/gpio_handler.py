import RPi.GPIO as GPIO
import random
import time
from config import LED, SWITCH

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    for pin in LED:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    for pin in SWITCH:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def cleanup_gpio():
    GPIO.cleanup()

def turn_on_led(index):
    GPIO.output(LED[index], GPIO.HIGH)

def turn_off_led(index):
    GPIO.output(LED[index], GPIO.LOW)

def turn_off_all_leds():
    for pin in LED:
        GPIO.output(pin, GPIO.LOW)

def get_random_index():
    return random.randint(0, len(LED) - 1)

def wait_for_button(index, timeout=2.0):
    """
    Waits up to 'timeout' seconds for the correct button to be pressed.
    Returns True if pressed in time, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if GPIO.input(SWITCH[index]) == GPIO.HIGH:
            return True
    return False
