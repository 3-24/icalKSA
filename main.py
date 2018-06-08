#-*- coding: utf-8 -*-

from icalendar import Calendar, Event
from datetime import datetime
import requests, urllib2,sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8') # for hangul

def get_html(url):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    content = page.read()
    return content

def get_data(url):
    list = []
    content = get_html(url)
    soup = BeautifulSoup(content, 'html.parser')
    whole = soup.select('#kcontent > div.page_content > div:nth-of-type(2) > div > div > div > table > tbody > tr')
    for i in range (0,len(whole)):
        part = whole[i]
        splitpart = part.text.split('\n')
        for i in range (len(splitpart)):
            s = splitpart[i]
            if s != '':
                if not (len(s) == 13 and s[4] == '-' and s[7] == '-'):
                    if (ord(s[0])==42):
                        s = s[1:]
                    if (ord(s[0]) == 9675):
                        s = s[2:]
                    if not ((s[0:4] == '졸업연구' or s[0:3] == 'R&E' \
                        or s[0:9] == '연구방법기초세미나' or s[0:6] == '창의설계활동') \
                        and (s[-1] == ')' and (s[-3] == '(') or s[-4] == '(')) and not (s[-2]+s[-1] == '주차') \
                        and not (s == '교무회의' or s == '담임협의회'):
                        des = s
                        list.append([date,des])
                else: date = s
    return list

def mainParse(year):
    number = 0
    cal = Calendar()
    def addEvent(title,start,end):
        event = Event()
        event['summary'] = title
        event['dtstart'] = start
        event['dtend'] = end
        cal.add_component(event)

    for i in range (1,13):
        url = 'https://ksa.hs.kr/SchoolEvent/Index/135?year='+str(year)+'&month='+str(i)
        L = get_data(url)
        for j in range (len(L)):
            year = L[j][0][0:4]
            month = L[j][0][5:7]
            date = L[j][0][8:10]
            maintime = str(year)+str(month)+str(date)
            #if ord(L[j][1][0]) == 42 or ord(L[j][1][0]) == 9675: #asterisk and circle unicodes
                #desc = L[j][1][1:]
            #else:
            desc = L[j][1]
            addEvent(desc,maintime,maintime)
            number +=1

    f = open('KSA.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
    print number

mainParse(2018)
