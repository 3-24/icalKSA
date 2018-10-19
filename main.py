from icalendar import Calendar, Event
import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr


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
            desc = L[j][1]
            addEvent(desc,maintime,maintime)
            number +=1

    f = open('KSA.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
    print(number)

mainParse(2018)
