import platform
import aiohttp
import asyncio
import sys
import datetime

def days(day):
    if day<=10 and day>0:
        date=[]
        for d in range(day):
            today=datetime.datetime.now().date()
            delta=datetime.timedelta(days=d)
            str_data=(today-delta).strftime("%d.%m.%Y")
            date.append(str_data)
        return date
    else:
        return [datetime.datetime.now().date().strftime("%d.%m.%Y")]
    
def date_eur_usd_list(res):
    eur_usd={}
    date_eur_usd={}
    curr={}
    result_list=[]
    for re in res:
        curr.update({re["date"]:re["exchangeRate"]})
    for c in curr.items():
        date=c[0]
        for cdict in c[1]:
            for ccdict in cdict.values():
                if ccdict=="EUR" or ccdict=="USD":
                    eur_usd.update({ccdict:{"sale":cdict["saleRate"],"purchase":cdict["purchaseRate"]}})
            date_eur_usd.update({date:eur_usd})
    result_list.append(date_eur_usd)
    return result_list

async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            result = await response.json()
            return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res=[]
    for d in days(int(sys.argv[1])):
        r=asyncio.run(main("https://api.privatbank.ua/p24api/exchange_rates?json"+"&date="+d))
        res.append(r)
    print(date_eur_usd_list(res))
