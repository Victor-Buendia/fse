b_sizes = {
	"int": 4
	, "float": 4
}

request_menu = {
	"INT": 0xA1
	, "FLOAT": 0xA2
	, "STRING": 0xA3
}

destination_register = 0x01

gpio_pins = {
	"clk": (16, "in", "pud_down")
	, "dt": (20, "in", "pud_down")
	, "sw": (21, "in", "pud_down")
	, "resistor": (23, "out", None)
	, "cooler": (24, "out", None)
	, "ti": (4, "in", "pud_down")
}