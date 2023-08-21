# This file output the file names for umbrella sampling
# input: number of files
# output: .dat files
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='num', help='Total number of files', required=True)
args = parser.parse_args()
num = int(args.num)

# output data file
lines = []
for i in range(num):
    lines.append("umbrella" + str(i) + "_pullf.xvg\n")
with open("pullf-files.dat", "w") as f:
    f.writelines(lines)

# output data file
lines = []
for i in range(num):
    lines.append("umbrella" + str(i) + ".tpr\n")
with open("tpr-files.dat", "w") as f:
    f.writelines(lines)
