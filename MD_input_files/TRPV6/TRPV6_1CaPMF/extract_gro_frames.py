# extract gro frame from trajectory
# 2022/12/8
import MDAnalysis as mda
import argparse

# config file: "selected_frames.txt"
# output directory: ./confs
parser = argparse.ArgumentParser()
parser.add_argument('-s', dest='topologyFile', help='Input topology file: .tpr, .gro', required=True)
parser.add_argument('-f', dest='trajectoryFile', help='Input trajectory file: .xtc', required=True)
# parser.add_argument('-t', dest='frame', help='Selected frame (start from 0)', required=True)
# parser.add_argument('-o', dest='outputFileName', help='Output file name', required=True)

args = parser.parse_args()

# create Universe
topFile = args.topologyFile
trajFile = args.trajectoryFile
# get frame list
frameList = []
with open("selected_frames.txt", "r") as f:
    lines = f.readlines()
for line in lines:
    frameList.append(int(line.replace("\n", "")))
u = mda.Universe(topFile, trajFile)

# select the frames and output
for t in frameList:
    u.trajectory[t]
    ag = u.atoms
    ag.write("./confs/conf"+str(t)+".gro")
