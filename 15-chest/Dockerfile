FROM debian:stable-slim

RUN apt-get update -y && \
    apt-get install -y -q python3 && \
    apt-get install -y -q make    && \
    apt-get install -y -q avr-libc binutils-avr gcc-avr gdb-avr qemu-system-avr

# RUN apt-get install -y -q procps netcat

WORKDIR /chest
COPY entrypoint.sh chest.c generate.py Makefile ./

EXPOSE 5678

ENTRYPOINT ["/chest/entrypoint.sh"]
