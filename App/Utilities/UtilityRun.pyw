import asyncio
import os
import re
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv


class ScriptsRunner:
    processes = {}
    logger = LoggerSrv.LoggerManager().get_logger("ScriptsRunner")

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
        for item in os.listdir():
            if ignore_config or item in enabled_utilities:
                scripts.append(item)
        if len(scripts) == 0:
            self.logger.error("No scripts have been found")
        return scripts

    async def run_all_scripts_async(self) -> None:
        scripts = self.get_all_scripts()
        self.logger.info(f"Running all available scripts ({len(scripts)} found)")
        for item in scripts:
            await self.run_script_async(item)
        for proc in self.processes:
            try:
                await self.processes[proc].wait()
            except asyncio.CancelledError:
                self.logger.error("Program got Interrupted by user")

    async def run_script_async(self, item: str):
        if item not in self.processes:
            self.logger.info(f"Running Script {item}")
            proc = await asyncio.create_subprocess_exec("python", f"./{item}/{item}.pyw")
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
