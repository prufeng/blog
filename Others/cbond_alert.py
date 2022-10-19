# 可转债申购和上市提醒
import requests
import random
import os
from bs4 import BeautifulSoup
import json
from tkinter import *
from datetime import date

def main():
        today = date.today().strftime('%Y-%m-%d')
        # today='2022-10-11'
        print('Today is', today)
        monitor_code=['127073','123158','118022'] #,'128062' only can access code in the page 1
        print('Monitoring', monitor_code)
        
        data = req_data()
        print('Loaded data',len(data))
        (pubtoday, lsttoday, monitoring) = parse_data(data, today, monitor_code)
        pop_window(monitoring, pubtoday, lsttoday)

def req_data():
    url = 'http://data.eastmoney.com/kzz/default.html'
    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123030765374725206196_1665969085956&sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE,f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO,f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE,f23~01~CONVERT_STOCK_CODE~PBV_RATIO&quoteType=0&source=WEB&client=WEB'
    try:
        headers = req_headers()
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        # print(r.status_code)
        r.encoding = r.apparent_encoding
        # print(r.text)
        # soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
    except:
        print('Failed to connect to ' + url)
    else:
        jtext = json.loads(r.text[r.text.index('(')+1:-2])
        # print(jtext)
        # print(jtext['version'])
        # print(jtext['result']['data'][0])
        return jtext['result']['data']

def parse_data(data, today, monitor):
    pubtoday = []
    lsttoday = []
    monitoring = []
    for v in data:
        ldate = '-' if v['LISTING_DATE']==None else v['LISTING_DATE'][:10]
        if today == v['PUBLIC_START_DATE'][:10]:
            pubtoday.append(v)
        if today == ldate:
            lsttoday.append(v)
        if v['SECURITY_CODE'] in monitor:
            monitoring.append(v)

    return (pubtoday, lsttoday, monitoring)

def pop_window(monitoring, pubtoday, lsttoday):
    window = Tk()
    window.title('可转债一览表')
    window.geometry("1450x500")

    header_cn = ['债券代码', '债券简称', '申购日期', '转股价', '转股价值', '债现价', '转股溢价率', '上市时间']
    header_en = ['SECUCODE', 'SECURITY_NAME_ABBR', 'PUBLIC_START_DATE', 'TRANSFER_PRICE', 'TRANSFER_VALUE', 'CURRENT_BOND_PRICE', 'TRANSFER_PREMIUM_RATIO', 'LISTING_DATE']
    
    header_row(window, header_cn)
    row_no = label_row(window, '今日申购', 1, len(header_en))
    row_no = grid_row(window, pubtoday, row_no, header_en)

    row_no = label_row(window, '今日上市', row_no, len(header_en))
    row_no = grid_row(window, lsttoday, row_no, header_en)

    row_no = label_row(window, '我的自选', row_no, len(header_en))
    row_no = grid_row(window, monitoring, row_no, header_en)

    window.mainloop()


def label_row(window, label, row_no, max_col_no):
    e = Label(window, text=label)
    e.grid(row=row_no, column=0, columnspan=max_col_no)
    row_no = row_no + 1
    return row_no

def header_row(window, header_cn):
    for j in range(len(header_cn)):
        e = Entry(window, width=25, font=('Arial', 10, 'bold'))
        e.grid(row=0, column=j)
        e.insert(END, header_cn[j])

def grid_row(window, row_data, row_no, header_en):
    for v in row_data:
        for j in range(len(header_en)):
            e = Entry(window, width=25, font=('Arial', 10))
            e.grid(row=row_no, column=j)
            h = header_en[j]
            # print(v.get(h))
            e.insert(END, str(v.get(h)))
    
        row_no = row_no + 1
    return row_no

def req_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
    ]
    random_user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': random_user_agent
    }

    return headers


if __name__ == "__main__":
    main()
