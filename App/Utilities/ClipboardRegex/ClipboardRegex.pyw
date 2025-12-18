import re
import time
from pathlib import Path
import win32api
import win32clipboard
import global_hotkeys
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

logger = LoggerSrv.LoggerManager().get_logger("ClipboardRegex")


def regex_clipboard_text(expression):
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_OEMTEXT).decode('utf-8')
        logger.debug(f"Succesfully retrieved {data}")
        match = re.fullmatch(expression, data)
        if match:
            expression_output = match.groups()
            if len(expression_output) > 0:
                filtered_data = match.group(1)
            else:
                filtered_data = match.group(0)
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(filtered_data.encode('utf-8'), win32clipboard.CF_TEXT)
            logger.info(f'Set clipboard text "{data.replace("\n", "").replace("\r", "")}" '
                        f'to: "{filtered_data.replace("\n", "").replace("\r", "")}"')
        else:
            logger.warning(f'"{data.replace("\n", "").replace("\r", "")}" did not match "{expression}",'
                           f' therefore the clipboard text was unmodified')
    except TypeError:
        logger.warning("Tried to fetch clipboard data, but the clipboard contained non-text")
    except win32api.error as e:
        logger.warning(f"win32api error: {e}")
    win32clipboard.CloseClipboard()


def run():
    logger.info("Started")
    set_keybindings = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Keybindings')
    set_expressions = ConfigREST.get(f'Utilities.{Path(__file__).name.split('.')[0]}.Expressions')
    if len(set_expressions) != len(set_keybindings):
        raise NotImplementedError("default_config.json is incorrect in some way "
                                  "(set_keybindings and set_expressions are different lengths)")
    # The 2 lists are interleaved to allow iterating through both of them at the same time
    set_rules = []
    for x in range(len(set_keybindings)):
        set_rules.append((set_keybindings[x], set_expressions[x]))
    for keybinding, expression in set_rules:
        bindings = [
            [keybinding, None, lambda: regex_clipboard_text(expression), True],
        ]
        global_hotkeys.register_hotkeys(bindings)
    global_hotkeys.start_checking_hotkeys()
    while True:  # sleep indefinitely
        time.sleep(1)


if __name__ == "__main__":
    run()
