# mpv_websocket_subs

mpv script to send subtitles via a websocket server. Useful to send subs to a texthooker like [texthooker-ui]() or the one included in my other project [Jiku]().

### Demo



## Installation

Locate your mpv config folder. It is typically found at `~/.config/mpv/` on Linux/MacOS and `C:\users\USERNAME\AppData\Roaming\mpv\` on Windows.  [Files section](https://mpv.io/manual/master/#files) in mpv's manual for more info. I will refer to the path of this folder as `<mpv config directory>` for the rest of this file.

To install the mpv script you can either use the precompiled binaries without having to install anything else. Otherwise you can setup a python environent to run the script. Binaries have not been thoroughly tested, open an Issue if you encounter any problem.

### Setup mpv script using compiled binaries

- Download the build version matching your system from the [Release page](https://github.com/TnTora/mpv_websocket_subs/releases) and extract its contents
  
- Place the `mpv_websocket_subs` folder inside the `scripts` folder in `<mpv config directory>`. If it doesn't exist you should create it.

- If you are on macOS you may need to run the following command in Terminal to allow the system to run the sctipt since it is not signed:
  ```
  xattr -dr com.apple.quarantine ~/.config/mpv/scripts/mpv_websocket_subs/bin
  ```
Running the script for the first time might take a while so if nothing seems to happen just wait. Afterwards it should start almost instantly.

### Setup mpv script using python script

- Download the source code from Release section.

- Place the `mpv_websocket_subs` folder inside the `scripts` folder in `<mpv config directory>`. If it doesn't exist you should create it.

If you don't already have python 3.10 or above installed on your machine, install it. On Windows make sure python is added to PATH.

>**Optional:** Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) named `.mpv_venv` in `<mpv config directory>`. While optional, it is highly reccomended to keep the script isolated from the system python.
>
> If you chose a different name for the virtual environment or you want to use a different version of pyhton, open `main.lua` in a text editor and set the `custom_python_cmd` variable to a string containing your preferred command or path to binary.

Install dependencies (substitute `/` with `\` if you are on Windows)

```
cd <mpv config directory>
cd scripts/mpv_websocket_subs
pip install -r requirement.txt
```

## Usage

On mpv, use the keybinding `CTRL+ALT+w` to start the script and then follow the instruction on screen.\
If you want to send secondary subs instead use `CTRL+ALT+e`.

Press the same keybinding to stop the script from running.

To change the keybinding add the following lines to your `input.conf` file after replacing `CTRL+ALT+w` and `CTRL+ALT+e` with whatever you prefer

```
# mpv_websocket_subs
CTRL+ALT+w             script-binding mpv_websocket_subs/startWS_subs
CTRL+ALT+e             script-binding mpv_websocket_subs/startWS_secondary_subs
```

> **NOTE: If you are not using the [standard mpv build](https://mpv.io/installation/), your player might ignore the `input.conf` file (e.g. [mpv.net](https://github.com/mpvnet-player/mpv.net), [IINA](https://iina.io/)) so you might need to use the in-app options to set the keybindings.**

## Dependencies
| Name | LICENSE |
|------|---------|
| [websockets](https://github.com/python-websockets/websockets) | [BSD 3-Clause](https://github.com/python-websockets/websockets/blob/main/LICENSE) |
| [python-mpv-jsonipc](https://github.com/TnTora/python-mpv-jsonipc) (TnTora) <br> forked from [python-mpv-jsonipc](https://github.com/iwalton3/python-mpv-jsonipc) (iwalton3) | [Apache-2.0](https://github.com/TnTora/python-mpv-jsonipc/blob/master/LICENSE.md) |

Binaries are compiled using [Nuitka](https://github.com/Nuitka/Nuitka).
