# umbrella sampling shell script
# do in michael
file=$1  # file name
ind=$2   # input trial index
gpu_id=$3  # gpu_id

while read i;
do
        mkdir conf${i}
        cp confs/conf${i}.gro  conf${i}
        cd conf${i}
        # NPT
        gmx grompp -f ../npt_umbrella.mdp -c conf${i}.gro -p ../topol.top -r ../step5_input_cam.gro -n ../index_pull1.ndx -o npt${ind}.tpr --maxwarn 3
        gmx mdrun -v -deffnm npt${ind} -nt 32 -gpu_id $gpu_id
        # umbrella sampling
        gmx grompp -f ../md_umbrella.mdp -c npt${ind}.gro -t npt${ind}.cpt -p ../topol.top -r ../step5_input_cam.gro -n ../index_pull1.ndx -o umbrella${ind}.tpr -maxwarn 2
        gmx mdrun -v -deffnm umbrella${ind} -nt 32 -gpu_id $gpu_id
        cd ..
        ind=$((ind+1))
done < $file


