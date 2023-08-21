#!/usr/bin/python

import re, sys, math
import MDAnalysis
import numpy as np


top = sys.argv[1]
trj = sys.argv[2]
nstart = int(sys.argv[3]) # for parallel run
nend = int(sys.argv[4])
z0 = 20.00
z1 = 80.00
dz = 0.5
rmax = 15

u = MDAnalysis.Universe(top, trj)

sf = u.select_atoms("resid 643 and name O")
xsf = np.average([atom.position[0] for atom in sf])
ysf = np.average([atom.position[1] for atom in sf])

sel_ions = "name D0"
ions = u.select_atoms(sel_ions)
nions = len(ions)
coord_oxygens = [u.select_atoms("name O* and around 3.0 bynum %d" % (i.index+1), updating=True) for i in ions]

N = int((z1 - z0)/dz)
noxygens = {}                   # number of oxygens in each bin, key is resname.resid-name
nbins = [0 for j in range(N)]   # number of calcium ions in each bin
ntotoxy = [0 for j in range(N)] # number of total oxygen atoms in each bin

nframes = len(u.trajectory)
for ts in u.trajectory:
    # [nstart, nend)
    if ts.frame < nstart:
        continue
    if ts.frame >= nend:
        break
    if ts.frame % 100 == 0:
        sys.stderr.write("%6d/%6d: %.1f%%\n" % (ts.frame, nframes, ts.frame*100./nframes))
    for i in range(nions):
        x = ions[i].position[0] - xsf
        y = ions[i].position[1] - ysf
        z = ions[i].position[2]
        if z >= z0 and z < z1:
            if x*x + y*y < rmax*rmax:
                if not 'POPC' in coord_oxygens[i].resnames:
                    nz = int((z - z0)/dz)
                    for o in coord_oxygens[i]:
                        if o.resname == "TIP3":
                            atom = "%s-%s"%(o.resname, o.name)
                        else:
                            atom = "%s%d-%s"%(o.resname, o.resid, o.name.rstrip('1234567890'))
                        if not atom in noxygens:
                            noxygens[atom] = [0 for j in range(N)]
                        noxygens[atom][nz] += 1
                    ntotoxy[nz] += coord_oxygens[i].n_atoms
                    nbins[nz] += 1

#print "#z n-ca n-tot-oxy n-avg-oxy",
#for o in noxygens:
#    print o,
#print
#
#for i in range(N):
#    z = z0 + dz*(i+0.5)
#    print z, nbins[i], ntotoxy[i], float(ntotoxy[i])/max(1,nbins[i]),
#    for o in noxygens:
#        print float(noxygens[o][i])/max(1,nbins[i]),
#    print

print "z n-ca n-tot-oxy",
for o in noxygens:
    print o,
print

for i in range(N):
    z = z0 + dz*(i+0.5)
    print z, nbins[i], ntotoxy[i],
    for o in noxygens:
        print noxygens[o][i],
    print
