/*
Polling for input means checking for input periodically on an as needed basis.
Polled input is the simplest method of input on the Raspberry Pi.
For a desired pin, the state of the input pin is checked for the input value.
*/
#include <bcm2835.h>
#include <stdio.h>

#define BUTTON_PIN RPI_V2_GPIO_P1_23 // GPIO 11

int main(int argc, char **argv) {
	// If error, end program
    if (!bcm2835_init())
        return 1;
    
    // Set BUTTON_PIN as an input pin with a pull-up resistor
    bcm2835_gpio_fsel(BUTTON_PIN, BCM2835_GPIO_FSEL_INPT);
    bcm2835_gpio_set_pud(BUTTON_PIN, BCM2835_GPIO_PUD_UP);
    
	int button_state = bcm2835_gpio_lev(BUTTON_PIN);
	printf("Initial state of GPIO 11: %d\n", button_state);
    while (1) {
        // Poll the state of the button every 500 milliseconds
        bcm2835_delay(500);
        
		if(button_state != bcm2835_gpio_lev(BUTTON_PIN)) {
        	printf("State of GPIO 11 changed to: %d\n", bcm2835_gpio_lev(BUTTON_PIN));
			button_state = bcm2835_gpio_lev(BUTTON_PIN);
		}
    }
    
    bcm2835_close();
    return 0;
}
