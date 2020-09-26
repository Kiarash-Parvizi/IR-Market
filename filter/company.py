from stocks.company import company
from typing import List

def noShareDilution(companies: List[company], days: int) -> List[company]:
    f = open('filters.txt', mode='w', encoding='utf-8')
    newCompanies: List[company] = []
    for com in companies:
        if len(com.prices) < days: continue
        pre = com.prices[-days]
        for p in com.prices[-days:]:
            if abs(p-pre) / pre > 0.3:
                f.write(com.name + '\n')
                break
            pre = p
        else:
            newCompanies.append(com)
    return newCompanies
