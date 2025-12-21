import re
import time
from pathlib import Path

import win32api
import win32clipboard
import global_hotkeys
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

logger = LoggerSrv.LoggerManager().get_logger("ClipboardRegex")


def regex_clipboard_text(expression: str):
    win32clipboard.OpenClipboard()
    try:
        # this could cause issues since CF_OEMTEXT and utf-8 is assumed,
        # not sure whether normally (ctrl + c) copied text will hold anything else, though
        data = win32clipboard.GetClipboardData(win32clipboard.CF_OEMTEXT).decode('utf-8')
        logger.debug(f"Succesfully retrieved {data}")
        match = re.fullmatch(expression, data)
        if match:
            expression_output = match.groups()
            if len(expression_output) > 0:
                if len(expression_output) > 1:
                    logger.warning(f'{expression} has multiple groups')
                filtered_data = match.group(1)  # retrieve the first group, ignore if multiple groups are defined
            else:
                filtered_data = match.group(0)  # fallback to full match if the regex does not have any groups
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(filtered_data.encode('utf-8'), win32clipboard.CF_TEXT)
            logger.info(f'Set clipboard text "{data.replace("\n", "").replace("\r", "")}" '
                        f'to: "{filtered_data.replace("\n", "").replace("\r", "")}"')
        else:
            logger.warning(f'"{data.replace("\n", "").replace("\r", "")}" did not match "{expression}",'
                           f' therefore the clipboard text was unmodified')
    except TypeError as e:
        logger.warning("Tried to fetch clipboard data, but the clipboard contained non-text")
        logger.warning(e)
    except win32api.error as e:
        logger.warning(f"win32api has failed")
        logger.warning(e)
    finally:
        win32clipboard.CloseClipboard()


def run() -> None:
    logger.info("Started")
    set_keybindings = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Keybindings')
    set_expressions = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Expressions')
    if len(set_expressions) != len(set_keybindings):
        logger.error(f"Number of expressions and keybindings do not match")
        raise NotImplementedError("default_config.json or / and config.json is incorrect in some way "
                                  "(set_keybindings and set_expressions are different lengths)")
    set_rules = []
    for x in range(len(set_keybindings)):  # The lists are interleaved to allow iterating through both of them at once
        set_rules.append((set_keybindings[x], set_expressions[x]))
    for keybinding, expression in set_rules:
        bindings = [
            {
                "hotkey": keybinding,
                "on_press_callback": None,
                "on_release_callback": lambda: regex_clipboard_text(expression),
                "actuate_on_partial_release": True
            },
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
