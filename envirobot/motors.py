# Motor1.py
# Motor forward & backward

import RPi.GPIO as GPIO
import time

P_MOTB1 = 14
P_MOTB2 = 15
P_MOTA1 = 23
P_MOTA2 = 24

H = GPIO.HIGH
L = GPIO.LOW

FORWARD  = [H,L,H,L]
BACKWARD = [L,H,L,H]
STOP     = [L,L,L,L]
LEFT     = [H,L,L,H]
RIGHT    = [L,H,H,L]


def move(command):
    a1, a2, b1, b2 = command
    GPIO.output(P_MOTA1, a1)
    GPIO.output(P_MOTA2, a2)
    GPIO.output(P_MOTB1, b1)
    GPIO.output(P_MOTB2, b2)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_MOTA1, GPIO.OUT)
    GPIO.setup(P_MOTA2, GPIO.OUT)
    GPIO.setup(P_MOTB1, GPIO.OUT)
    GPIO.setup(P_MOTB2, GPIO.OUT)

print("starting")
setup()
while True:
    print("forward")
    move(FORWARD)
    time.sleep(2)
    print("backward")
    move(BACKWARD)
    time.sleep(2)
    print("left")
    move(LEFT)
    time.sleep(2)
    print("right")
    move(RIGHT)
    time.sleep(2)
    print("stop")
    move(STOP)
    time.sleep(5)
