import subprocess
import json
import time

from datetime import datetime

from bs4 import BeautifulSoup
import re
import requests

from config import config, rpc_endpoints

def extract_headline(url):    
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    headline = soup.title.text

    #headline = 'Melania Trump cancels plans to attend Tuesday rally citing Covid recovery'
    return headline

def extract_body(url):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    summary=""		
    
    rm=[]
    class_names=["header", "footer", "nav", "side", "aside", "menu", "layout","caption","figure"]
    classes=[]    
    
    for i in range(7):
        try:
            soup.footer.decompose()
        except:
            pass

        try:
            soup.header.decompose() 
        except:
            pass
    
        try:
            soup.nav.decompose()
        except:
            pass
    
        try:
            soup.aside.decompose()
        except:
            pass

        try:
            soup.figure.decompose()
        except:
            pass

    body=soup.body.text
    for class_name in class_names:
        temp=soup.find_all(class_=re.compile(class_name))
        all_classes=soup.find_all(class_=re.compile(class_name))
        for item in all_classes:
            body=soup.body.text
            cont=str(item.text)
            ext=body.replace(cont,"")            
            if len(ext)<300:
                temp.remove(item)
        classes+=temp
    for cont in classes:
        rm+=cont.find_all("p")
    pclass=""
    temp2=0
    for cont in soup.find_all("p"):
        temp2=0
        try:
            pclass=cont['class']
            pclass=pclass[0]
            for class_name in class_names:
                if class_name in pclass:
                    temp2=1
                    break    
        except:
            pass
        if cont not in rm and temp2==0:
            temp=cont.text
            try:
                if temp[-1]!=".":
                    temp+=". "
                else:
                    temp+="  "
            except:
                pass
            summary+=temp
            summary=summary.replace("\n"," ")
        pclass=""

    # summary = '''Melania Trump is canceling her first campaign appearance in
    # months because she is not feeling well as she continues to recover from
    # Covid-19.'''
    return summary


url = "https://stackoverflow.com/questions/35956045/extract-title-with-beautifulsoup"
body = extract_body(url)
#print(body)
headline = extract_headline(url2)
#print(headline)