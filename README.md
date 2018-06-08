# icalKSA

main.py는 KSA의 [학사일정](https://ksa.hs.kr/SchoolEvent/Index/135)을 긁어서 KSA.ical 파일로 저장합니다(Python 2.7 기반).

사용되는 파이썬 라이브러리 목록은 다음과 같습니다:

- [icalendar](https://icalendar.readthedocs.io/en/latest/index.html)
- bs4.BeautifulSoup
- urllib2
- request

**창의설계활동, 연구방법기초세미나, R&E, 졸업연구, 교무회의, 담임협의회, ~주차**
는 학사일정에 포함되어있으나 매 주마다 반복되어 임의로 제거했습니다.

### Google 캘린더


<div style="text-align:center"><img src ='/google_calendar.PNG' /></div><br>

[Google 캘린더에 추가](https://calendar.google.com/calendar?cid=ZnI5bDcxMTBuY2xkZjhjYTZrZXBoczNnZ2dAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ) (Last Updated: 2018.06.08)
