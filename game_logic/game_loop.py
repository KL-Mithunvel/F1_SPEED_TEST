from game_logic import gpio_handler as gpio

def play_single_round():
    index = gpio.get_random_index()
    gpio.turn_on_led(index)
    hit = gpio.wait_for_correct_button(index)
    gpio.turn_off_led(index)
    return hit
