# This script find the proper ion to pull
# 2023/2/15
# exchange one CAM molecule to SF

import MDAnalysis as mda


fileName = 'npt_ori.gro'
u = mda.Universe(fileName)

# config
target_x = 65.1  # A
target_y = 65.1
target_z = 72 # A
water_O_name = "OH2"


# select ion
D0 = u.select_atoms("name D0")
sel_D0 = D0[1]
sel_CAM = sel_D0.residue.atoms
index = sel_D0.index+1  # start from 1
print("Index of ion is {:d}".format(index))

# select water molecule
wat = u.select_atoms("name "+water_O_name+" and prop z < "+str(target_z+2)+" and prop z > "+str(target_z-2)+" and prop x<"+str(target_x+3)+" and prop x>"+str(target_x-3)+
              " and prop y<"+str(target_y+3)+" and prop y>"+str(target_y-3))
sel_wat = wat[0].residue.atoms
print("selected water O at (unit:A): ",sel_wat.positions[0,:])

# exchange the position of ion and one water molecules
dev = sel_D0.position - sel_wat.positions[0,:]
# change position of ion
sel_CAM.positions -= dev
# change position of water molecule
sel_wat.positions += dev

# output gro file
u.atoms.write(fileName.replace("_ori.gro","_exchange1_ori.gro"))
