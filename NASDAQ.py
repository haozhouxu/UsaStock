# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import requests
import socket

time_out= 10

socket.setdefaulttimeout(time_out)


sleep_download_time = 0

i = 1

addr1 = "US_Name_AMEX"

addr2 = "US_Name_NASDAQ"

addr3 = "US_Name_NYSE"

def download_one(sub_url,keyword,sleep_time,addr):
    time.sleep(sleep_time)
    
    #urllib.urlretrieve(sub_url+keyword,"..\\data\\"+addr+"\\"+keyword+".csv")

    f = requests.get(sub_url+keyword,timeout=30)
    with open(".\\data\\"+addr+"\\"+keyword+".csv","wb") as code:
        code.write(f.content)
    
    #f = urllib2.urlopen(sub_url+keyword)
    #data = f.read()
    #f.close()
    #with open("..\\data\\"+addr+"\\"+keyword+".csv","wb") as code:
    #    code.write(data)
    
    print keyword
    return 'OK'

def Download_auto(downloadlist,keyword,fun,sleep_time,addr):
    while True:
        try: # 外包一层try   
            value = fun(downloadlist,keyword,sleep_time,addr) # 这里的fun是你的下载函数，我当函数指针传进来。  
           # 只有正常执行方能退出。  
            if value == 'OK':
                break
        except : # 如果发生了10054或者IOError或者XXXError  
            if  (sleep_time > 20):
                with open(".\\log\\"+addr+"_log.txt",'a') as f:
                    f.write(keyword+"\n")
                break
            sleep_time += 10 #多睡5秒，重新执行以上的download.因为做了检查点的缘故，上面的程序会从抛出异常的地方继续执行。防止了因为网络连接不稳定带来的程序中断。  
            print('enlarge sleep time:',sleep_time)

down_url = 'http://real-chart.finance.yahoo.com/table.csv?s='

str_xml = ''

print 'begin-2'

with open('.\\resource\\US_Name_NASDAQ.xml') as f:
    str_xml = f.read()

soup = BeautifulSoup(str_xml,["lxml", "xml"])

for company in soup.find_all(u'上市公司'):
    if i != 0:
        if ('/' not in company[u'代码']) and ('-' not in company[u'代码']):
            Download_auto(down_url,company[u'代码'],download_one,sleep_download_time,addr2)
            print i
        i = i + 1

print 'end-2'

with open(".\\log\\"+addr2+"_log.txt",'a') as f:
    f.write('end-2'+"\n")

time.sleep(500)
