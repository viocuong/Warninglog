import threading
import os
import re
import requests
import json
import sys
import time as tm
import datetime
from pathlib import Path
import argparse
flag = None

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

def checkSpam(filelog):
    print(1)
    
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
def process(filelog,fileblacklist):
    global flag
    setIp=set()
    listIp=dict()
    
    blackList = []
    path = Path(filelog)
    path_bl = Path(fileblacklist)
    with open(path_bl, "r") as file:
        listbl = file.readlines()
        for i in listbl:
            blackList.append(re.findall(r'[0-9]+(?:\.[0-9]+){3}', i)[0])
    # response=requests.get("http://api.antideo.com/ip/health/27.69.63.222")
    # print(response.json())
    
    pointer_current=0
    while True:
        file = open(path, "r+")
        file.seek(pointer_current)
        line = file.readline()
        ## Nếu đọc hết file chờ cho đến khi file log được cập nhật thêm
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
                        listIp[s]['datetime'].append(t)
                else:
                    listIp[s]=dict()
                    listIp[s]['num']=1
                    listIp[s]['datetime']=list()
                    listIp[s]['datetime'].append(t)
                    if(len(t)>1):
                        print(t)
                        print(s)
                        listIp[s]['inital']=coverTime(str(t))
                        
                
                if(len(s)>3 and len(t)>3):
                    if(blackList.count(s)):
                        print(f"{bcolors.WARNING}Phat hien IP: '"+f"{bcolors.FAIL}"+s+f"{bcolors.WARNING}' khong tot vao luc: ("+str(coverTime(t))+")")
        file.close()
        tm.sleep(2)    
    
if __name__=="__main__":
    paser = argparse.ArgumentParser()
    paser.add_argument('-f', "--filelog",
                       help="duong dan file log", required=True)
    paser.add_argument('-fbl', "--fileblacklist",
                       help="file blacklist", required=True)
    args = paser.parse_args()
    process(args.filelog,args.fileblacklist)
    # t1=threading.Thread(target = checkFileSize ,args=(args.filelog,))
    # t2 = threading.Thread(target = process,args=(args.filelog,args.fileblacklist))
    # t2.start()
    # t1.start()
