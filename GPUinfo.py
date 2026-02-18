import platform
from re import sub
import subprocess

class OSCompatibiltyError(Exception):
  def __init__(self, message, os):
    self.message = message
    self.os = os
  
  def __str__(self) -> str:
    return "{} (Non-Compatible OS: {}) List of compatible OS [Windows, Linux, Mac OS]".format(self.message, self.os)

CMD_DICT = {
  "Linux" : "lspci | grep -iE VGA|3D|video",
  "Darwin" : "system_profiler SPDisplaysDataType",
  "Windows" : {
    "11" : "powershell -Command Get-CimInstance Win32_VideoController | Select-Object name",
    "legacy" : "wmic path win32_VideoController get name"
    }
}

def cmd_getter(device_os: str):
  if device_os not in ["Windows", "Linux", "Darwin"]:
    raise OSCompatibiltyError("Current OS is not compatible with this module.", device_os)
  
  if device_os == "Windows":
    win_ver = platform.release()
  
    if win_ver != "11":
      win_ver = "legacy"
    
    return CMD_DICT.get(device_os, {}).get(win_ver)

  return CMD_DICT.get(device_os)

def parse_cmd(cmd):
  """ 
  Divides command at the | operator and separates them into 2 lists. The two lists
  are then split at every white-space. This makes 2 lists of commands to be run
  """
  cmd_lists = [word.split() for word in cmd.split('|', 1)]
  print(cmd_lists)
  assert len(cmd_lists) <= 2, "cmd_list contains too many lists of commands, Max Num of list: 2"

  GPUname_getter_cmd1 = cmd_lists[0]

  GPUname_getter_cmd2 = None
  if len(cmd_lists) == 2:
    GPUname_getter_cmd2 = cmd_lists[1]

  return GPUname_getter_cmd1, GPUname_getter_cmd2

def init_and_run_cmds():
  device_os = platform.system()

  cmds = cmd_getter(device_os)

  primary_cmd, secondary_cmd = parse_cmd(cmds)
  assert primary_cmd != None, "cmd_getter function incorrectly returning None"

  if secondary_cmd == None:
    return run_single_cmd(primary_cmd)

  return run_multi_cmds(primary_cmd, secondary_cmd)

def run_single_cmd(primary_cmd):
  try:
    # Runs command and returns all connected GPU names as a string
    result = subprocess.Popen(primary_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True)
    return result.stdout
  except FileNotFoundError as err:
    print(err)
  except subprocess.CalledProcessError as err:
    print(err)

def run_multi_cmds( primary_cmd, secondary_cmd):
  try:
    process = subprocess.Popen(primary_cmd, stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, shell=False, text=True)

    result = subprocess.Popen(secondary_cmd, stdin=process.stdout, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              shell=False, text=True)

    process.stdout.close()
    output, _ = result.communicate()
    return output
  except FileNotFoundError as err:
    print(err)
  except subprocess.CalledProcessError as err:
    print(err)

if __name__ == "__main__":
  gpus = init_and_run_cmds()

  print(gpus)