LIRR.py
=========

Hate opening a browser to get long island railroad train times? 

LIRR.py obtains the 4 most recent train times given a source and destination.


Installation
---
    git clone https://github.com/Dannyzen/lirr.git
    pip install -r requirements.txt


Usage
---
python lirr.py -s source -d destination -a [optional] additional hours



Example
---
    run at 3:50pm: python lirr.py -s penn -d hicks -a 2

    Source departure times    Destination arrival times      Trip duration in minutes
    ------------------------  ---------------------------  --------------------------
    05:46 PM                  06:31 PM                                             45
    05:51 PM                  06:13 PM                                             59
    06:01 PM                  06:45 PM                                             44
    06:08 PM                  06:59 PM                                             51


Fuzzy String Matching
---
    (core-dev)[davidjarvis@ziz:lirr] 00:13:57 $ python lirr.py -s pens -d hicks

    Couldn't autocomplete 'pens' - did you mean one of the following?
    oceanside
    hempstead gardens
    country life press
    speonk
    glen street
    queens village
    penn station
    kew gardens
