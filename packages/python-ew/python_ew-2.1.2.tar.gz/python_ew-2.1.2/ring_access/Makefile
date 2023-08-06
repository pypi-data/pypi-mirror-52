CFLAGS = -fPIC -m64 -Dlinux -D_LINUX -D_INTEL -D_USE_SCHED  -D_USE_PTHREADS -D_USE_TERMIOS
CC = gcc
LIB = -lm -lpthread

all: build

build:
	$(CC) $(CFLAGS) -I$(EW_INCLUDE) -L$(EW_LIB) $(LIB) -c ringwriter.c
	$(CC) $(CFLAGS) -I$(EW_INCLUDE) -L$(EW_LIB) $(LIB) -c ringreader.c

clean:
	rm -rf *.o
