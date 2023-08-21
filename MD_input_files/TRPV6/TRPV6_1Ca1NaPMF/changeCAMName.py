# This script intends to change the name of ion in .gro and .top files
# 2023/1/17
# input: index of ion, original gro file
# output: new gro files, output info for .top editing
# example usage: python changeIonName.py -i 116209

# config
groFileNames = ["npt_exchange.gro", "step5_input_cam.gro"]
topFileNames = ["topol.top"]

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='index', help='Atom index of ion (start from 1)', required=True)
args = parser.parse_args()

# 1. change the name of ion in gro file for given index
index = int(args.index)
# open gro file
for fileName in groFileNames:
    oriFileName = fileName.replace(".gro", "_ori.gro")
    with open(oriFileName, "r") as f:
        lines = f.readlines()
    # record the position of CAM
    ion_line_list = []
    for i in range(len(lines)):
        line = lines[i]
        if line.find("CAM     D0") != -1:
            ion_line_list.append(i)
    # change name of ion
    line_id = index+1
    numBefore = int((line_id - min(ion_line_list))/7)
    numAfter = int((max(ion_line_list) - line_id)/7)
    print("There are {:d} CAM before replaced ion, {:d} CAM after replaced ion".format(numBefore,numAfter))
    for i in range(7):
        lines[line_id+i] = lines[line_id+i].replace("CAM ", "CAMR")
    # write file
    with open(fileName, "w") as f:
        f.writelines(lines)
        print("File "+fileName+" replacement finished!")
# 2. change the topology file accordingly
