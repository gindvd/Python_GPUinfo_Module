"""
GPUinfo
Callable functions to get GPU names, manufacturers, and compatible codecs
David Gingerich
Version 1.0.0
"""

from GPUinfo.handler import *

def get_manufacturers():
  device_info = get_gpu_names()
  
  items = device_info.splitlines()

  manufacturers = []
  for item in items:
    temp = []
    item = remove_symbols(item)
    temp = item.split()

    if temp == []:
      continue
    
    name = temp[0]

    # Linux devices may use Advanced Micro Devices, Inc instead on AMD
    if name == "Advanced":
      name = "AMD"

    # possible options for OS run on virtual machines, and containers
    if name in ["Microsoft", "VMware", "VirtualBox"]:
      name = "Adapter"

    manufacturers.append(name)

  return manufacturers