import os
import time
from pathlib import Path
import global_hotkeys
from PIL import ImageGrab
from App.internal_scripts import ConfigREST


def image_to_file():
    im = ImageGrab.grabclipboard()
    start_path = os.getcwd()
    file_path = r'\Image.png'
    full_path = start_path + file_path
    try:
        im.save(full_path, 'PNG')
    except IOError:
        print("not an image")
    command = f'powershell Set-Clipboard -LiteralPath {full_path}'
    os.system(command)


bindings = [
    [ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Keybinding'), None, image_to_file, True],
]

global_hotkeys.register_hotkeys(bindings)

global_hotkeys.start_checking_hotkeys()

while True:  # sleep indefinitely
    time.sleep(1)
