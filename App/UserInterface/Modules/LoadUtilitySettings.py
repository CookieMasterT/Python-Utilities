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
        ttk.Label(mainframe, text=data["Description"]).grid(column=0, row=1, sticky="W E")