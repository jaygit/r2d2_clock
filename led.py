from gpiozero import LED
from time import sleep

RED = LED(27)
BLUE = LED(23)
GREEN = LED(24)
YELLOW = LED(22)

while True:
    RED.on()
    sleep(1)
    RED.off()
    sleep(1)
    GREEN.on()
    sleep(1)
    GREEN.off()
    sleep(1)
    BLUE.on()
    sleep(1)
    BLUE.off()
    sleep(1)
    YELLOW.on()
    sleep(1)
    YELLOW.off()
    sleep(1)
