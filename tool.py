import threading
import os
import re
import requests
import json
import time as tm
import datetime
from pathlib import Path
import argparse
import keyboard
import matplotlib.pyplot as plt
import numpy as np
flag = None
listIp=dict()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
months={'Jan': 1,'Feb': 2,'Mar' : 3,'Apr' : 4,'May' : 5,'Jun' : 6,'Jul' : 7,'Aug' : 8,'Sep' : 9,'Oct' : 10,'Nov' : 11,'Dec' : 12}

def checkSpam(ip):
    global listIp
    mark= [1]*listIp[ip]['num']
    for i in range(1,listIp[ip]['num']):
        ti = (listIp[ip]['datetime'][i]-listIp[ip]['datetime'][i-1]).total_seconds()
        if(ti < 2):
            mark[i]=mark[i-1]+1
    return mark[listIp[ip]['num']-1]>4
        
def coverTime(str):
    #13/Jun/2020:10:29:54
    global month
    day= int(re.search('\d{2}\/',str).group()[:2])
    month=months[re.search('\/[a-zA-Z]+\/',str).group()[1:-1]]
    year=int(re.search('\/\d{4}',str).group()[1:])
    h,m,s=re.split('\:',str[-8:])
    time=datetime.datetime(year,month,day,int(h),int(m),int(s))
    return time

def subTime(t1,t2):
    time=t1-t2
    return time.total_seconds()

def charting():
    print('------')

def process2():
    while(True):
        if(keyboard.is_pressed('delete')):
            try:
                print('Nhap thoi gian muon xem tinh toi thoi diem hien tai: ')
                t= float(input())
                T= datetime.datetime.now()
            except:
                print('Thoi gian la phut, nhap so thuc')
            
def process(filelog,fileblacklist):
    global flag
    setIp=set()
    global listIp
    
    blackList = []
    path = Path(filelog)
    path_bl = Path(fileblacklist)
    with open(path_bl, "r") as file:
        listbl = file.readlines()
        for i in listbl:
            blackList.append(re.findall(r'[0-9]+(?:\.[0-9]+){3}', i)[0])
    
    pointer_current=0
    while True:
        file = open(path, "r+")
        file.seek(pointer_current)
        line = file.readline()
        if( not line):
            continue
        else:
            pointer_current=file.tell()
            if(len(line)>1):
                s = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line[:100])[0]
                t = re.findall(r'\d{2}\/[a-zA-Z]+\/\d{4}\:\d{2}\:\d{2}\:\d{2}', line[:100])[0]
                if( s in listIp.keys()):
                    listIp[s]['num']+=1
                    if(t not in listIp[s]['datetime'] ):
                        listIp[s]['datetime'].append(coverTime(t))
                else:
                    listIp[s]=dict()
                    listIp[s]['num']=1
                    listIp[s]['datetime']=list()
                    listIp[s]['datetime'].append(coverTime(t))
                    listIp[s]['inBlackList']=False
                    if(len(t)>1):
                        listIp[s]['inital']=coverTime(str(t))
                if(checkSpam(s)):
                    print(f"{bcolors.FAIL}'"+s+"' dang spam cuc manh")
                if(len(s)>3 and len(t)>3):
                    if(blackList.count(s)):
                        listIp[s]['inBlackList']=True
                        print(f"{bcolors.WARNING}Phat hien IP: '"+f"{bcolors.FAIL}"+s+f"{bcolors.WARNING}' khong tot vao luc: ("+str(coverTime(t))+")")
                    else:
                        response=requests.get("http://api.antideo.com/ip/health/"+s).json()
                        for i in response['health']:
                            if(response['health'][i]):
                                listIp[s]['inBlackList']=True
                                print(f"{bcolors.WARNING}Phat hien IP: '"+f"{bcolors.FAIL}"+s+f"{bcolors.WARNING}' khong tot vao luc: ("+str(coverTime(t))+")")
        file.close()
        tm.sleep(1)    
    
if __name__=="__main__":
    paser = argparse.ArgumentParser()
    paser.add_argument('-f', "--filelog",
                       help="duong dan file log", required=True)
    paser.add_argument('-fbl', "--fileblacklist",
                       help="file blacklist", required=True)
    args = paser.parse_args()
    t1=threading.Thread(target = process2)
    
    #process(args.filelog,args.fileblacklist)
    #t1.start
    t2 = threading.Thread(target = process,args=(args.filelog,args.fileblacklist))
    t1.start()
    t2.start()
    # t1.start()
