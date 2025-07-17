import RPi.GPIO as GPIO
import time
from config import LED, SWITCH

def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in LED:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    for pin in SWITCH:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def cleanup():
    GPIO.cleanup()

def test_gpio():
    print("Starting GPIO test... (Press the correct button to continue each step)\n")

    for i in range(len(LED)):
        led_pin = LED[i]
        switch_pin = SWITCH[i]

        print(f"Testing LED {i + 1} (Pin {led_pin}) with Button (Pin {switch_pin})")
        GPIO.output(led_pin, GPIO.HIGH)
        print("➡️  LED ON. Waiting for button press...")

        # Wait until the correct button is pressed
        while GPIO.input(switch_pin) == GPIO.LOW:
            time.sleep(0.05)

        GPIO.output(led_pin, GPIO.LOW)
        print("✅ Button press detected.\n")
        time.sleep(0.3)  # short debounce delay

    print("🎉 All GPIOs tested successfully!")
    cleanup()

if __name__ == "__main__":
    try:
        setup()
        test_gpio()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
        cleanup()
