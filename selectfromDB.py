import pymysql,threading,time
import SA

db = pymysql.connect("localhost","root","","Bilingual" , charset="UTF8")
cursor = db.cursor()

current=0
cursor.execute('Select num,Chinese,Portuguese From raw2')
db.commit()
result=cursor.fetchall()
total=len(result)
class Thread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print('start1')
    def run(self):
        for index in range(len(result)):

            threadLock.acquire()
            global current
            current = index
            threadLock.release()

            num=result[index][0]
            ch=result[index][1]
            po=result[index][2]
            #print(num)
            #print(ch)
            #print(po)
            string=SA.bi(ch,po)
            cursor.execute("update raw2 set bilingual=%s where num=%s",[string,num])
            db.commit()



class Thread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print('start2')

    def run(self):
        while 1:
            threadLock.acquire()
            global current
            index = current
            threadLock.release()
            # print(index)

            if index == total-1:
                break
            else:
                per = index / total

                print('%.4f' % per, index)
                time.sleep(2)


threadLock = threading.Lock()
thread1 = Thread1()
thread2 = Thread2()

thread1.start()
thread2.start()
thread1.join()
thread2.join()

db.close()