import threading
import os
import re
import requests
import json
import sys
import time
from pathlib import Path
import argparse
flag = None
fileSize = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def checkFileSize(filelog):
    global flag
    file_size_defaule=os.path.getsize(filelog)
    while True:
        if(os.path.getsize(filelog) != file_size_defaule):
            file_size_defaule=os.path.getsize(filelog)
            flag=1
            print("check1")
        time.sleep(1)

def process(filelog,fileblacklist):
    global flag
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
                if(len(s)>3):
                    if(blackList.count(s)):
                        print(f"{bcolors.WARNING}Phat hien IP: '"+f"{bcolors.FAIL}"+s+f"{bcolors.WARNING}' khong tot vao luc: "+time.asctime())
        file.close()
        time.sleep(3)    
    
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
