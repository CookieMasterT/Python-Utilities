import asyncio
import os
import re


from App.internal_scripts import ConfigREST


async def run_scripts():
    config = ConfigREST.get("*")
    expression = re.compile(r"^Utilities\.(?P<UtilityName>.*)\.Enabled$")
    enabled_utilities = []
    for option in config:
        match = re.fullmatch(expression, option)
        if match and config[option] is True:
            enabled_utilities.append(match.group('UtilityName'))
    processes = []
    for item in os.listdir():
        if item in enabled_utilities:
            processes.append(await asyncio.create_subprocess_exec("python", f"./{item}/{item}.pyw"))
    for proc in processes:
        await proc.wait()  # wait for processes to finish


if __name__ == "__main__":
    asyncio.run(run_scripts())
