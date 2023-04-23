#include <bcm2835.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#define BUTTON_PIN RPI_V2_GPIO_P1_23 // GPIO 11

volatile sig_atomic_t button_state = -1;

void signal_handler(int signal)
{
	button_state = bcm2835_gpio_lev(BUTTON_PIN);
	printf("The button's state changed to: %d\n", button_state);
}

int main(int argc, char **argv)
{
    // If error, end program
    if (!bcm2835_init()) {
        return 1;
    }

    bcm2835_gpio_fsel(BUTTON_PIN, BCM2835_GPIO_FSEL_INPT);  // Set the button pin as input
    bcm2835_gpio_set_pud(BUTTON_PIN, BCM2835_GPIO_PUD_UP);   // Enable pull-up resistor

    signal(SIGUSR1, signal_handler);   // Register signal handler for SIGUSR1

    printf("Press the button to see its state:\n");

    while (1) {
        bcm2835_delay(100);  // Wait for 100ms before checking the button state again
		if(bcm2835_gpio_lev(BUTTON_PIN) != button_state)
			raise(SIGUSR1);
    }

    bcm2835_close();  // Close the bcm2835 library

    return 0;
}
