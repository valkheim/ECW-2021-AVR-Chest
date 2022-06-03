NAME=blinky
MCU=atmega328p
QEMU_MCU=uno # see qemu-system-avr -machine help for a full list
DEBUG=#-gdwarf-2 -g3 -D DEBUG

all: $(NAME).elf $(NAME).hex

$(NAME).elf:
	avr-gcc $(DEBUG) -DF_CPU=16000000UL -Os -mmcu=$(MCU) -o $(NAME).elf $(NAME).c

$(NAME).hex:
	avr-objcopy -j .text -O ihex $(NAME).elf $(NAME).hex

test: $(NAME).elf
	tmux new -d -s debug
	tmux send 'qemu-system-avr -S -s -nographic -machine $(QEMU_MCU) -bios $(NAME).elf' ENTER
	tmux split-window
	tmux send 'avr-gdb -ex "target remote :1234" $(NAME).elf' ENTER
	tmux a

clean:
	rm -f $(NAME).elf
	rm -f $(NAME).hex

re: clean all
