import RPi.GPIO as RPIO
import constants as C
# https://pythonhosted.org/RPIO/
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/

io = {
	"in": RPIO.IN
	, "out": RPIO.OUT
	, "pud_down": RPIO.PUD_DOWN
	, None: None
}

class GPIO:
	def __init__(self):
		RPIO.setmode(RPIO.BCM)
		self.setup_pins()

	def setup_pins(self):
		for pin in C.gpio_pins.keys():
			bcm_pin, io_type, pud = C.gpio_pins[pin]
			
			if io_type == "in":
				RPIO.setup(bcm_pin, io[io_type], pull_up_down=io[pud])
			else:
				RPIO.setup(bcm_pin, io[io_type], initial=RPIO.LOW)

	def cleanup_pins(self):
		RPIO.cleanup()

	def set_pin(self, pin_name, value):
		RPIO.output(C.gpio_pins[pin_name], RPIO.HIGH if value else RPIO.LOW)


if __name__ == "__main__":
	gpio = GPIO()
	RPIO.cleanup()