#include <bcm2835.h>
#include <stdio.h>
#define PIN RPI_V2_GPIO_P1_29

int main(int argc, char **argv) {
	// If error, end program
	 if (!bcm2835_init())
      return 1;
	// Set the pin to be an output
    bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);

	while(1) {
	// Turn it on
	bcm2835_gpio_write(PIN, HIGH);
	// wait a bit
	bcm2835_delay(1000);
	// turn it off
	bcm2835_gpio_write(PIN, LOW);
	// wait a bit
	bcm2835_delay(1000);
	}
	
    bcm2835_close();
    return 0;
}