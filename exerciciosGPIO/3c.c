#include <bcm2835.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>


#define BUTTON_PIN RPI_V2_GPIO_P1_23 // GPIO 11
#define DEBOUNCE_TIME_MS 50 // Debounce time in milliseconds

volatile sig_atomic_t last_state = -1;
static clock_t last_time = 0;

volatile sig_atomic_t current_state = -1;
static clock_t current_time = 0;

volatile sig_atomic_t state_changed = 0;

void signal_handler(int signal)
{
	current_time = clock();
	current_state = bcm2835_gpio_lev(BUTTON_PIN);

	if(current_state != last_state)
		if((current_time - last_time) >= (DEBOUNCE_TIME_MS * CLOCKS_PER_SEC / 1000)) {
			last_state = current_state;
			last_time = current_time;
			state_changed = 1;
		}
}

int main(int argc, char **argv)
{
    // If error, end program
    if (!bcm2835_init())
        return 1;

    bcm2835_gpio_fsel(BUTTON_PIN, BCM2835_GPIO_FSEL_INPT);  // Set the button pin as input
    bcm2835_gpio_set_pud(BUTTON_PIN, BCM2835_GPIO_PUD_UP);   // Enable pull-up resistor

    signal(SIGUSR1, signal_handler);   // Register signal handler for SIGUSR1

    printf("Press the button to see its state:\n");

    while (1) {
		raise(SIGUSR1);
		if(state_changed) {
			state_changed = 0;
			printf("The button's state changed to: %d\n", last_state);
		}
    }

    bcm2835_close();  // Close the bcm2835 library

    return 0;
}
