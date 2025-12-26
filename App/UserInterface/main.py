from tkinter import *
from tkinter import ttk
from App.InternalScripts.Logging import LoggerSrv
from App.UserInterface.Modules.LoadMainPage import MainPageLoader
from Modules.LoadSidebar import SidebarLoader


class UserInterface:
    logger = LoggerSrv.get_logger("UserInterface")

    def __init__(self) -> None:
        self.logger.info("Starting GUI application")
        root = Tk()
        root.title("Python Utilities")
        root.geometry("1000x500")
        root.resizable(True, True)

        option_list = ttk.Frame(root, padding=(10, 10, 10, 10))
        option_list.grid(column=0, row=0, sticky="N W E S")

        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=1, row=0, sticky="N W E S")

        SidebarLoader().load(mainframe, option_list)
        MainPageLoader().load(mainframe)

        root.mainloop()


if __name__ == "__main__":
    UserInterface()
