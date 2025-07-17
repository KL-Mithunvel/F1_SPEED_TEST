import time
from rpi_ws281x import PixelStrip, Color

# LED configuration:
LED_COUNT = 16          # Number of LEDs in one ring
LED_PIN = 18            # GPIO18 (must support PWM!)
LED_FREQ_HZ = 800000    # LED signal frequency (Hz)
LED_DMA = 10            # DMA channel to use
LED_BRIGHTNESS = 64     # Brightness (0-255)
LED_INVERT = False      # Invert signal (False for Pi)
LED_CHANNEL = 0

# Create PixelStrip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                   LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def show_color(color, delay_sec):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    print(f"Showing color {color} for {delay_sec} seconds...")
    time.sleep(delay_sec)

try:
    show_color(Color(255, 0, 0), 5)   # Red
    show_color(Color(0, 255, 0), 5)   # Green
    show_color(Color(0, 0, 0), 1)     # Off
    print("✅ Test complete.")

except KeyboardInterrupt:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("🛑 Interrupted. LEDs off.")
