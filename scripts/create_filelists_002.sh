find /home/karol/CTMCCVPR20/train -name '*.jpg' > ../filelists/002-all
awk 'NR % 5 != 0' ../filelists/002-all > ../filelists/002-train
awk 'NR % 5 == 0' ../filelists/002-all > ../filelists/002-val

find /home/karol/CTMCCVPR20/train-180 -name '*.jpg' >> ../filelists/002-all
awk 'NR % 5 != 0' ../filelists/002-all >> ../filelists/002-train
awk 'NR % 5 == 0' ../filelists/002-all >> ../filelists/002-val

find /home/karol/CTMCCVPR20/train-hf -name '*.jpg' >> ../filelists/002-all
awk 'NR % 5 != 0' ../filelists/002-all >> ../filelists/002-train
awk 'NR % 5 == 0' ../filelists/002-all >> ../filelists/002-val

find /home/karol/CTMCCVPR20/train-vf -name '*.jpg' >> ../filelists/002-all
awk 'NR % 5 != 0' ../filelists/002-all >> ../filelists/002-train
awk 'NR % 5 == 0' ../filelists/002-all >> ../filelists/002-val
