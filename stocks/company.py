import net
import requests
from requests.exceptions import Timeout

import pickle
import matplotlib.pyplot as plt

import re

from typing import List
from os import listdir
from os.path import isfile, join

url_template = "http://members.tsetmc.com/tsev2/chart/data/Financial.aspx?i={id}&t=ph&a=0"
stats_template= "http://www.tsetmc.com/Loader.aspx?ParTree=151311&i={id}"
tarazUrl_template = 'http://www.tsetmc.com/tsev2/data/CodalContent.aspx?s={}&r=6&st=6&pi=0'
#
holdersAV_pattern = re.compile(r'"جمع حقوق صاحبان سهام",{"_Id":"ctl00_cphBody_ucSFinancialPosition_grdSFinancialPosition_ctl\d+_txbLiabilityYear0","_text":"(-?\d+)"}')

highest_monthVol = 0

class company:
    def __init__(self, id: str, name: str, symbol: str):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.prices = []
        #get data from tsetmc
        addr = url_template.format(id = id)
        #session
        #s = requests.session()
        while True:
            try:
                resp = requests.get(url = addr, timeout = 7)
                break
            except Timeout as ex:
                print("timeout")
        vek = resp.text.split(';')
        for v in vek:
            subs = v.split(',')
            if len(subs) < 3:
                break
            #price = (int(subs[1]) + int(subs[2]))/2
            price = int(subs[-1])
            self.prices.append(price)
        # EPS, marketVal, PE,...
        while True:
            try:
                resp = requests.get(url = stats_template.format(id = id), timeout = 7)
                break
            except Timeout as ex:
                print("timeout")
        stats = resp.text
        #eps
        m = re.search('EstimatedEPS\s*=\s*\W?(-?[0-9]\d*(\.\d+)?)', stats)
        self.EPS = float(m.group(1)) if m and len(m.group(1)) != 0 else 0
        self.PE  = self.prices[-1]/self.EPS if len(self.prices) > 0 and self.EPS != 0 else -1
        #baseVol
        m = re.search('BaseVol\s*=\s*\W*(\d*)', stats)
        self.baseVol = int(m.group(1)) if m and len(m.group(1)) != 0 else 0
        #shareCount
        m = re.search('ZTitad\s*=\s*\W*(\d*)', stats)
        self.shareCount = int(m.group(1)) if m and len(m.group(1)) != 0 else 0
        #monthVol
        m = re.search('QTotTran5JAvg\s*=\s*\W*(\d*)', stats)
        self.monthVol = int(m.group(1)) if m and len(m.group(1)) != 0 else 0
        #sectorPE
        m = re.search('SectorPE\s*=\s*\W?(-?[0-9]\d*(\.\d+)?)', stats)
        self.sectorPE = float(m.group(1)) if m and len(m.group(1)) != 0 else 0
        #floatingShares
        m = re.search('KAjCapValCpsIdx\s*=\s*\W*(\d*)', stats)
        self.floatingShares = int(m.group(1)) if m and len(m.group(1)) != 0 else 0
        # NEW
        # Tarazname
        tarazUrl = tarazUrl_template.format(self.name)
        tarazData = net.session_get(tarazUrl).text
        self.holdersAV_vec = [int(s) for s in holdersAV_pattern.findall(tarazData)]
        print('->>>', self.holdersAV_vec)
        print('->=>', holdersAV_pattern.findall(tarazData))
        print(self.holdersAV_vec)
        # --

    def get_holdersAV(self):
        if "holdersAV_vec" not in self.__dict__ or len(self.holdersAV_vec) == 0:
            return 0
        return self.holdersAV_vec[0]
    
    def holdersAV_to_shareCount_to_price(self) -> float:
        if "holdersAV_vec" not in self.__dict__ or len(self.holdersAV_vec) == 0:
            return 0
        return round(self.holdersAV_vec[0] * 1e6 / self.shareCount / self.get_price(), 3)

    def AVG(self, days: int) -> float:
        sum = 0
        for v in self.prices[-days:]:
            sum += v
        return sum / days

    def PA_ratio(self, days: int) -> float:
        if len(self.prices) < days:
            return 100
        return round(self.prices[-1]/self.AVG(days), 2)
    
    def Score(self, days: int) -> float:
        # changes: a*8
        #a = 8 * 2 / (self.PA_ratio(days) + 1)
        #b = (self.sectorPE / self.PE) * (-1 if self.PE > 0 and self.sectorPE < 0 else 1) / 2
        #c = (10 / (self.PE+10) if self.PE > 0 else 0)
        #d = 1 / (self.floatingShares/7 + 1)
        #e = (self.monthVol / highest_monthVol)
        #return a + b + c + d + e
        return self.holdersAV_to_shareCount_to_price()
    
    def get_price(self, offset=1):
        if len(self.prices) < offset:
            return 0
        return self.prices[-offset]

    def plot(self, offset: int = 100):
        plt.title(self.name[::-1])
        #
        plt.plot([i for i in range(offset)], self.prices[-offset:])
        plt.show()
    
    def save(self):
        f = open('stocks/dat/'+self.name+'.bin', 'wb')
        pickle.dump(self, f)

def load_company(name: str) -> company:
    return pickle.load(open('stocks/dat/'+name, 'rb'))

def load_companies(names: List[str]) -> List[company]:
    res: List[company] = []
    for name in names:
        res.append(load_company(name))
    return res

def load_all() -> List[company]:
    res: List[company] = []
    path = 'stocks/dat'
    for fName in listdir(path):
        if isfile(join(path, fName)):
            res.append(load_company(fName))
    return res



def set_highestMonthVol(lis: List[company]):
    global highest_monthVol 
    highest_monthVol = max(com.monthVol for com in lis)

