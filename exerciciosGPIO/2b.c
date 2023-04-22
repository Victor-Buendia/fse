/*
Debouncing is removing unwanted input noise from buttons, switches or other user input. 
*/

#include <bcm2835.h>
#include <stdio.h>
#include <stdbool.h>
#include <time.h>

#define BUTTON_PIN RPI_V2_GPIO_P1_23 // GPIO 11
#define DEBOUNCE_TIME_MS 50 // Debounce time in milliseconds

static bool last_state = HIGH;
static clock_t last_time = 0;

bool is_button_pressed(void) {
    bool current_state = bcm2835_gpio_lev(BUTTON_PIN);
    clock_t current_time = clock();
    
    if (current_state != last_state) {
        if ((current_time - last_time) >= (DEBOUNCE_TIME_MS * CLOCKS_PER_SEC / 1000)) {
            last_state = current_state;
            last_time = current_time;
            return true;
        }
    } 
    
    return false;
}

int main(int argc, char **argv) {
    // If error, end program
    if (!bcm2835_init())
        return 1;
    
    // Set BUTTON_PIN as an input pin with a pull-up resistor
    bcm2835_gpio_fsel(BUTTON_PIN, BCM2835_GPIO_FSEL_INPT);
    bcm2835_gpio_set_pud(BUTTON_PIN, BCM2835_GPIO_PUD_UP);
    
    printf("Button current state: %d\n", last_state);
    while (1) {
        if (is_button_pressed()) {
            printf("Button state changed to: %d\n", last_state);
        }
    }
    
    bcm2835_close();
    return 0;
}
