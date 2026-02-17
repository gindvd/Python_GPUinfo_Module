import platform
import subprocess

CMD_DICT = {
  "Linux" : "lspci | grep -iE 'VGA|3D|video'",
  "Darwin" : "system_profiler SPDisplaysDataType",
  "Windows" : {
    "11" : "powershell -Command Get-CimInstance Win32_VideoController | Select-Object name",
    "legacy" : "wmic path win32_VideoController get name"
    }
}
