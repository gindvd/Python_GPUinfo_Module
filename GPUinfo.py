import platform
import subprocess

class OSCompatibiltyError(Exception):
  def __init__(self, message, os):
    super().__init__(message)
    self.os = os
  
  def __str__(self):
    return "{} (Non-Compatible OS: {}) List of compatible OS [Windows, Linux, Mac OS]".format(self.message, self.os)

CMD_DICT = {
  "Linux" : "lspci | grep -iE 'VGA|3D|video'",
  "Darwin" : "system_profiler SPDisplaysDataType",
  "Windows" : {
    "11" : "powershell -Command Get-CimInstance Win32_VideoController | Select-Object name",
    "legacy" : "wmic path win32_VideoController get name"
    }
}

def cmd(device_os):
  if device_os not in ["Windows", "Linux", "Darwin"]:
    raise OSCompatibiltyError("Current OS is not compatible with this module.", device_os)
  
  if device_os == "Windows":
    win_ver = platform.release()
  
    if win_ver != "11":
      win_ver = "legacy"
    
    return CMD_DICT.get(device_os, {}).get(win_ver)

  return CMD_DICT.get(device_os)
