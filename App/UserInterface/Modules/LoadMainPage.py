from tkinter import ttk
from App.Utilities.UtilityRun import is_running
from App.InternalScripts.Logging import LoggerSrv


class MainPageLoader:
    logger = LoggerSrv.get_logger("MainPageLoader")

    def __init__(self) -> None:
        pass

    def load(self, mainframe) -> None:
        for widget in mainframe.winfo_children():
            widget.destroy()
        (ttk.Label(mainframe,
                   text=f"The utilities are currently{"" if is_running() else ' not'} running")
         .grid(column=0, row=0, sticky="W E"))
