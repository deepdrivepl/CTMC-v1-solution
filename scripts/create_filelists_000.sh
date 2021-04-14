find /home/karol/projects/cufix/CTMCCVPR20/train -name '*.jpg' > ../filelists/000-all
awk 'NR % 5 != 0' ../filelists/000-all > ../filelists/000-train
awk 'NR % 5 == 0' ../filelists/000-all > ../filelists/000-val
