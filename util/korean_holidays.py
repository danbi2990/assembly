from workalendar.asia import SouthKorea
from datetime import datetime as dt

hd0 = [   # 대체휴일
    '20140910',
    '20150929',
    '20160210',
    '20170130',
    '20171006',
    '20180507',
    '20180926',
]
hd1 = [   # 임시공휴일
    '19880917',
    '20020701',
    '20150814',
    '20160506',
    '20170509',
    '20171002',
]
hd2 = [   # 대선
    '20170509',
    '20121219',
    '20071219',
    '20021219',
    '19971218',
]
hd3 = [   # 총선
    '20160413',
    '20120411',
    '20080409',
    '20040415',
    '20000413',
]
hd4 = [   # 지선
    '20140604',
    '20100602',
    '20060531',
    '20020613',
]

cal = SouthKorea()
years = range(2000, 2019)
hds = []
[hds.extend([h[0] for h in cal.holidays(y)]) for y in years]
thds = [dt.strptime(h, '%Y%m%d').date() for h
        in (*hd0, *hd1, *hd2, *hd3, *hd4)]
hds.extend(thds)
# print(hds)


# 2014.09.10: Extended Holiday
'''
Extended Holidays:
[20140910, 20150929, 20160210, 20170130, 20171006, 20180507, 20180926]
https://namu.wiki/w/%EB%8C%80%EC%B2%B4%20%ED%9C%B4%EC%9D%BC%20%EC%A0%9C%EB%8F%84#s-4

Temporary Holidays (since 2002)
[19880917, 20020701, 20150814, 20160506, 20170509, 20171002]
https://namu.wiki/w/%EC%9E%84%EC%8B%9C%EA%B3%B5%ED%9C%B4%EC%9D%BC

Election Holidays
- President: [20170509, 20121219, 20071219, 20021219, 19971218]
https://namu.wiki/w/%EC%A0%9C16%EB%8C%80%20%EB%8C%80%ED%86%B5%EB%A0%B9%20%EC%84%A0%EA%B1%B0
- Assembly: [20160413, 20120411, 20080409, 20040415, 20000413]
https://namu.wiki/w/%EC%A0%9C17%EB%8C%80%20%EA%B5%AD%ED%9A%8C%EC%9D%98%EC%9B%90%20%EC%84%A0%EA%B1%B0
- Local: [20140604, 20100602, 20060531, 20020613]
https://namu.wiki/w/%EC%A0%9C4%ED%9A%8C%20%EC%A0%84%EA%B5%AD%EB%8F%99%EC%8B%9C%EC%A7%80%EB%B0%A9%EC%84%A0%EA%B1%B0
'''
