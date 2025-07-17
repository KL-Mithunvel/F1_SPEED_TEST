import time
import board
import neopixel

# === CONFIG ===
LED_COUNT = 16       # Number of LEDs in the ring
GPIO_PIN = board.D18 # Change this to your actual GPIO pin (e.g., board.D21)
BRIGHTNESS = 0.3     # 0.0 to 1.0

# === INIT ===
pixels = neopixel.NeoPixel(
    GPIO_PIN,
    LED_COUNT,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# === ACTION ===
def show_color(color, duration):
    pixels.fill(color)
    pixels.show()
    print(f"Showing color {color} for {duration} seconds...")
    time.sleep(duration)

try:
    show_color((255, 0, 0), 5)   # Red
    show_color((0, 255, 0), 5)   # Green
    pixels.fill((0, 0, 0))
    pixels.show()
    print("Done. LEDs turned off.")

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    print("Interrupted. LEDs off.")
