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
    print("Starting GPIO test...")

    for i in range(len(LED)):
        led_pin = LED[i]
        switch_pin = SWITCH[i]

        print(f"\nTesting LED {i + 1} (Pin {led_pin}) with Switch (Pin {switch_pin})")
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED ON. Waiting for button press (5 seconds)...")

        start_time = time.time()
        pressed = False
        while time.time() - start_time < 5:
            if GPIO.input(switch_pin) == GPIO.HIGH:
                pressed = True
                break
            time.sleep(0.05)

        GPIO.output(led_pin, GPIO.LOW)

        if pressed:
            print("✅ Button press detected.")
        else:
            print("❌ Button not pressed in time.")

    print("\nTest complete.")
    cleanup()

if __name__ == "__main__":
    try:
        setup()
        test_gpio()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        cleanup()
