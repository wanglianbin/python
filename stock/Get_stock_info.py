#!/usr/bin/python
#encoding:utf-8
import urllib2
import string
import os
import sys
import time
from threading import Thread
reload(sys)
sys.setdefaultencoding("utf-8")

url = "http://hq.sinajs.cn/list="
'''
信息转码
'''
def ToGB(str):
	return str.decode('gb2312')

'''
通过URL获取股票的信息
'''
def GetStockStrByUrl(url):                                                                                                                                            
	i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                     "Referer": 'http://www.baidu.com'}
	req = urllib2.Request(url, headers=i_headers)
	try:
		stock_page = urllib2.urlopen(req)
	except urllib2.URLError:
		return 'error';
	stock_info = stock_page.read()
	return stock_info

'''
分析获取的股票信息
'''
def ParseResultStr(resultstr):
	slist=resultstr.split(',')
	name=slist[0].split('="')[1]
	stock_id = slist[0].split('="')[0][-8:]
	yesterdayendprice=slist[2]
	todaystartprice=slist[1]
	nowprice=slist[3]
	if todaystartprice.startswith('0.0') :
		return
 	upgraderate=(float(nowprice)-float(todaystartprice))/float(todaystartprice)
	upgraderate= upgraderate * 100
	dateandtime=slist[30] + ' ' + slist[31]        
	if not os.path.exists('./data'):
		os.makedirs('./data')
	file_name = './data/' + stock_id + '.info'
	file_exist = 0
	if os.path.exists(file_name):
		file_exist = 1
	
	fp = open(file_name, 'a')
	if file_exist == 0:
        	title = "名称          股票代码          昨天收盘价          开盘价          目前价          涨跌率          时 间\n" 
		fp.write(title)
	string = "%-10s%-18s%-20s%-16s%-16s%-16s%-14s\n"%(name, stock_id, yesterdayendprice, todaystartprice, nowprice, str(upgraderate), dateandtime)
	fp.write(string)
	fp.close

'''
获取股票信息
'''
def GetStockInfo(num):
	url_info = url + str(num)
	string=GetStockStrByUrl(url_info)
	if len(string) < 32:
		return
	strGB=ToGB(string)
	ParseResultStr(strGB)

'''
主控函数
'''
def Main():
	if os.path.exists('./All_stock_id.txt'):
		fp = open('./All_stock_id.txt', 'r')
		all_stock_id_info = fp.readlines()
		fp.close()
	else:
		print "Error: All_stock_id.txt  is not exist!"
		sys.exit(1)
	
	'''
	多线程处理
	'''
	threads = []
	for stock in all_stock_id_info:
		stock = stock.strip().split()
		thr = Thread(target=GetStockInfo, args=[stock[0],])
		time.sleep(0.03)
		thr.start()
		threads.append(thr)
	for index in threads:
		index.join()


if __name__ == "__main__":
	while True:
		hour = time.strftime('%H',time.localtime(time.time()))
		if int(hour) > 8 and int(hour) < 16:
			Main()
			time.sleep(60)
		else:
			Main()
			time.sleep(3600)


