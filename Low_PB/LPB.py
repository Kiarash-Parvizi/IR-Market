import net
url_tmpl = 'https://rahavard365.com/asset/{}/%D8'

li = []

c = 0
for i in range(4, int(2e4)):
    res = net.get(url_tmpl.format(i)).text
    try:
        loc = res.find('last_pb')
        if loc != -1:
            loc_e = res.find('date', loc)
            #print(i, ':', res[loc+18:loc_e-2])
            pb = float(res[loc+18:loc_e-2])
            li.append((i, pb))
    except:
        print('err at', i)
    c += 1
    if c == 100:
        print('.')
        c = 0
li.sort(key = lambda x: x[1])
print(li)

with open('res.txt', 'w') as f:
    col_width = max(len(str(word)) for row in li for word in row) + 2  # padding
    for tup in li:
        f.write("".join(str(word).ljust(col_width) for word in tup[:-1]) + str(tup[-1]) + '\n')
#    for (id, pb) in li:
#        f.write(str(id) + ' : ' + str(pb) + '\n')
