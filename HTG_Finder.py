# Hard-to-get Finder
import net
import stocks.company

base_url = r'https://core.tadbirrlc.com//StocksHandler.ashx?%7B%22Type%22:%22compactintradaychart%22,%22la%22:%22Fa%22,%22isin%22:%22{symbol}%22%7D'
tset_base_url = r'http://www.tsetmc.com/tsev2/data/instinfodata.aspx?i={id}&c=67%20'

comLis = stocks.company.load_all()

def had_constant_price(prices) -> bool:
    if len(prices) == 0:
        return True
    pre_price = prices[0]
    for price in prices:
        if price != pre_price:
            return False
        pre_price = price
    return True

final_list = []

for com in comLis:
    try:
        # tset
        tset_vec_data = net.get(tset_base_url.format(id=com.id)).text.split(',')
        last_price = int(tset_vec_data[3])
        yesterday_price = int(tset_vec_data[5])
        # tadbirrlc
        url = base_url.format(symbol=com.symbol)
        prices = [vec[3] for vec in net.get(url).json()['olst'][5]]
        if had_constant_price(prices):
            print(com.symbol)
            final_list.append((last_price/yesterday_price, com))
    except KeyboardInterrupt:
        exit()
    except:
        continue

final_list.sort(key = lambda x: x[0])

with open('HTG_res.txt', mode='w', encoding='utf-8') as f:
    for el in final_list:
        com = el[1]
        f.write(str(el[0]) + '\t\t' + com.name + '\t\t' + com.symbol + '\t\t' + com.id + '\n')