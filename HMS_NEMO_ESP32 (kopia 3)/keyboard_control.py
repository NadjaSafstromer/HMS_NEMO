import pygame
import serial
import time

# =====================================
# HMS NEMO - KEYBOARD CONTROLLER
# =====================================

SERIAL_PORT = "/dev/cu.usbserial-1120"
BAUD_RATE = 9600

# Connect to ESP32-S3
esp32 = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

# Allow ESP32 to initialize
time.sleep(9)

pygame.init()

screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("HMS NEMO Controller")

clock = pygame.time.Clock()

running = True
active_key = None

last_heartbeat = time.monotonic()

key_mapping = {
    pygame.K_w: "w",
    pygame.K_s: "s",
    pygame.K_a: "a",
    pygame.K_d: "d"
}


def send_command(command):
    esp32.write((command + "\n").encode("utf-8"))
    print("Sent:", command)


print("HMS NEMO Keyboard Controller Ready")

print("W = Forward")
print("S = Backward")
print("A = Rotate Left")
print("D = Rotate Right")
print("X = Emergency Stop")

try:
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                send_command("x")
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_x:
                    send_command("x")
                    active_key = None

                elif event.key in key_mapping:

                    new_key = key_mapping[event.key]

                    if active_key != new_key:
                        active_key = new_key
                        send_command(active_key)

            elif event.type == pygame.KEYUP:

                if event.key in key_mapping:

                    released_key = key_mapping[event.key]

                    if active_key == released_key:
                        send_command("r")
                        active_key = None

        # Send heartbeat every 0.25 seconds
        current_time = time.monotonic()

        if current_time - last_heartbeat >= 0.25:
            send_command("h")
            last_heartbeat = current_time

        screen.fill((25, 30, 40))

        pygame.display.flip()

        clock.tick(60)

finally:
    try:
        send_command("x")
    except serial.SerialException:
        pass

    esp32.close()
    pygame.quit()