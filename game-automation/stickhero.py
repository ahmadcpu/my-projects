""" 
Automating stick-hero game using adb shell.
"""

from ppadb.client import Client
import numpy as np
from time import sleep
from PIL import Image
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]

while True:
    image = device.screencap()

    with open("screen.png", 'wb') as f:
        f.write(image)

    image = Image.open("screen.png")
    image = np.array(image)
    pixels = [list(i[:3]) for i in image[850]]

    p1 = True
    p2 = False
    p3 = False
    p4 = False
    first_black = 0
    first_black2 = 0
    last_black = 0
    for e,i in enumerate(pixels):
        if i[0] == 0 and p1:
            p1 = False
            p2 = True
        if i[0] != 0 and p2:
            first_black = e
            p2 = False
            p3 = True
        if i[0] == 0 and p3:
            first_black2 = e
            p3 = False
            p4 = True
        if i[0] != 0 and p4:
            last_black = e
            break

    print(first_black, first_black2, last_black)

    num = (last_black + first_black2) / 2 - first_black
    device.shell(f'input touchscreen swipe 360 360 360 360 {int(num*1.4)}')
    sleep(3)