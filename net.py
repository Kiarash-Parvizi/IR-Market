import requests

def post(url: str, data: dict) -> requests.Response:
    while True:
        try:
            res = requests.post(url = url, data = data, timeout = 3)
            break
        except requests.Timeout as err:
            print("timeout: ", str(data))
        except requests.RequestException as err:
            print("ERR: request exceptions")
    return res

def get(url: str) -> requests.Response:
    while True:
        try:
            res = requests.get(url = url, timeout = 3)
            break
        except requests.Timeout as err:
            print("timeout: ", url[-10:])
        except requests.RequestException as err:
            #print("ERR: request exceptions")
            pass
    return res

def session_get(url: str) -> requests.Response:
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Host': 'www.tsetmc.com',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': r'_ga=GA1.2.2047787200.1600798355; _gid=GA1.2.608074105.1600798355; ASP.NET_SessionId=j4vvs1u2jxj3311gjtfphyb3',
    }
    #s.get(url = url, timeout = 3)
    while True:
        try:
            res = s.get(url = url, timeout = 4, headers=headers)
            break
        except requests.Timeout as err:
            print("timeout: ", url[-10:])
        except requests.RequestException as err:
            #print("ERR: request exceptions")
            pass
    return res