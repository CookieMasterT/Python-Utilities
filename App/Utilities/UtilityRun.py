import asyncio
import os
import re
from App.InternalScripts.ConfigManagement import ConfigREST
from App.InternalScripts.Logging import LoggerSrv


class ScriptsRunner:
    processes = {}
    logger = LoggerSrv.LoggerManager().get_logger("ScriptsRunner")

    def get_all_scripts(self, ignore_config=False):
        self.logger.debug("Getting all scripts")
        scripts = []
        if ignore_config:
            for item in os.listdir():
                scripts.append(item)
        else:
            config = ConfigREST.get("*")
            expression = re.compile(r"^Utilities\.(?P<UtilityName>.*)\.Enabled$")
            enabled_utilities = []
            for option in config:
                match = re.fullmatch(expression, option)
                if match and config[option] is True:
                    enabled_utilities.append(match.group('UtilityName'))
            for item in os.listdir():
                if ignore_config or item in enabled_utilities:
                    scripts.append(item)
        return scripts

    async def run_all_scripts_async(self):
        self.logger.info("Running all available scripts")
        for item in self.get_all_scripts():
            await self.run_script_async(item)

    async def run_script_async(self, item: str):
        if item not in self.processes:
            self.logger.info(f"Running Script {item}")
            proc = await asyncio.create_subprocess_exec("python", f"./{item}/{item}.pyw")
            self.processes[item] = proc
            await proc.wait()
        else:
            self.logger.warning(f"Tried to run script {item} but it was already running")

    def stop_all_scripts(self):
        self.logger.info("Stopping all scripts")
        for item in self.processes:
            self.stop_script(item)

    def stop_script(self, item: str):
        self.logger.info(f"Stopping Script {item}")
        proc = self.processes[item]
        if proc.returncode:
            proc.terminate()
        del self.processes[item]


if __name__ == "__main__":
    main = ScriptsRunner()
    asyncio.run(main.run_all_scripts_async())
