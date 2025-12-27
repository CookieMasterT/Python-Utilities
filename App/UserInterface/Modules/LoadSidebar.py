import os
from pathlib import Path
from tkinter import ttk
from App.UserInterface.Modules.LoadUtilitySettings import UtilitySettingsLoader
from App.UserInterface.Modules.LoadMainPage import MainPageLoader


class SidebarLoader:
    def __init__(self) -> None:
        self.USLoader = UtilitySettingsLoader()
        self.MPLoader = MainPageLoader()

    def load(self, mainframe, options) -> None:
        (ttk.Button(options, text="Main",
                    command=lambda: self.MPLoader.load(mainframe))
         .grid(column=0, row=0, sticky="N W E"))
        row = 1
        with os.scandir(Path(__file__).parents[2] / "Utilities") as files:
            for item in files:
                if item.is_dir() and item.name != "__pycache__":
                    (ttk.Button(
                        options,
                        text=f"{item.name}",
                        command=lambda _=item.name: self.USLoader.load(_, mainframe))
                     # the above lambda is done so that the value is passed and it doesn't change as the loop continues
                     .grid(column=0, row=row, sticky="N W E"))
                    row += 1
