import subprocess
from pathlib import Path
from tkinter import ttk
import App.Utilities.UtilityRun as UtilityRun
from App.InternalScripts.Logging import LoggerSrv


class MainPageLoader:
    logger = LoggerSrv.get_logger("MainPageLoader")

    def __init__(self) -> None:
        pass

    def run_scripts(self, mainframe) -> None:
        self.logger.info("Starting UtilityRun.py")
        # creation flag 0x00000208 detaches the process, making it persistent
        subprocess.Popen(
            ["python", Path(__file__).parents[2] / "Utilities/UtilityRun.py", "-m"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=0x00000208)
        # Reload the mainpage to update running status, this time displaying that the scripts are running
        self.load(mainframe, True)

    def load(self, mainframe, overwrite=False) -> None:
        scripts_running = UtilityRun.is_running() or overwrite
        for widget in mainframe.winfo_children():
            widget.destroy()
        (ttk.Label(
            mainframe,
            text=f"The utilities are currently{"" if scripts_running else ' not'} running")
         .grid(column=0, row=0, sticky="W E"))

        (ttk.Button(
            mainframe,
            text="Start the utilities",
            state="disabled" if scripts_running else "normal",
            command=lambda: self.run_scripts(mainframe))
         .grid(column=0, row=1, sticky="W"))

        (ttk.Button(mainframe,
                    text="Open AutoStart folder",
                    command=lambda: subprocess.run(["explorer.exe", "shell:startup"]))
         .grid(column=0, row=2, sticky="W"))
