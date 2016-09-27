import os
import bi

Mfile=[[] for col in range(2)]
for root, dirs, files in os.walk('D:\\cp_data\\news\\cn'):
    index=0
    for file in files: 
        Mfile[0].append(os.path.join(root, file))
        index+=1

for root, dirs, files in os.walk('D:\\cp_data\\news\\pt'):
    index=0
    for file in files: 
        Mfile[1].append(os.path.join(root, file))
        index+=1

for index in range(len(Mfile[0])):
    
    dirname=os.path.join('D:\\cp_data\\bi-io',os.path.basename(os.path.dirname(Mfile[0][index])))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    opath=os.path.join(dirname , os.path.basename(Mfile[0][index]))
    print(opath)
    print(Mfile[0][index])
    print(Mfile[1][index])
    if Mfile[0][index][len(Mfile[0][index])-5]==Mfile[1][index][len(Mfile[1][index])-5]: #prevent the incorresponding file
        bi.bi(Mfile[0][index], Mfile[1][index], opath)
