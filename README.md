LIRR.py
=========

Hate opening a browser to get long island railroad train times? 

LIRR.py obtains the 4 most recent train times given a source and destination.


Installation
---
    git clone https://github.com/Dannyzen/lirr.git



Usage
---
python lirr.py -s source -d destination



Example
---
python lirr.py -s penn -d hicks

    Source departure times

    ['02:14 PM', '02:29 PM', '02:52 PM', '03:07 PM']

    Destination arrival times

    ['02:59 PM', '03:17 PM', '03:41 PM', '03:48 PM']

    Trip duration in minutes

    [u'45', u'48', u'49', u'41']
