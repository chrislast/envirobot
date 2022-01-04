from evdev import InputDevice, categorize, ecodes
from motors import move, FORWARD, BACKWARD, LEFT, RIGHT, STOP
from pathlib import Path
import logging
from time import sleep

# logging.basicConfig(format="$(date) $(level) $(msg)",level=logging.INFO, datefmt="H:M:s")
log = logging.getLogger(__name__)

mode = Path("/home/pi/enviromode.txt")
text = Path("/home/pi/envirotext.txt")

# 8BitDo SN30pro

# EV_KEY

btnA = 305
btnB = 304
btnX = 307
btnY = 306

start = 313
select = 312

trigL1 = 308
trigL2 = 310

trigR1 = 309
trigR2 = 311

star = 317
power = 316

# EV_ABS

up_down = 17
left_right = 16

joyLX = 0
joyLY = 1

joyRX = 3
joyRY = 4

#loop and filter by event code and print the mapped label

def get_controller():
    while True:
        try:
            controller = InputDevice('/dev/input/event1')
            print(controller)

        except FileNotFoundError:
            print("Turn on controller...")
            sleep(1)

        else:
            return controller

def loop(controller):
    rx = ry = lx = ly = 0

    for event in controller.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:
                if event.code == btnA:
                    log.info("A")
                    mode.write_text("1")
                elif event.code == btnB:
                    log.info("B")
                    mode.write_text("2")
                elif event.code == btnX:
                    log.info("X")
                    mode.write_text("3")
                elif event.code == btnY:
                    log.info("Y")
                    mode.write_text("4")

                elif event.code == start:
                    log.info("start")
                elif event.code == select:
                    log.info("select")
                elif event.code == star:
                    log.info("star")
                elif event.code == power:
                    log.info("power")

                elif event.code == trigL1:
                    log.info("left trigger 1")
                elif event.code == trigL2:
                    log.info("left trigger 2")
                elif event.code == trigR1:
                    log.info("right trigger 1")
                elif event.code == trigR2:
                    log.info("right trigger 2")


        if event.type == ecodes.EV_ABS:
            if event.code == up_down:
                if event.value == 1:
                    log.info("down")
                elif event.value == -1:
                    log.info("up")

            elif event.code == left_right:
                if event.value == 1:
                    log.info("right")
                elif event.value == -1:
                    log.info("left")

            elif event.code == 0:
                lx = event.value - 32768
                log.info(f"left x={lx}, y={ly}")
            elif event.code == 1:
                ly = 32768 - event.value
                log.info(f"left x={lx}, y={ly}")
            elif event.code == 3:
                rx = event.value - 32768
                log.info(f"right x={rx}, y={ry}")
            elif event.code == 4:
                ry = 32768 - event.value
                log.info(f"right x={rx}, y={ry}")

        if abs(ly) <= 16000:
            if abs(lx) <= 16000:
                move(STOP)
            elif lx > 16000:
                log.info("RIGHT")
                move(RIGHT)
            else:
                log.info("LEFT")
                move(LEFT)
        else:
            if abs(ly) > abs(lx):
                if ly > 0:
                    log.info("FORWARD")
                    move(FORWARD)
                else:
                    log.info("BACKWARD")
                    move(BACKWARD)
            else:
                if lx > 16000:
                    log.info("RIGHT")
                    move(RIGHT)
                else:
                    log.info("LEFT")
                    move(LEFT)

def main():
    while True:
        try:
            controller = get_controller()
            loop(controller)

        except KeyboardInterrupt:
            break

        except OSError:
            pass

if __name__ == "__main__":
    main()
