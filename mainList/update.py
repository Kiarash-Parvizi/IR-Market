import requests

init_url = "http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0"

def run():
    res = requests.get(url = init_url)
    print(res.status_code)
    with open('dat.txt', 'w', encoding='utf-8') as f:
        f.write(res.text)