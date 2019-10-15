import numpy as np
import pandas as pd
from multiprocessing import Pool
import time
from ast import literal_eval
import os
import subprocess
from random import choice

"""
def f(n):

   return subprocess.check_output('python3 ../AG/index.py', shell=True)

pool = Pool(processes=1)
res = pool.apply_async(f,(20,))
try:
    print(res.get(timeout=1))
except:
    print("time error")"""

a = np.array([1,2]).tolist()
b = np.array([1,2]).tolist()
print(a==b)
