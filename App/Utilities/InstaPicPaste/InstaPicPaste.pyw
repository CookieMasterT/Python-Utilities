import subprocess
import time
from pathlib import Path
import global_hotkeys
from PIL import ImageGrab
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

logger = LoggerSrv.LoggerManager().get_logger("InstaPicPaste")


def image_to_file() -> None:
    im = ImageGrab.grabclipboard()
    start_path = Path(__file__).parents[0]
    file_path = 'Image.png'
    full_path = start_path / file_path
    try:
        im.save(full_path, 'PNG')
        logger.info(f"Succesfully saved {full_path}")
    except (IOError, AttributeError):
        logger.warning("Tried to convert, but the clipboard contained a non-image")
    subprocess.run(
        ["powershell", "Set-Clipboard", "-LiteralPath", str(full_path)],
        check=True,
        capture_output=True
    )


def run() -> None:
    logger.info("Started")
    keybinding = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Keybinding')
    bindings = [
        {
            "hotkey": keybinding,
            "on_press_callback": None,
            "on_release_callback": image_to_file,
            "actuate_on_partial_release": True
        }
    ]
    global_hotkeys.register_hotkeys(bindings)
    global_hotkeys.start_checking_hotkeys()
    try:  # sleep indefinitely until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.error("Interrupted by user")


if __name__ == "__main__":
    run()
