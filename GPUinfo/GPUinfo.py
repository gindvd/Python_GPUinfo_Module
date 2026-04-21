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

    manufacturers.append(temp[0])

  return manufacturers