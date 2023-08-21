#python z-radius-half-ca.py pr_ions.gro pr_ions.xtc 15 > calcium-zr.dat
#python 2d-histogram-half-ca.py > 2d-histogram-half-ca.dat;
#a=`wc -l calcium-zr.dat|awk '{print $1}'`;awk "{for(i=0;i<NF;i++){printf \" %17.10e\", \$i/$a} printf \"\n\";}" 2d-histogram-half-ca.dat > 2d-histogram-half-ca-normalized.dat;

#!/usr/bin/env python

import re, sys, math
import MDAnalysis
import numpy as np

zdn = 15
zup = 95
NZ = 160
rmin = 0
rmax = 15
NR = 30
rcutoff = rmax

raw = np.loadtxt('calcium-zr.dat')
ca_zr = np.reshape(raw, (-1,2), 'C')

CaDen, zedges, redges = np.histogram2d(ca_zr[:,0], ca_zr[:,1], bins=[NZ, NR], range=[[zdn,zup],[rmin,rmax]])
for iz in range(NZ):
    for ir in range(NR):
        CaDen[iz][ir] /= abs((zedges[iz+1]-zedges[iz])*math.pi*(redges[ir+1]**2 - redges[ir]**2))


for iz in range(NZ-1,-1,-1):
    for ir in range(NR):
        sys.stdout.write(" %17.10e" % (CaDen[iz][ir]))
    sys.stdout.write("\n")
