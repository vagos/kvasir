CC = gcc
CFLAGS = -Wall -Wextra -O2

PROGS = primenum mersene adder

all: $(PROGS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

.PHONY: all clean

clean:
	rm -f $(PROGS)