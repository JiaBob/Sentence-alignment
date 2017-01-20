import os
import sentenceAlign

tempdir=''
n=0
Mfile=[[] for col in range(2)]
for root, dirs, files in os.walk('C:\\Users\\Bob\\Desktop\\New folder'):
    for dir in dirs: 
        if n==1:
            #print('asd')
            dirpath1=os.path.join(root, tempdir)
            dirpath2=os.path.join(root, dir)
            for r, d, f in os.walk(dirpath1):
                for ff in f:
                    Mfile[0].append(os.path.join(root, tempdir, ff))
            for r, d, f in os.walk(dirpath2):
                for ff in f:
                    Mfile[1].append(os.path.join(root, dir, ff))
            tempdir=''
            n=0
        else:
            tempdir=dir
            n+=1 

for index in range(len(Mfile[0])):
    
    dirname=os.path.join('C:\\Users\\Bob\\Desktop\\New folder (2)',os.path.basename(os.path.dirname(Mfile[0][index])))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    opath=os.path.join(dirname , os.path.basename(Mfile[0][index]))
    print(opath)
    print(Mfile[0][index])
    print(Mfile[1][index])
    if Mfile[0][index][len(Mfile[0][index])-5]==Mfile[1][index][len(Mfile[1][index])-5]: #prevent the incorresponding file
        sentenceAlign.bi(Mfile[0][index], Mfile[1][index], opath)



