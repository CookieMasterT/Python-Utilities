import json
from pathlib import Path
from tkinter import *
from tkinter import ttk
from App.InternalScripts.Logging import LoggerSrv
from App.InternalScripts.ConfigManagement import ConfigREST


class UtilitySettingsLoader:
    logger = LoggerSrv.get_logger("UtilitySettingsLoader")

    def __init__(self) -> None:
        # tkinter excepts the stringvars to be persistent.
        self.persistent_config_vars = []

    def on_change_config(self, i, location) -> None:
        value = self.persistent_config_vars[i].get()
        self.logger.info(f'Changing "{location}" to "{value}"')
        ConfigREST.put(location, value)

    def add_trace(self, i: int, data: dict, config_option: list) -> None:
        """
        Adds an on change trace to an persistent config var to update the config. Default for simple variables
        :param i: Position in persistent_config_vars
        :param data: The data from the json, passed from the main loop
        :param config_option: The name of the config option (which config from ConfigInputs is to be changed)
        """
        self.persistent_config_vars[i].trace_add("write",
                                                 lambda *args, _i=i,
                                                 save_location=data["ConfigInputs"][config_option][2]:
                                                 self.on_change_config(_i, save_location))

    def on_change_keo_config(self, i, list_pos, locations) -> None:
        target_location = locations[1]
        expressions_arr = ConfigREST.get(target_location)
        change = self.persistent_config_vars[i][list_pos].get()
        expressions_arr[list_pos] = change

        self.logger.info(f'Changing "{locations[1]}" at position "{list_pos}" to "{change}"')
        ConfigREST.put(target_location, expressions_arr)

    def add_keo_trace(self, i: int, list_pos: int, data: dict, config_option: list) -> None:
        """
        Adds an on change trace to an persistent config var to update the config. Meant for Keyboard Extra Options (KEO)
        :param i: Position in persistent_config_vars
        :param list_pos: Position in the list, beacuse KEO can have up to 10 positions
        :param data: The data from the json, passed from the main loop
        :param config_option: The name of the config option (which config from ConfigInputs is to be changed)
        """
        self.persistent_config_vars[i][list_pos].trace_add("write",
                                                           lambda *args, _i=i, _listpos=list_pos,
                                                           save_locations=data["ConfigInputs"][config_option][2]:
                                                           self.on_change_keo_config(_i, list_pos, save_locations))

    def load(self, utility_name, mainframe) -> None:
        self.logger.info(f'Loading data for utility: "{utility_name}"')

        for widget in mainframe.winfo_children():
            widget.destroy()

        data = {}
        with open(Path(__file__).parents[2] / f"Utilities/{utility_name}/data.json") as f:
            data = json.load(f)
        ttk.Label(mainframe, text=data["LongName"]).grid(column=0, row=0, sticky="W E")
        ttk.Label(mainframe, text=data["Description"], wraplength=750).grid(column=0, row=1, sticky="W E")
        options = ttk.Frame(mainframe, padding=(10, 10, 10, 10))
        options.grid(column=0, row=2, sticky="N S E W")
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)

        self.persistent_config_vars = []
        i = 0
        for ConfigOption in data["ConfigInputs"]:
            option = ttk.Frame(options)
            option.grid(column=0, row=i, sticky="W E")
            option.columnconfigure(0, weight=1)
            option.columnconfigure(1, weight=1)

            title = ttk.Frame(option, border="2")
            title.grid(column=0, row=0, sticky="W E")

            (ttk.Label(title, text=ConfigOption)
             .grid(column=0, row=0, sticky="W E"))
            (ttk.Label(title, text=str(data["ConfigInputs"][ConfigOption][1]))
             .grid(column=0, row=1, sticky="W E"))

            if data["ConfigInputs"][ConfigOption][0] == 'Text':
                self.persistent_config_vars.append(
                    StringVar(value=ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2]))))

                config_input = ttk.Entry(option, textvariable=self.persistent_config_vars[i])
                config_input.grid(column=1, row=0, sticky="E")
                self.add_trace(i, data, ConfigOption)

            elif data["ConfigInputs"][ConfigOption][0] == 'Enum':
                self.persistent_config_vars.append(
                    StringVar(value=ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2]))))
                config_input = ttk.Combobox(option, textvariable=self.persistent_config_vars[i],
                                            values=data["ConfigInputs"][ConfigOption][3:],
                                            state="readonly")
                config_input.grid(column=1, row=0, sticky="E")
                self.add_trace(i, data, ConfigOption)

            elif data["ConfigInputs"][ConfigOption][0] == 'Int':
                # untested implementation
                self.persistent_config_vars.append(
                    IntVar(value=ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2]))))
                config_input = ttk.Spinbox(option, from_=0, to=100, textvariable=self.persistent_config_vars[i])
                config_input.grid(column=1, row=0, sticky="E")
                self.add_trace(i, data, ConfigOption)

            elif data["ConfigInputs"][ConfigOption][0] == 'KeyboardExtraOptions':
                # choice instead of option since option is used above
                choice_list = ConfigREST.get(str(data["ConfigInputs"][ConfigOption][2][1]))
                print(str(data["ConfigInputs"][ConfigOption][2][1]))
                k = 0
                self.persistent_config_vars.append([])
                for choice in choice_list:
                    container = ttk.Frame(option)
                    container.grid(column=0, row=k + 1, sticky="W E")

                    self.persistent_config_vars[i].append(StringVar(value=choice))
                    (ttk.Label(container, text=f"{k + 1}: ")
                     .grid(column=0, row=0, sticky="W"))
                    config_input = ttk.Entry(container, textvariable=self.persistent_config_vars[i][k])
                    config_input.grid(column=1, row=0, sticky="W")
                    self.add_keo_trace(i, k, data, ConfigOption)
                    k += 1
            else:
                self.persistent_config_vars.append(StringVar())
            i += 1
