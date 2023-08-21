# This script intends to change the reference position of ion in .gro file
# 2023/1/17
# input: gro file
# output: new gro file with changed position
# example usage: python changeIonRefPos.py -i 116209

# config
# x,y =5.65,5.58 nm

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='index', help='Atom index of ion (start from 1)', required=True)
args = parser.parse_args()
index = int(args.index)

fileName = "step5_input_cam.gro"
with open(fileName, "r") as f:
    lines = f.readlines()
line_id = index+1

lines[line_id] = lines[line_id][:20] + "   5.650   5.580   0.000\n"
# write file
with open(fileName, "w") as f:
    f.writelines(lines)
    print("Reference position change finished!")
