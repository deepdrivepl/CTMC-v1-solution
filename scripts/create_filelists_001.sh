find /home/karol/CTMCCVPR20/train -name '*.jpg' > ../filelists/001-all
awk 'NR % 5 != 0' ../filelists/001-all > ../filelists/001-train
awk 'NR % 5 == 0' ../filelists/001-all > ../filelists/001-val
