#! /usr/bin/python3

from pyrow import pyrow
from pyrow.pyrow import PyErg

ergs = list(pyrow.find())

erg = PyErg(ergs[0])

while True:
    print(erg.get_monitor())