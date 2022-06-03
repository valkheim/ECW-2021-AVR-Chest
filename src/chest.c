#define F_CPU 		(16000000UL)			// 16 MHz
#define BAUD 		(9600)				// Desired bandwidth (Bps)
#define UBRR 		((F_CPU / 16 / BAUD) - 1)	// Estimated baud rate
#define MAX_BUFFER_SIZE	(32)

#define _STRINGIFY(X)	#X		// STRINGIFY_IMPL(FLAG) => "FLAG"
#define STRINGIFY(X)	_STRINGIFY(X)	// STRINGIFY(FLAG) => "ECW{flag_value}"

#include <avr/io.h> // iom328p.h
uint8_t flag[] = STRINGIFY(FLAG);

void usart_init(uint8_t const ubrr)
{
	// Set baud rate
	UBRR0H = (uint8_t)(ubrr >> 8);
	UBRR0L = (uint8_t)(ubrr);

	// Enable rx/tx
	UCSR0B = (1 << RXEN0) | (1 << TXEN0);

	// Set frame format (8 data, 1 stop)
	UCSR0C = (3 << UCSZ00);
}

void usart_transmit_byte(uint8_t const data)
{
	// Wait TX
	while (!(UCSR0A & (1 << UDRE0)));
	UDR0 = data;
}

void usart_transmit_bytes(uint8_t const * const data, uint8_t const size)
{
	for (uint8_t i = 0 ; i < size ; ++i)
		usart_transmit_byte(data[i]);
}

uint8_t usart_receive_byte(void)
{
	// Wait RX
	while (!(UCSR0A & (1 << RXC0)));
	return UDR0;
}

void usart_receive_bytes(uint8_t * const data, uint8_t const requested_size)
{
	for (uint8_t i = 0 ; i < requested_size ; ++i)
		data[i] = usart_receive_byte();
}

uint8_t ask_key(void)
{
	uint8_t prompt[] = "Enter key\n";
	uint8_t prompt_size = sizeof(prompt) / sizeof(*prompt);
	usart_transmit_bytes(prompt, prompt_size);
	return usart_receive_byte();
}

void decode_flag(uint8_t const key)
{
	uint8_t flag_size = sizeof(flag) / sizeof(*flag);
	for (uint8_t i = 0 ; i < flag_size ; i += 2)
		usart_transmit_byte((flag[i] - ROT_KEY ) ^ key);

	usart_transmit_byte('\n');
}

int main(void)
{
	usart_init(UBRR);
	for (;;) decode_flag(ask_key());
}
