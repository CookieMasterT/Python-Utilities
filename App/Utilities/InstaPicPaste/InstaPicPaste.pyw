import os
import time
from pathlib import Path
import global_hotkeys
from PIL import ImageGrab
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

logger = LoggerSrv.get_logger("InstaPicPaste", __name__)


def image_to_file():
    im = ImageGrab.grabclipboard()
    start_path = Path(__file__).parents[0]
    file_path = r'.\Image.png'
    full_path = start_path.joinpath(file_path)
    try:
        im.save(full_path, 'PNG')
        logger.info(f"Succesfully saved {full_path}.png")
    except (IOError, AttributeError):
        logger.warn("Tried to convert, but the clipboard contained a non-image")
    command = f'powershell Set-Clipboard -LiteralPath {full_path}'
    os.system(command)


def run():
    logger.info("Running")
    bindings = [
        [ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Keybinding'), None, image_to_file, True],
    ]
    global_hotkeys.register_hotkeys(bindings)
    global_hotkeys.start_checking_hotkeys()
    while True:  # sleep indefinitely
        time.sleep(1)


if __name__ == "__main__":
    run()
