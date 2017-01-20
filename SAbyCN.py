import re, chardet, os

def countcharacter(string):
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

        if re.match(r'\n', word) and not string=='': #deal with the problem of multi line feed which cause non-parallel problem
            string=string.strip()
            string=string.replace(r'No.', 'xxx') #detect no. symbol
            para.append(string)
            string=''
        else:
            string+=word
            string=string.replace('\n', '')#deal with the problem of multi line feed which cause non-parallel problem
            string=string.replace('\r', '')
    para.append(string)
    return para


def parallel(string1 , string2,l_limit,u_limit):

    result=[[] for col in range(2)]
    chs=''
    pos=''
    chsum=0
    posum=0
    temp=''
    stemp1=string1
    #stemp2=string2
    for char in string1:
        if not re.match('[!.?/:;，：；！？。\u2026]', char):
            chs+=char
        else:
            chsum=countcharacter(chs)
            for word in string2:
               if not re.match('[!.?/:;，：；！？。\u2026]', word):
                    pos+=word
               else:
                    posum=countword(pos)
                    if posum>=chsum/u_limit and posum<=chsum/l_limit:
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
                    elif posum<chsum/u_limit:
                        #print("asd")
                        pos+=word
                        #print(chs)
                        #print(pos)
                        #print(word)
                    elif posum>=chsum/l_limit:
                        #print("dsa")
                        #print(chs, chsum)
                        #print(pos, posum)
                        #print(string2)
                        string2=string2.replace(pos, '')
                        temp=pos
                        chs+=char
                        break
    #if not re.search('[!.?/:;，：；！？。\u2026]$', stemp1):
    #   stemp1+='zzz' #detect phrases
    result[0].append(stemp1)
    result[1].append(string2)
    return result
    #bifile.close()
    
def postprocess(result, bifile):
    res = [[] for col in range(2)]
    chtemp=''
    potemp=''
    for sent in range(len(result[0])):
        # if result[0][sent]=='yyy':#placeholder for each paragraph
        #     bifile.write('\n')
        # else:
        chtemp+=result[0][sent]
        potemp+=result[1][sent]

        if re.search('[。？！]$|zzz', result[0][sent]):
            if not chtemp:
                potemp=potemp.replace('xxx','No.' )

                #res[1][len(res[1]) - 1] += potemp

                bifile.write(potemp)
                potemp=''
            elif not potemp:
                #res[0][len(res[0])-1]+=chtemp

                bifile.write(chtemp)
                chtemp=''
            else:
                #res[0].append(chtemp)

                bifile.write(chtemp+'\n')
                potemp=potemp.replace('xxx','No.')

                #res[1].append(potemp)
                bifile.write(potemp+'\n')
                chtemp=''
                potemp=''
    #return res


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

    chparas=dividePara(s1)
    poparas = dividePara(s2)

    #chparas=re.split('\r\n|\n',s1)
    #poparas=re.split('\r\n|\n',s2)
    
    #check paragraph (whether align or not)
    errorPara=0
    for index in range(len(chparas)):
        if len(chparas)==len(poparas):
            if countcharacter(chparas[index])>=3*countword(poparas[index]):
                errorPara+=1
        else:
            opath=opath.replace('.txt', 'x.txt')
            break
    if errorPara>len(chparas)/5:
        opath=opath.replace('.txt', 'x.txt')
    
    bifile=open(opath,'w+', encoding='utf-8')

    result = [[] for col in range(2)]
    for index in range(len(chparas)):
        chpara=chparas[index]
        if index<len(poparas): #deal with the problem of non-parallel corpus
            popara=poparas[index]
        else:
            popara=''
        temp=parallel(chpara,popara,1,3)
        result[0]+=temp[0]
        #result[0].append('yyy')#place holder for each paragraph
        result[1]+=temp[1]
        #result[1].append('yyy')

    for i in range(len(result[0])):

        print(result[0][i])
        print(result[1][i])
    postprocess(result, bifile)

    chfile.close()
    pofile.close()
    bifile.close()

if __name__=="__main__":
    bi('test\\chspeech.txt','test\\pospeech.txt', 'result\\cn_result.txt' )
