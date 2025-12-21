import os
from pathlib import Path
from tkinter import ttk
from typing import Any

from App.UserInterface.Modules.LoadUtilitySettings import UtilitySettingsLoader


class UtilityListLoader:
    def __init__(self) -> None:
        self.USLoader = UtilitySettingsLoader()

    def load(self, mainframe, options) -> Any:
        i = 0
        with os.scandir(Path(__file__).parents[2] / "Utilities") as files:
            for item in files:
                if item.is_dir():
                    (ttk.Button(options, text=f"{item.name}",
                                command=lambda _=item.name: self.USLoader.load(_, mainframe))
                     # the above is done so that the value is passed and it doesn't change as the loop continues
                     .grid(column=0, row=i, sticky="N W"))
                    i += 1
