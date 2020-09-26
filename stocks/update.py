from stocks.company import *

def isMainCompany(name: str) -> bool:
    #digCount = 0
    for c in name:
        if c.isdigit():
            return False
            #digCount = digCount + 1
    print(name)
    return True#digCount < 2

def run(location: str):
    ids = {}
    raw = open(location, 'r', encoding='utf-8').read()
    # looping
    for vek in raw.split(';')[1:]:
        subs = vek.split(',')
        #if subs[2] != 'خساپا':
        #    continue
        print(subs)
        if subs[0] in ids:
            break
        if not isMainCompany(subs[2]):
            continue
        ids[subs[0]] = subs[2]
        c = company(subs[0], subs[2])
        c.save()

def get_stocks():
    pass

