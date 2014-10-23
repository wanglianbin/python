#!/usr/bin/python
#encoding:utf-8
import urllib2
import string
import os
import sys
from multiprocessing import Process


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
def ParseResultStr(resultstr, stock_name):
	slist=resultstr.split(',')
	name=stock_name
	yesterdayendprice=slist[2]
	todaystartprice=slist[1]
	nowprice=slist[3]
 	upgraderate=(float(nowprice)-float(yesterdayendprice))/float(yesterdayendprice)
	upgraderate= upgraderate * 100
	dateandtime=slist[30] + ' ' + slist[31]        
	print'*******************************'
	print'name is :%s'%name
	print'yesterday end price is :%s'%yesterdayendprice
	print'today start price is :%s'%todaystartprice
	print'now price is :%s'%nowprice
	print'upgrade rate is :%s%s'%(upgraderate, '%')
	print'date and time is :%s'%dateandtime
	print'*******************************'

'''
获取股票信息
'''
def GetStockInfo(num, name):
	url_info = url + str(num)
	string=GetStockStrByUrl(url_info)
	if len(string) < 32:
		return
	strGB=ToGB(string)
	ParseResultStr(strGB, name)

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
	多进程处理
	'''
	mul_jobs = []
	for stock in all_stock_id_info:
		stock = stock.strip().split()
		proc = Process(target=GetStockInfo,args=(stock[0], stock[1]))
		mul_jobs.append(proc)
		proc.start()
	for jobs in mul_jobs:
		jobs.join()

if __name__ == "__main__":
	Main()
