import pymysql, chardet, os, re
import threading
import time

Mfile=[[] for col in range(2)]
current=0

db = pymysql.connect("localhost","root","88329900","Bilingual" , charset="UTF8")
cursor = db.cursor()

tempdir=''
n=0
Mfile=[[] for col in range(2)]
for root, dirs, files in os.walk('D:\\cp_data\\io'):
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
            
total=len(Mfile[0])

class Thread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print('start1')
    def run(self):
        for index in range(len(Mfile[0])):
            cpath=Mfile[0][index]
            ppath=Mfile[1][index]
            threadLock.acquire()
            global current
            current=index
            threadLock.release()
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
            try:
                cursor.execute("insert into raw2(Chinese,Portuguese) values(%s,%s)", [s1, s2])
                db.commit()
            except Exception as e:
                print (Exception,":",e)
            chfile.close()
            pofile.close()
            

        
class Thread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print('start2')
    def run(self):
        while 1:
            threadLock.acquire()
            global current
            index=current
            threadLock.release()
            #print(index)
            
            if  index==total:
                break
            else:
                per=index/total
 
                print('%.4f'%per, index)
                time.sleep(2)
                
threadLock = threading.Lock()
thread1=Thread1()
thread2=Thread2()

thread1.start()
thread2.start()
thread1.join()
thread2.join()



db.close()
