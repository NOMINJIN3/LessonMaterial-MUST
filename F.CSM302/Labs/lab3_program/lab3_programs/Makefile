# Lab 3 - Chapter 3 Programming Problems (3.18 - 3.27)
CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -O2
JAVAC   ?= javac

# shm_open() lives in librt on (older) Linux; macOS has no librt -> no flag there.
ifeq ($(shell uname -s),Linux)
LDLIBS  ?= -lrt
else
LDLIBS  ?=
endif

C_TARGETS = \
	p3_18_zombie/zombie \
	p3_19_time/time_shm \
	p3_19_time/time_pipe \
	p3_20_pid_manager/pid_test \
	p3_21_collatz_fork/collatz_fork \
	p3_22_collatz_shm/collatz_shm \
	p3_26_reverse_case/reverse_case \
	p3_27_filecopy/filecopy

JAVA_DIRS = p3_23_quote_server p3_24_haiku_server p3_25_echo_server

all: c java

c: $(C_TARGETS)

java:
	for d in $(JAVA_DIRS); do $(JAVAC) $$d/*.java || exit 1; done

p3_20_pid_manager/pid_test: p3_20_pid_manager/pid_test.c p3_20_pid_manager/pid_manager.c p3_20_pid_manager/pid_manager.h
	$(CC) $(CFLAGS) -o $@ p3_20_pid_manager/pid_test.c p3_20_pid_manager/pid_manager.c

%: %.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f $(C_TARGETS)
	rm -f p3_2*/*.class

.PHONY: all c java clean
