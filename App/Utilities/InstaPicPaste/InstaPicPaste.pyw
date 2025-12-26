import os
import subprocess
import time
from pathlib import Path
import global_hotkeys
from PIL import ImageGrab
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

logger = LoggerSrv.get_logger("InstaPicPaste")


def image_to_file() -> None:
    im = ImageGrab.grabclipboard()

    file_name = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.FileName')
    file_format = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.FileFormat')

    start_path = Path(__file__).parents[0] / "Images"
    file_path = f"{file_name}.{file_format.lower()}"
    full_path = start_path / file_path

    for f in os.listdir(start_path):
        file_path = start_path / f
        if not file_path == full_path:
            logger.info(fr'Cleared "{f}" from \Images')
            os.remove(file_path)

    try:
        im.save(full_path, file_format)
        logger.info(f"Succesfully saved image from clipboard into: {full_path}")
    except AttributeError as e:
        logger.warning("Tried to convert clipboard image to file, but the clipboard contained a non-image")
        logger.warning(e)
        return
    except IOError as e:
        logger.error("Path is invalid or the program does not have access to its own directory")
        logger.error(e)
        raise IOError("The program cannot failed to save a file inside itself"
                      "(Is the directory access locked, readonly or otherwise unusable?)")
    try:
        subprocess.run(
            ["powershell", "Set-Clipboard", "-LiteralPath", str(full_path)],
            check=True,
            capture_output=True,
        )
        logger.info("succesfully copied file into clipboard")
    except subprocess.CalledProcessError as e:
        logger.error(f'Powershell failed with return code: "{e.returncode}"')
        subprocess_output = ""
        if e.stdout:
            subprocess_output += e.stdout.decode()
        if e.stderr:
            subprocess_output += e.stderr.decode()
        logger.error(f'subprocess output: "{subprocess_output}"')


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
