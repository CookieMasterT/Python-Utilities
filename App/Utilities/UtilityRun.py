import asyncio
import os
import re
from App.internal_scripts import ConfigREST

processes = {}


def get_all_scripts(ignore_config=False):
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


async def run_all_scripts_async():
    for item in get_all_scripts():
        await run_script_async(item)


async def run_script_async(item: str):
    proc = await asyncio.create_subprocess_exec("python", f"./{item}/{item}.pyw")
    processes[item] = proc
    await proc.wait()


def stop_all_scripts():
    for item in processes:
        stop_script(item)


def stop_script(item: str):
    proc = processes[item]
    if proc.returncode:
        proc.terminate()


if __name__ == "__main__":
    asyncio.run(run_all_scripts_async())
