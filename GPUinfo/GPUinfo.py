"""
GPUinfo
Callable functions to get GPU names, manufacturers, and compatible codecs
David Gingerich
Version 1.0.0
"""

from GPUinfo.gpuinfo_handler import *

def names() -> list[str]:
  output = get_gpu_names()
  
  cleaned_list = clean_data(output.splitlines())
  gpu_fullnames = [item.split(": ")[1] for item in cleaned_list]

  return gpu_fullnames

def manufacturers() -> list[str]:
 
  gpu_fullnames = names()
  gpu_splitnames = [item.split() for item in gpu_fullnames]
  
  vendor_names = [item[0] for item in gpu_splitnames]
  return vendor_names