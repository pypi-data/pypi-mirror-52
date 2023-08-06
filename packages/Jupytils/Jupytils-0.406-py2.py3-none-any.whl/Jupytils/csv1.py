#!/usr/local/bin/python
import sys
import datetime
import getopt
import os
import pandas as pd
import numpy as np
import collections
from collections import defaultdict

opts, args = 0,0
try:
    opts, args = getopt.getopt(sys.argv[1:], "abcdefghijklmnopqrstuvwxyz")
except getopt.GetoptError as e:
    print("Invalid option: ", e )

print (opts, "ARGS: " , args)