#!/usr/bin/bash

gcc -O0 -c get_key.c decrypt.c

ld -r get_key.o decrypt.o -o get_key_and_decrypt.o
