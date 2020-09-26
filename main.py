import stocks.company
import stocks.update
import mainList.update
import filter.company

# update mainList
#mainList.update.run()

# update stocks
#stocks.update.run('mainList/dat.txt')
#print("update finished")
#exit()

print("technical analysis...")
days = 20

comLis = stocks.company.load_all()
comLis = filter.company.noShareDilution(comLis, days)
stocks.company.set_highestMonthVol(comLis)

lis = []
for com in comLis:
    if com.name == 'ولساپا':
        print('hav: ', com.holdersAV_vec)
        #print('shareCount: ', com.shareCount)
        #print('price: ', com.get_price())
        #com.plot(days)
        #exit(0)
    lis.append((com.Score(days), com.holdersAV_to_shareCount_to_price(),
        com.get_holdersAV(), "pa:", com.PA_ratio(days),
        "f:", com.floatingShares, "p:", com.get_price(), "eps:", com.EPS, "pe:", round(com.PE, 2),
        "s-pe", round(com.sectorPE, 2), com.name, round(com.monthVol/stocks.company.highest_monthVol, 2)))
lis.sort()

f = open('res.txt', 'w', encoding='utf-8')
col_width = max(len(str(word)) for row in lis for word in row) + 2  # padding
for tup in lis:
    f.write("".join(str(word).ljust(col_width) for word in tup[:-1]) + str(tup[-1]) + '\n')
#for tup in lis:
#    for v in tup:
#        f.write(str(v) + '\t\t')
#    f.write('\n')

