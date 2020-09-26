from win10toast import ToastNotifier
import stocks.company
import net

base_url = 'http://www.tsetmc.com/tsev2/data/instinfodata.aspx?i={id}&c=67%20'
comLis = stocks.company.load_all()

toaster = ToastNotifier()
f = open('safe_res.txt', 'w', encoding='utf-8')

while True:
    for v in comLis:
        addr = base_url.format(id=v.id)
        res = net.get(addr)
        vec_data = res.text.split(',')
        #
        if len(vec_data) < 4:
            continue
        #
        yesterday_price = int(vec_data[5])
        last_price = int(vec_data[3])
        if last_price <= yesterday_price:
            continue
        current_price = int(vec_data[2])
        ratio = current_price/last_price-1
        if (ratio < -0.04):
            #f.write(str(ratio) + ' : ' + v.name + '\n')
            #f.flush()
            toaster.show_toast("IR-Market", v.name)
            print('--------------')
        print(v.id, '|', ratio, ':', last_price, current_price)
