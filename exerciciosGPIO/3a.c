#include <bcm2835.h>
#include <stdio.h>

#define BUTTON_PIN RPI_V2_GPIO_P1_23 // GPIO 11

void button_event_handler(void)
{
    printf("The button's state changed to: %d\n", bcm2835_gpio_lev(BUTTON_PIN));
}

int main(int argc, char **argv)
{
	// If error, end program
    if (!bcm2835_init())
        return 1;

    bcm2835_gpio_fsel(BUTTON_PIN, BCM2835_GPIO_FSEL_INPT);  // Set the button pin as input
    bcm2835_gpio_set_pud(BUTTON_PIN, BCM2835_GPIO_PUD_UP);   // Enable pull-up resistor

    bcm2835_gpio_ren(BUTTON_PIN);   // Enable rising edge detection
    bcm2835_gpio_fen(BUTTON_PIN);   // Enable falling edge detection

    bcm2835_gpio_set_eds(BUTTON_PIN);   // Clear any previous interrupts

    printf("Press the button to see its state:\n");

    while (1) {
        bcm2835_delay(100);  // Wait for 100ms before checking the button state again
        if (bcm2835_gpio_eds(BUTTON_PIN)) {   // Check if an event occurred on the button pin
            bcm2835_gpio_set_eds(BUTTON_PIN);   // Clear the event
            button_event_handler();   // Handle the event
        }
    }

    bcm2835_close();  // Close the bcm2835 library

    return 0;
}
