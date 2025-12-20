# Python-Utilities

A python repository to store and manage python utilities for Windows QoL, think of it as PowerToys.

**This project is a work in progress**

## Features

- ClipboardRegex
  - Runs regular expressions on the text in your clipboard and copies the output back into it.
- InstaPicPaste
  - Converts the images in your clipboard into a file, in order to quickly save the image, anywhere.

## Requirements

- Python 3.x
- global_hotkeys
- pillow
- pywin32

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CookieMasterT/Python-Utilities.git
    cd Python-Utilities
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Enable autostart:
   - Add a shortcut to `App\Utilities\UtilityRun.pyw` in Windows startup folder
   - The windows startup folder is usually located at:
     - `C:\Users\%USER%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
     - Or to quickly navigate use run (Windows + R) → `shell:startup`
   - Afterward run `UtilityRun.pyw` or Reboot the system.

## Project Structure

```
App/
├───InternalScripts
│   ├───ConfigManagement/
│   └───Logging/
├───UserInterface/
└───Utilities/
```

## License

MIT License - See LICENSE file for details
