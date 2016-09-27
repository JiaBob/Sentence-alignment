import os
import re
diruri='C:\\Users\\hp\\Desktop\\py' 

ch=os.path.join(diruri,'ch')
po=os.path.join(diruri,'po')
chs=''
pos=''
if not (os.path.exists(ch) and os.path.exists(po)):
    print ('ch and po dirctory not both exist')
else:
    os.chdir(diruri)
    if not os.path.exists(os.path.join(diruri,'bi')):
        os.mkdir('bi')
    for root, dir, file in os.walk(ch):
        for name in file :
            chname=os.path.join(ch,name)
            poname=os.path.join(po,name)
            if not os.path.exists(poname):
                print ('no matched file of '+ name)
            else:
                bifile=open(os.path.join(diruri,'bi', name), 'w+', encoding='utf-8')
                chfile=open(chname, 'r+')
                pofile=open(poname, 'r+', encoding='utf-8')
                stringc=chfile.read()
                stringp=pofile.read()
                for char in stringc:
                    chs+=char
                    if re.match('[\x21-\x2f\x3a-\x3e\x5b-\x60\x7b-\x7e\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u201c\u201d\u300a\u300b\u2026\uff08\uff09]', char):
                        bifile.write(chs+'\n')
                        chs=''
                        for word in stringp:
                            pos+=word
                            if re.match('[\x21-\x2f\x3a-\x3e\x5b-\x60\x7b-\x7e\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u201c\u201d\u300a\u300b\u2026\uff08\uff09]', word):
                                bifile.write(pos+'\n')
                                stringp=stringp.replace(pos, '')
                                pos=''
                                break
                   
                
bifile.close()
chfile.close()
pofile.close()
