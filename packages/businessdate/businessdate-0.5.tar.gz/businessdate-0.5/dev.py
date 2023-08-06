# -*- coding: utf-8 -*-

# businessdate
# ------------
# Python library for generating business dates for fast date operations
# and rich functionality.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.5, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/businessdate
# License:  Apache License 2.0 (see LICENSE file)


from __future__ import print_function


if False:
    from businessdate import BusinessDate as BD, BusinessSchedule
    from businessdate import BusinessPeriod as BP

    a = BD()
    p = BP('1y2m3d')
    b = a + p

    print(a, p, b - a, a - b)

    a = BD(20160229)
    p = BP('1y1m')
    b = a + p

    print(a, p, b, b - a, a - b)

    print(BD(20160229) + '1y' + '1m', BD(20160229) + '1m' + '1y', BD(20160229) + '1y1m')

    print(not BP("3M") == BP("1M"))
    print(not BP("31d") == BP("1M"))
    print(BP("1Y") == BP("12M"))
    print(BP("3M") == BP("1M") + "2m")

    print(BD("20190418").is_business_day())

if False:
    import businessdate.basedate

    businessdate.basedate.BaseDate = businessdate.basedate.BaseDateFloat

    from businessdate import BusinessDate

    print(businessdate.basedate.BaseDate)
    print('')
    print(BusinessDate().baseclass)
    print(businessdate.BusinessDate().baseclass)
    print(businessdate.businessdate.BusinessDate().baseclass)

if False:
    from time import time
    from businessdate import BusinessDate, BusinessPeriod, BusinessSchedule

    n = 1
    s = BusinessDate()
    e = s + BusinessPeriod('100Y')
    p = BusinessPeriod('1M')

    t = time()
    for _ in range(n):
        BusinessSchedule(s, e, p).adjust()
    print(s.baseclass, 'BusinessSchedule', (time() - t) / n)

    # 1x
    # BaseDateDatetimeDate 0.631363153458
    # BaseDateFloat 0.865006923676
    # BaseDateTuple 1.58643198013

    # 10x
    # BaseDateDatetimeDate 0.640032410622
    # BaseDateFloat 0.852301883698
    # BaseDateTuple 1.23395960331

if False:
    from time import time
    from businessdate import BusinessDate, BusinessPeriod, BusinessSchedule

    n = int(1e6)
    s = BusinessDate()
    e = s + BusinessPeriod('1y')

    t = time()
    for _ in range(n):
        s._add_years(1)
    print(s.baseclass, '_add_years', (time() - t) / n)

    # 1e6 _add_years
    # BaseDateDatetimeDate 4.1959002018e-06
    # BaseDateFloat 6.634775877e-06
    # BaseDateTuple 1.15310940742e-05

    t = time()
    for _ in range(n):
        s._add_months(1)
    print(s.baseclass, '_add_months', (time() - t) / n)

    # 1e6 add_days
    # BaseDateFloat 1.97633004189e-06
    # BaseDateDatetimeDate 5.02036499977e-06
    # BaseDateTuple 1.36047940254e-05

    t = time()
    for _ in range(n):
        s._add_days(1)
    print(s.baseclass, 'add_days', (time() - t) / n)

    # 1e6 add_days
    # BaseDateFloat 1.97633004189e-06
    # BaseDateDatetimeDate 5.02036499977e-06
    # BaseDateTuple 1.36047940254e-05

    t = time()
    for _ in range(n):
        s < e
    print(s.baseclass, 'leq', (time() - t) / n)

    # 1e6 leq
    # BaseDateDatetimeDate 1.44394159317e-07
    # BaseDateFloat 1.7797088623e-07
    # BaseDateTuple 2.16879796982e-06

    t = time()
    for _ in range(n):
        s == e
    print(s.baseclass, '==', (time() - t) / n)

    # 1e6 ==
    # BaseDateDatetimeDate 1.68392896652e-07
    # BaseDateFloat 1.74712896347e-07
    # BaseDateTuple 2.41393589973e-06

    """ 20190724
    BaseDateFloat BusinessSchedule 1.13527107239
    BaseDateFloat _add_years 8.06885409355e-06
    BaseDateFloat _add_months 1.45274348259e-05
    BaseDateFloat add_days 2.22360181808e-06
    BaseDateFloat leq 1.03132009506e-07
    BaseDateFloat == 1.10569000244e-07

    BaseDateDatetimeDate BusinessSchedule 0.504576921463
    BaseDateDatetimeDate _add_years 2.55046105385e-06
    BaseDateDatetimeDate _add_months 3.1582660675e-06
    BaseDateDatetimeDate add_days 5.83482694626e-06
    BaseDateDatetimeDate leq 1.04933023453e-07
    BaseDateDatetimeDate == 1.02378129959e-07
    """

if False:
    from businessdate.businessdate import NewBusinessDate

    n = NewBusinessDate('3M') + NewBusinessDate(20191231)
    print(n)
    print(n.month)
    print(n.months)
    print(n.to_businessdate())

if False:
    from datetime import date, timedelta

    print(date(2015, 0o1, 29) + timedelta(30))
    print(date(2015, 0o1, 29) + timedelta(30) - date(2015, 0o1, 29))

if False:
    from businessdate import BusinessDate as bd

    x = bd('-1M', '20110201', 'MOD_PREVIOUS', bd.DEFAULT_HOLIDAYS)
    print(x, type(x))
    x = bd('3B1Y', None, 'MOD_PREVIOUS', bd.DEFAULT_HOLIDAYS)
    print(x, type(x))
    x = bd('3B1Y1B', None, 'MOD_PREVIOUS', bd.DEFAULT_HOLIDAYS)
    print(x, type(x))
    x = bd('3B-1Y6M-1B', None, 'MOD_PREVIOUS', bd.DEFAULT_HOLIDAYS)
    print(x, type(x))

if False:
    from datetime import date
    from businessdate import BusinessDate

    d = date.fromordinal(735963)
    x = BusinessDate.fromordinal(d.toordinal())
    print(d, x, x.adjust_mod_follow())
    print(BusinessDate.today(), BusinessDate(), date.today())
    print(BusinessDate('0B3D0BMODFOLLOW20171231'))

if False:
    from businessdate import BusinessPeriod

    print(BusinessPeriod(''))
    # print(BusinessPeriod('1B2D1B'))
    print(BusinessPeriod._parse_ymd('1B'))
    print(BusinessPeriod._parse_ymd('1B2D'))
    print(BusinessPeriod._parse_ymd('1B2D1B'))
    print(BusinessPeriod._parse_ymd('2D'))
    print(BusinessPeriod._parse_ymd('2D1B'))

if False:
    from businessdate import BusinessDate

    BusinessDate().adjust()
    BusinessDate().get_day_count(BusinessDate())

    # doctest

    from datetime import date, timedelta
    from businessdate import BusinessDate, BusinessPeriod

    BusinessPeriod(businessdays=10)
    BusinessPeriod(years=2, months=6, days=1)
    BusinessPeriod(years=1, months=6)
    BusinessPeriod(months=18)
    BusinessPeriod(months=1, days=45)
    BusinessPeriod(months=2, days=14)
    BusinessPeriod(months=2, days=15)
    # BusinessPeriod(businessdays=1, days=1)

    from datetime import date, timedelta
    from businessdate import BusinessDate, BusinessPeriod

    a, b = date(2010, 6, 1), date(2010, 12, 31)
    b - a
    BusinessPeriod(b - a)
    timedelta(213)
    BusinessPeriod(timedelta(213))

    from datetime import date, timedelta
    from businessdate import BusinessDate, BusinessPeriod

    BusinessPeriod('-0b')
    BusinessPeriod('-10D')
    BusinessPeriod('-1y3m4d')
    BusinessPeriod('-18M')
    BusinessPeriod('-1Q')
    BusinessPeriod('-2w')
    BusinessPeriod('-10B')
    BusinessPeriod(years=-2, months=-6, days=-1)

    from businessdate import BusinessDate, BusinessPeriod

    BusinessDate.BASE_DATE = 20161010
    BusinessDate()
    # create from period
    BusinessDate(BusinessPeriod(months=1))
    # create from period string
    BusinessDate('1m')
    BusinessDate() + '1m'
    # works with additional date as well
    BusinessDate('1m20161213')
    BusinessDate('20161213') + '1m'
    # even for business days
    BusinessDate('15b')
    BusinessDate() + '15b'
    # add adjustment convention 'end_of_month' with a business date
    BusinessDate('0bEOM')
    BusinessDate('15bEOM')
    # add adjustment convention 'mod_follow' with a business date
    BusinessDate('0bModFlw')
    BusinessDate('15bModFlw')
    # adjustment convention without a business date is ignored
    BusinessDate('EOM')
    BusinessDate('ModFlw')
    # even together with a classical period since the adjustment statement is ambiguous
    # should the start date (spot) or end date be adjusted?
    BusinessDate('1mModFlw')
    # but adding zero business days clarifies it
    BusinessDate('0b1mModFlw')
    BusinessDate('0b1mModFlw') == BusinessDate().adjust('ModFlw') + '1m'
    BusinessDate('1m0bModFlw')
    BusinessDate('1m0bModFlw') == (BusinessDate() + '1m').adjust('ModFlw')
    # clearly business days may be non zero, too
    BusinessDate('15b1mModFlw')
    BusinessDate('15b1mModFlw') == BusinessDate('15b').adjust('ModFlw') + '1m'
    BusinessDate('1m5bModFlw')
    BusinessDate('1m5bModFlw') == (BusinessDate() + '1m').adjust('ModFlw') + '5b'
    # putting all together we get
    BusinessDate('15b1m5bModFlw20161213')
    BusinessDate('15b1m5bModFlw20161213') == ((BusinessDate(20161213) + '15b').adjust('ModFlw') + '1m').adjust(
        'ModFlw') + '5b'

if False:
    from businessdate import BusinessDate, BusinessPeriod, BusinessRange

    rng = BusinessRange('19990101', '20051231')
    for a in rng:
        for b in rng:
            if min(a, b).day > 0:
                b - a

if False:
    from datetime import timedelta, date
    from businessdate import BusinessDate, BusinessPeriod, BusinessRange

    for p in ('1M0D', '1M1D', '1M2D', '1M3D', '100D'):
        jan = BusinessDate(20150129)
        mar = jan + p
        print(('mar = jan + p', p, jan, mar, mar-jan, jan-mar))

    for p in ('1M0D', '1M1D', '1M2D', '1M3D', '100D'):
        mar = BusinessDate(20150301)
        jan = mar - p
        print(('jan = mar - p', p, jan, mar, mar-jan, jan-mar))

if False:

    class avg_day_per_month(object):

        cum_days = list(enumerate([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]))

        def __init__(self, max=12, start=0):
            self.start = start
            self.pos = self.start
            self.cum = 0
            self.num = 0
            self.max = max


        def __iter__(self):
            self.pos = self.start
            self.cum = 0
            self.num = 0
            return self

        def __next__(self):
            if self.max <= self.num:
                raise StopIteration
            i, d = self.__class__.cum_days[self.pos % 12]
            self.pos += 1
            self.cum += (d + 1) if self.pos % 48 == 36 + 2 else d
            self.num += 1
            return self.cum

    # for i in range(124):
    #     starts = [list(iter(avg_day_per_month(max=i+1, start=s)))[-1] for s in range(12)]
    #     mx = [i+1 for i, e in enumerate(starts) if e == max(starts)]
    #     mn = [i+1 for i, e in enumerate(starts) if e == min(starts)]
    #     # print((i, max(starts), mx))
    #     # print((i, min(starts), mn))
    #     #print((i+1, min(starts), max(starts), max(starts)-min(starts)))
    #     #print((i, max(starts), min(starts)))
    #     #print(min(starts))

    # days = 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31
    # rday = tuple(reversed(days))
    # print(rday)
    # mn,mx = 0, 0
    # for i in range(12):
    #     mn += days[int(i%12)]
    #     mn += 1 if int(i % 48) == 36 else 0
    #     mx += rday[int(i%12)]
    #     mx += 1 if int(i % 48) == 11 else 0
    #     print((i+1, mn, mx, mx-mn))

    from businessdate import BusinessPeriod, BusinessDate, BusinessRange

    jan31 = BusinessDate(20010131)
    feb01 = BusinessDate(20010201)

    for date in BusinessRange(20000101, 21000101):
        if date.month==1 and date.day==1:
            print('\n:', end='')
        for m in range(12):
            period = BusinessPeriod(months=m)
            mn, mx = period.min_days(), period.max_days()
            # dn, dx = feb01.diff_in_days(feb01 + period), (jan31 - period).diff_in_days(jan31)
            fwd, bck = date.diff_in_days(date + period), (date - period).diff_in_days(date)
            if not mn < fwd < mx:
                print('.', end='')
                if not mn <= fwd <= mx:
                    print((period, date, mn, fwd, mx))
            elif not mn < bck < mx:
                print('*', end='')
                if not mn <= bck <= mx:
                    print((period, date, mn, bck, mx))
            print(' ', end='')

if False:
    from businessdate import BusinessPeriod, BusinessDate, BusinessRange

    BusinessPeriod('13m').max_days()  # 397
    BusinessPeriod('13m').min_days()  # 393
    BusinessPeriod('13m') < BusinessPeriod('395d')  # not well defined -> None
    BusinessPeriod('13m') < BusinessPeriod('397d') # False
    BusinessPeriod('13m') <= BusinessPeriod('397d') # True
    BusinessPeriod('ON') == BusinessPeriod('1B') # True
    BusinessPeriod('7D') == BusinessPeriod('1W') # True
    BusinessPeriod('30D') == BusinessPeriod('1M') # False
    BusinessPeriod('1D') == BusinessPeriod('1B')  # not well defined -> None

if True:

    from businessdate import BusinessDate
    s, e = BusinessDate(20190915), BusinessDate(20190915) + '10y'
    for a in dir(s):
        print(a)

    print(s.get_act_360(e))
    print(s.get_day_count(e, 'act360'))
    print(s.get_act_act(e))
    print(s.get_day_count(e, 'actact'))
    print(s.adjust_flw())
    print(s.adjust_follow())
    print(s.adjust('follow'))
    print(s.adjust_imm())
    print(s.adjust('imm'))
