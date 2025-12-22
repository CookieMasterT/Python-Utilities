import json
from pathlib import Path
from tkinter import ttk
from typing import Any
from App.InternalScripts.Logging import LoggerSrv


class UtilitySettingsLoader:
    logger = LoggerSrv.LoggerManager().get_logger("LoadUtilitySettings")

    def load(self, utility_name, mainframe) -> Any:
        self.logger.info(f'Loading data for utility: "{utility_name}"')
        data = {}
        with open(Path(__file__).parents[2] / f"Utilities/{utility_name}/data.json") as f:
            data = json.load(f)
        ttk.Label(mainframe, text=data["LongName"]).grid(column=0, row=0, sticky="W E")
        ttk.Label(mainframe, text=data["Description"], wraplength=750).grid(column=0, row=1, sticky="W E")
        options = ttk.Frame(mainframe, padding=(10, 10, 10, 10))
        options.grid(column=0, row=2, sticky="N S E W")
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)

        i = 0
        for ConfigOption in data["ConfigInputs"]:
            option = ttk.Frame(options)
            option.grid(column=0, row=i, sticky="W E")
            option.columnconfigure(0, weight=1)
            option.columnconfigure(1, weight=1)

            left = ttk.Frame(option, border="2")
            left.grid(column=0, row=0, sticky="W E")

            (ttk.Label(left, text=ConfigOption)
             .grid(column=0, row=0, sticky="W E"))
            (ttk.Label(left, text=str(data["ConfigInputs"][ConfigOption][1]))
             .grid(column=0, row=1, sticky="W E"))

            (ttk.Label(option, anchor="e", text=data["ConfigInputs"][ConfigOption][0])
             .grid(column=1, row=0, sticky="N S E W"))
            i += 1
