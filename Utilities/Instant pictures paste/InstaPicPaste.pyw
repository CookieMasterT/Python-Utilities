import global_hotkeys
import time
import os
from PIL import ImageGrab


def image_to_file():
    im = ImageGrab.grabclipboard()
    startPath = os.getcwd()
    filePath = R'\Image.png'
    try:
        im.save(startPath + filePath,'PNG')
    except IOError:
        print("not a image")
    command = f'powershell Set-Clipboard -LiteralPath {filePath}'
    os.system(command)
    

bindings = [
    ["control + 0x5B + i", None, image_to_file, True],
]

global_hotkeys.register_hotkeys(bindings)

global_hotkeys.start_checking_hotkeys()

while True: # sleep indefinitely
    time.sleep(0.1)