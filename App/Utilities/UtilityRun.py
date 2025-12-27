import asyncio
import os
import re
from time import time
from pathlib import Path
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv

HEART_BEAT_INTERVAL = 2


async def heart_beat_async() -> None:
    while True:
        with open(Path(__file__).parent / "UtilityRun.lock", 'w') as lock:
            lock.write(str(time()))
        await asyncio.sleep(HEART_BEAT_INTERVAL)


def is_running() -> bool:
    """
    Checks whether UtilityRun is running.
    """
    if os.path.exists(Path(__file__).parent / "UtilityRun.lock"):
        with open(Path(__file__).parent / "UtilityRun.lock", 'r') as lock:
            lock_value = lock.read()
            if time() - float(lock_value) >= HEART_BEAT_INTERVAL * 2:
                return False
            else:
                return True
    else:
        return False


class ScriptsRunner:
    processes = {}
    logger = LoggerSrv.get_logger("ScriptsRunner")

    def get_all_scripts(self, ignore_config: bool = False):
        self.logger.debug("Getting all scripts")
        scripts = []
        config = ConfigREST.get("*")
        # Matches config keys like "Utilities.[utility_name].Enabled" and extracts the utility name.
        expression = re.compile(r"^Utilities\.(?P<UtilityName>.*)\.Enabled$")
        enabled_utilities = []
        for option in config:
            match = re.fullmatch(expression, option)
            if match and config[option] is True:
                enabled_utilities.append(match.group('UtilityName'))
        for item in os.listdir(Path(__file__).parent):
            if ignore_config or item in enabled_utilities:
                scripts.append(item)
        if len(scripts) == 0:
            self.logger.error("No scripts have been found")
        return scripts

    async def run_all_scripts_async(self) -> None:
        """
        Runs all the Utilities that are currently defined by the config files to be enabled
        Additionally runs a service that updates the status of the script (that it is currently running)
        and waits infinitely.
        """
        if not is_running():
            scripts = self.get_all_scripts()
            self.logger.info("Starting Heartbeat")
            asyncio.create_task(heart_beat_async())
            self.logger.info(f"Running all available scripts ({len(scripts)} found)")
            for item in scripts:
                await self.run_script_async(item)
            for proc in self.processes:
                try:
                    await self.processes[proc].wait()
                except asyncio.CancelledError:
                    self.logger.error("Program got Interrupted by user")
        else:
            self.logger.warning("Tried to run all scripts but they were already running")

    async def run_script_async(self, item: str):
        if item not in self.processes:
            self.logger.info(f"Running Script {item}")
            proc = await asyncio.create_subprocess_exec(
                # creationflags=0x08000000 hides the console windows
                "python", Path(__file__).parent / f"{item}/{item}.pyw",
                creationflags=0x08000000)
            self.processes[item] = proc
        else:
            self.logger.warning(f"Tried to run script {item} but it was already running")

    def stop_all_scripts(self) -> None:
        self.logger.info("Stopping all scripts")
        for item in self.processes:
            self.stop_script(item)

    def stop_script(self, item: str):
        self.logger.info(f"Stopping Script {item}")
        proc = self.processes[item]
        if proc.returncode:
            proc.kill()
        del self.processes[item]


if __name__ == "__main__":
    main = ScriptsRunner()
    asyncio.run(main.run_all_scripts_async())
