import re, chardet, os

def countlatter(string):
    sum=0
    num=0
    pattern=r'[\s\x00-\x2f\x3a-\x3e\x5b-\x60\x7b-\x7e\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u201c\u201d\u300a\u300b\u2026\uff08\uff09]'
    string=re.sub(pattern, '',string)
    for word in string:
        if num!=1:
            sum+=1
            num=0
        if re.match(r'\d', word):
            num=1
        else:
            num=0
    return sum


    
def countword(string):
    sum=0
    pattern=r'[\x21-\x2f\x3a-\x3e\x5b-\x60\x7b-\x7e\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u201c\u201d\u300a\u300b\u2026\uff08\uff09]'
    string=re.sub(pattern, ' ',string)
    string=re.sub(r'\x20+', ' ', string)
    #print(string)
    for word in string:
        if word==' ' or word=='\n':
            sum+=1
    return sum


def dividePara(p):
    para=[]
    string=''
    for word in p:

        if re.match(r'\n', word) and not string=='': #deal with the problem of multi line feed which cause non-parallal problem
            string=string.strip()
            string=string.replace(r'.ยบ', 'xxx') #detect no. symbol
            para.append(string)
            string=''
        else:
            string+=word
            string=string.replace('\n', '')#deal with the problem of multi line feed which cause non-parallal problem
            string=string.replace('\r', '')
    para.append(string)
    return para


def parallal(string1 , string2):    
    #bifile=open('C:\\Users\\hp\\Desktop\\py\\bi.txt','w+', encoding='utf-8')
    result=[[] for col in range(2)]
    chs=''
    pos=''
    chsum=0
    posum=0
    temp=''
    stemp1=string1
    #stemp2=string2
    for char in string1:
        if not re.match('[\x21\x2e\x3f\x2c\x3a\x3b\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u2026]', char):
            chs+=char
        else:
            chsum=countlatter(chs)
            for word in string2:
               if not re.match('[\x21\x2e\x3f\x2c\x3a\x3b\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u2026]', word):
                    pos+=word
               else:
                    posum=countword(pos)
                    if posum>=chsum/3.5 and posum<=chsum:
                        result[0].append(chs+char)
                        stemp1=stemp1.replace(chs+char, '')
                        result[1].append(pos+word)
                        #bifile.write(chs+char+'\n')
                        #print('sda')   
                        #bifile.write(pos+word+'\n')
                        #print(chs)
                        #print(pos)
                        #print(string2)
                        pos=pos.replace(temp, '')
                        string2=string2.replace(pos, '', 1)
                        string2=string2.replace(word, '', 1)
                        posum=chsum=0
                        chs=pos=''
                        break
                    elif posum<chsum/3.5:
                        #print("asd")
                        pos+=word
                        #print(chs)
                        #print(pos)
                        #print(word)
                    elif posum>chsum:
                        #print("dsa")
                        #print(chs, chsum)
                        #print(pos, posum)
                        #print(string2)
                        string2=string2.replace(pos, '')
                        temp=pos
                        chs+=char
                        break
    if not re.search('[\x21\x2e\x3f\x2c\x3a\x3b\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u2026]$', stemp1):
        stemp1+='zzz' #detect phrases
    result[0].append(stemp1)
    result[1].append(string2)
    return result
    #bifile.close()
    
def postprocess(result, bifile):
    chtemp=''
    potemp=''
    for sent in range(len(result[0])):
        chtemp+=result[0][sent]
        potemp+=result[1][sent]
        if re.search('[\u3002\uff1f\uff01]$|zzz', result[0][sent]):
            if not chtemp or chtemp=='zzz': #deal with blank line parallal to Portuguese
                potemp=potemp.replace('xxx','.ยบ' )
                bifile.write(potemp)
                potemp=''
            elif not potemp:
                chtemp=chtemp.replace('zzz', '') #deal with blank line parallal to Chinese
                bifile.write(chtemp)
                chtemp=''
            else:
                chtemp=chtemp.replace('zzz', '')
                bifile.write('\n'+chtemp)
                potemp=potemp.replace('xxx','.ยบ' )
                bifile.write('\n'+potemp) 
                chtemp=''
                potemp=''
        
def bi(cpath, ppath, opath):
    chfile=open(cpath,'rb+')
    s1=chfile.read()
    coding=chardet.detect(s1)['encoding']
    if coding:
        s1=s1.decode(coding)
    else:
        s1=''
        
    pofile=open(ppath,'rb+')
    s2=pofile.read()
    coding=chardet.detect(s2)['encoding']
    if coding:
        s2=s2.decode(coding)
    else:
        s2=''

    result=[[] for col in range(2)]

    chparas=dividePara(s1)
    poparas=dividePara(s2)
    
    #check paragraph (whether align or not)
    errorPara=0
    print(chparas)
    print(poparas)
    for index in range(len(chparas)):
        if len(chparas)==len(poparas):
            if countlatter(chparas[index])>=3*countword(poparas[index]):
                errorPara+=1
        else:
            opath=opath.replace('.txt', 'x.txt')
            break
    if errorPara>len(chparas)/5:
        opath=opath.replace('.txt', 'x.txt')
    
    bifile=open(opath,'w+', encoding='utf-8')
    #print(chparas)
    #print(poparas)

    for index in range(len(chparas)):
        chpara=chparas[index]
        if index<len(poparas): #deal with the problem of non-parallal corpus
            popara=poparas[index]
        else:
            popara=''
        temp=parallal(chpara,popara)
        
        result[0]+=temp[0]
        result[1]+=temp[1]
    #print(result)
    postprocess(result, bifile)

    chfile.close()
    pofile.close()
    bifile.close()

bi('D:\\cp_data\\news\\cn\\2016\\2016-09-02\\2.txt','D:\\cp_data\\news\\pt\\2016\\2016-09-02\\2.txt', 'C:\\Users\\hp\\Desktop\\py\\error.txt' )
