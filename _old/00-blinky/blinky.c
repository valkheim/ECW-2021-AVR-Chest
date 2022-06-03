#define F_CPU 16000000UL	// Speed of the microprocessor, in hertz (16 MHz)
#include <avr/io.h>             // provides PORT* and DDR* registers
#include <util/delay.h>         // provides _delay_ms(), and needs F_CPU

#define LED _BV(PB0)		// = (1 << PB0)
#define LED_DDR DDRB
#ifdef DEBUG
int mock_led;
# define LED_PORT mock_led
#else
# define LED_PORT PORTB
#endif

int main (void) {
  LED_DDR = LED;		// Set the LED pin as an output

  for(;;) {
    LED_PORT ^= LED;		// Toggles just the LED pin
    _delay_ms(1000);
  }
}

