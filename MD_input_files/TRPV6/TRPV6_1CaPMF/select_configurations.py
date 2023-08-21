# get selected conformations
from gromacs.fileformats.xvg import XVG
import numpy as np
# read xvg file

a = XVG('pull_pullx.xvg')
tData = a.array[0,:] # unit: ps
devData = a.array[1,:]
# subsampling
subIndex = np.arange(0,len(tData),1)
tData = tData[subIndex]
devData = devData[subIndex]

# select conformations every 1 A
step = 0.1  # unit: nm
start_val = np.floor(devData.min()/0.1)*0.1+0.3
end_val = np.floor(devData.max()/0.1)*0.1
print('start z = {:.2f} nm, end z = {:.2f} nm, step = {:.2f} nm'.format(start_val,end_val,step))
zVals = np.arange(start_val,end_val,step)
confIndList = []
for zVal in zVals:
    index = abs(devData-zVal).argmin()
    confIndList.append(index)

# check the maximal interval between two points
iter_n = 0
while iter_n<20:
    devDataSel = devData[np.array(confIndList)]
    devDataSel = np.array(list(sorted(set(devDataSel))))  # sort
    intervals = abs(np.diff(devDataSel))
    if intervals.max() < step*1.1:
        break
    ind = np.argmax(intervals)
    thisZVal = devDataSel[ind]
    nextZVal = devDataSel[ind+1]
    newIndex = abs(devData-(thisZVal+nextZVal)/2).argmin()
    confIndList.append(newIndex)
    iter_n += 1
print("{:d} more points added".format(iter_n))
print("maximal interval = {:.3f} nm".format(intervals.max()))

confIndList = np.array(confIndList)
# output indices
confIndList
lines = []
for i in range(len(confIndList)):
    lines.append(str(confIndList[i])+"\n")


# write output file
with open("selected_frames.txt","w") as f:
    f.writelines(lines)
