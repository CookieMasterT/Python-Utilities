import json
from time import time
from pathlib import Path
from tkinter import *
from tkinter import ttk
from typing import Any
from App.InternalScripts.Logging import LoggerSrv
from App.InternalScripts.ConfigManagement import ConfigREST


class UtilitySettingsLoader:
    logger = LoggerSrv.LoggerManager().get_logger("LoadUtilitySettings")
    SAVE_COOLDOWN = 3000  # 3 seconds

    def __init__(self) -> None:
        # tkinter excepts the stringvars to be persistent.
        self.persistent_config_vars = []
        self.save_timer = time()

    def on_change_config(self, i, location) -> None:
        value = self.persistent_config_vars[i].get()
        self.logger.info(f'Changing "{location}" to "{value}"')
        ConfigREST.put(location, value)

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

            if data["ConfigInputs"][ConfigOption][0] == 'Text':
                self.persistent_config_vars.append(
                    StringVar(value=ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2]))))

                config_input = ttk.Entry(option, textvariable=self.persistent_config_vars[i])
                config_input.grid(column=1, row=0, sticky="E")
            elif data["ConfigInputs"][ConfigOption][0] == 'Enum':
                self.persistent_config_vars.append(
                    StringVar(value=ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2]))))
                config_input = ttk.Combobox(option, textvariable=self.persistent_config_vars[i],
                                            values=data["ConfigInputs"][ConfigOption][3:],
                                            state="readonly")
                config_input.grid(column=1, row=0, sticky="E")
            else:
                self.persistent_config_vars.append(StringVar())
            self.persistent_config_vars[i].trace_add("write",
                                                     lambda *args, _i=i,
                                                     save_location=data["ConfigInputs"][ConfigOption][2]:
                                                     self.on_change_config(_i, save_location))
            # (ttk.Label(option, anchor="e", text=data["ConfigInputs"][ConfigOption][0])
            # .grid(column=1, row=0, sticky="N S E W"))
            i += 1
