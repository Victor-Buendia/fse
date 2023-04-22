#include <bcm2835.h>
#include <stdio.h>

#define LED1 RPI_V2_GPIO_P1_29
#define LED2 RPI_V2_GPIO_P1_31
#define LED3 RPI_V2_GPIO_P1_33
#define LED4 RPI_V2_GPIO_P1_35
#define LED5 RPI_V2_GPIO_P1_37

#define MAX 32

int main(int argc, char **argv) {
	// If error, end program
	 if (!bcm2835_init())
      return 1;
	// Set the pin to be an output
    bcm2835_gpio_fsel(LED1, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED2, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED3, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED4, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED5, BCM2835_GPIO_FSEL_OUTP);

	int counter = 0;
	while(1) {
	// wait a bit
	bcm2835_delay(1000);
	// turn it off
	bcm2835_gpio_write(LED1, (counter & 0b00001)?(HIGH):(LOW));
	bcm2835_gpio_write(LED2, (counter & 0b00010)?(HIGH):(LOW));
	bcm2835_gpio_write(LED3, (counter & 0b00100)?(HIGH):(LOW));
	bcm2835_gpio_write(LED4, (counter & 0b01000)?(HIGH):(LOW));
	bcm2835_gpio_write(LED5, (counter & 0b10000)?(HIGH):(LOW));
	// wait a bit
	bcm2835_delay(1000);

	counter++;
	if(counter == MAX)
		counter = 0;
	}
	
    bcm2835_close();
    return 0;
}