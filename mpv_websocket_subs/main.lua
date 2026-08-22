local utils = require 'mp.utils'

local script_path = utils.join_path(mp.get_script_directory(), "WS_subs.py")
local running = false
local old_ipc_server = mp.get_property_native("input-ipc-server")
local new_ipc_server = "/tmp/mpvsocket"
local python_cmd
local custom_python_cmd
local default_venv_bin
local bin_path
local runScript

if package.config:sub(1,1) == '/' then
  python_cmd = "python3"
  bin_path = utils.join_path(mp.get_script_directory(), "bin/WS_subs.bin")
  default_venv_bin = mp.command_native({"expand-path", "~~/.mpv_venv/bin/python"})
else
  python_cmd = "py"
  bin_path = utils.join_path(mp.get_script_directory(), "bin/WS_subs.exe")
  default_venv_bin = mp.command_native({"expand-path", "~~/.mpv_venv/Scripts/python.exe"})
end

if utils.file_info(bin_path) == nil then
  bin_path = nil
end

if utils.file_info(default_venv_bin) ~= nil then
  python_cmd = default_venv_bin
end

if custom_python_cmd then
  python_cmd = custom_python_cmd
end

local function startScript(secondary)
  if running then
      mp.abort_async_command(runScript)
  else
    running = true
    old_ipc_server = mp.get_property_native("input-ipc-server")

    if old_ipc_server == "" then
      mp.set_property("input-ipc-server", new_ipc_server)
    end

    local arguments

    if bin_path then
      arguments = {
        bin_path,
      }
    else
      arguments = {
        python_cmd,
        script_path,
      }
    end

    table.insert(arguments, mp.get_property_native("input-ipc-server"))

    if secondary then
      table.insert(arguments, "secondary")
    end

    mp.osd_message("Loading WS_subs script...", 2)

    runScript = mp.command_native_async({
        name = "subprocess",
        playback_only = false,
        args = arguments,
      },
      function(res, val, err)
          mp.osd_message("WS_subs script has stopped", 2)
          -- mp.set_property("input-ipc-server", old_ipc_server)
          running = false
      end
    )
  end
end

mp.add_key_binding("CTRL+ALT+w", "startWS_subs", function ()
  startScript(false)
end)

mp.add_key_binding("CTRL+ALT+e", "startWS_secondary_subs", function ()
  startScript(true)
end)
