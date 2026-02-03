#made with chatgpt
import threading
import time
import kmNet
import keyboard
from keyboard import mouse

KM_CONFIG = {
    "ip": "192.168.2.188",
    "port": "",
    "mac": ""
}

KEY_SPACE = 44

ACTIVATION_MOUSE_BUTTON = 'x2'
EXIT_KEY = 'end'

TICK_64_MS = 13.5
PRE_HEAT_DELAY = (TICK_64_MS * 0.99) / 1000.0
LOOP_DELAY = (TICK_64_MS * 1.99) / 1000.0

PRESS_TIME_MS = 8

running = True

status = kmNet.init(
    KM_CONFIG["ip"],
    KM_CONFIG["port"],
    KM_CONFIG["mac"]
)

if status != 0:
    print(f"[ERROR] kmbox init failed: {status}")
    raise SystemExit

print("[INFO] kmbox Net 初始化成功")
print("--- CS2 BunnyHop ---")
print("Press mouse5 for bhop | End / Ctrl+C to exit")

def send_jump():
    kmNet.keydown(KEY_SPACE)
    time.sleep(PRESS_TIME_MS / 1000.0)
    kmNet.keyup(KEY_SPACE)

def bhop_loop():
    global running
    print("[INFO] BunnyHop loop started")

    while running:
        if keyboard.is_pressed(EXIT_KEY):
            print("[INFO] End pressed")
            running = False
            break

        if mouse.is_pressed(button=ACTIVATION_MOUSE_BUTTON):
            send_jump()
            time.sleep(PRE_HEAT_DELAY)
            send_jump()
          
            while mouse.is_pressed(button=ACTIVATION_MOUSE_BUTTON) and running:
                send_jump()
                time.sleep(LOOP_DELAY)
        else:
            time.sleep(0.001)

t = threading.Thread(target=bhop_loop, daemon=True)
t.start()

try:
    while running:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Ctrl+C detected")

running = False
kmNet.keyup(KEY_SPACE)
print("[INFO] Kmbox quited")
