# Makefile to compile C files into shared object files

# Compiler
CC = cc

# Compiler flags
CFLAGS = -fPIC -shared

# Source files
SOURCES = $(wildcard *.c)

# Object files
OBJECTS = $(SOURCES:.c=.so)

all: $(OBJECTS)

%.so: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f *.so