import os
import SAbyPT

Mfile=[[] for col in range(2)]
for root, dirs, files in os.walk('C:\\Users\\Bob\\Desktop\\New folder\\cn'):
    index=0
    for file in files: 
        Mfile[0].append(os.path.join(root, file))
        index+=1

for root, dirs, files in os.walk('C:\\Users\\Bob\\Desktop\\New folder\\pt'):
    index=0
    for file in files: 
        Mfile[1].append(os.path.join(root, file))
        index+=1

for index in range(len(Mfile[0])):

    dirname=os.path.join('C:\\Users\\Bob\\Desktop\\New folder (2)',os.path.basename(os.path.dirname(Mfile[0][index])))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    opath=os.path.join(dirname , os.path.basename(Mfile[0][index]))
    print(opath)
    # print(Mfile[0][index])
    # print(Mfile[1][index])
    if Mfile[0][index][len(Mfile[0][index])-5]==Mfile[1][index][len(Mfile[1][index])-5]: #prevent the incorresponding file
        SAbyPT.bi(Mfile[0][index], Mfile[1][index], opath)
