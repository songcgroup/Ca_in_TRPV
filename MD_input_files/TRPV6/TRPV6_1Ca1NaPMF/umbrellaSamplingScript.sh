# read frames, create directories, and do umbrella sampling in each directory
file="selected_frames.txt"
ind=0
gpu_id=1
bash umbrellaSampling.sh $file $ind $gpu_id


# analysis
mkdir analysis
cp conf*/umbrella*.tpr conf*/umbrella*pullf.xvg analysis/
cd analysis
num=`ls umbrella*.tpr|wc --lines`
python ../summaryFileNames.py -n ${num}
gmx wham -it tpr-files.dat -if pullf-files.dat -o -hist -unit kJ -temp 310.15 -tol 1e-3
cd ..

# extract more frames
python select_configurations_more.py
python extract_gro_frames_more.py -s pull.tpr -f pull.xtc

# read frames, create directories, and do umbrella sampling in each directory
file="selected_frames_more.txt"
ind=$num
bash umbrellaSampling.sh $file $ind  $gpu_id


# analysis
cp conf*/umbrella*.tpr conf*/umbrella*pullf.xvg analysis/
cd analysis
num=`ls umbrella*.tpr|wc --lines`
python ../summaryFileNames.py -n ${num}
gmx wham -it tpr-files.dat -if pullf-files.dat -o -hist -unit kJ -temp 310.15
cd ..
