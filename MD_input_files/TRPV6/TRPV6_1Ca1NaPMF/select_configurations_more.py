# get selected conformations
from gromacs.fileformats.xvg import XVG
import numpy as np
# read xvg file
a = XVG('./analysis/histo.xvg')
data = a.array
zArray = a.array[0,:] # unit: ps
countData = a.array[1:,:]

countDataSum = countData.sum(axis = 0)
indices = np.where(countDataSum<500)[0]
zVals = zArray[indices]

a = XVG('pull_pullx.xvg')
tData = a.array[0,:] # unit: ps
devData = a.array[1,:]
# subsampling
subIndex = np.arange(0,len(tData),1)
tData = tData[subIndex]
devData = devData[subIndex]

confIndList = []
for zVal in zVals:
    index = abs(devData-zVal).argmin()
    confIndList.append(index)

confIndList = np.array(confIndList)
# output indices
confIndList
lines = []
for i in range(len(confIndList)):
    lines.append(str(confIndList[i])+"\n")


# write output file
with open("selected_frames_more.txt","w") as f:
    f.writelines(lines)
