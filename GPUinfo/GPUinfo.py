"""
GPUinfo
Callable functions to get GPU names, manufacturers, and compatible codecs
David Gingerich
Version 1.0.0
"""

from GPUinfo.handler import *

def manufacturers() -> list[str]:
  """
  Possible returns options:
  NVIDIA - for NVIDIA GPUS
  AMD - for AMD for dedicated and integrated GPUs
  Intel - for Intel for dedicated and integrated GPUs
  Apple - for Macbook GPUs
  Adapter - possible returns on Virtual Machines and Container hosted OS
  """

  string_of_connected_gpus: str = get_gpu_names()
  
  list_of_connected_gpus: list[str] = string_of_connected_gpus.splitlines()

  device_manufacturers = []
  for connected_gpu in list_of_connected_gpus:
    temp = []
    connected_gpu = remove_symbols(item)
    temp = connected_gpu.split()

    if temp == []:
      continue
    
    name = temp[0]

    # Linux devices may use Advanced Micro Devices, Inc instead on AMD
    if name == "Advanced":
      name = "AMD"

    # possible options for OS run on virtual machines, and containers
    elif name in ["Microsoft", "VMware", "VirtualBox"]:
      name = "Adapter"

    device_manufacturers.append(name)

  return device_manufacturers