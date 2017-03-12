#encoding:utf-8
import urllib2
from bs4 import BeautifulSoup
import re
import requests
# import redis
from lxml import html
import pandas as pd
import csv

from multiprocessing.dummy  import Pool
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# values = {'username' : 'cqc',  'password' : 'XXXX' }
headers = {   'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"}
p=re.compile(r'urlToken":"(.*?)",')
num=re.compile('\d+')
def get_user_info(name=None):
    try:
        url='https://www.zhihu.com/people/'+name+'/following'
        req=urllib2.Request(url, headers=headers)
        # print urllib2.urlopen(req).read()
        soup = BeautifulSoup(urllib2.urlopen(req).read())
        t1=soup.find('ul',class_='Tabs ProfileMain-tabs').text
        t2=soup.find('div',class_='Profile-sideColumnItem').text
        t3=soup.find('div',class_='NumberBoard FollowshipCard-counts').text
        t4=soup.find('div',class_='Profile-lightList').text
        file_path='user_data/'+name[:2]+'.csv'
        tt=t1+t2+t3+t4
        info=num.findall(tt)
    except  Exception as e:
        info=None
    pd.DataFrame(info,columns=[name]).T.to_csv(file_path)
# 动态回答52分享0提问25收藏1关注获得 120 次赞同获得 18 次感谢，15 次收藏关注了62关注者114关注的话题137关注的专栏3关注的问题569关注的收藏夹0
# 动态回答52分享0提问25收藏1关注获得 120 次赞同获得 18 次感谢，15 次收藏关注了62关注者114关注的话题137关注的专栏3关注的问题569关注的收藏夹0


def get_singleUser_followings(name):
    name_collect=[]
    url='https://www.zhihu.com/people/'+name+'/following'
    get_html=requests.get(url, headers=headers)
    # print urllib2.urlopen(req).read()
    soup = BeautifulSoup(get_html.text)
    pageNum=soup.findAll('button',class_='Button PaginationButton Button--plain')[-1].text
    for page in range(1,int(pageNum)):
        url='https://www.zhihu.com/people/'+name+'/following/?page='+str(page)
        get_html=requests.get(url, headers=headers)
        # print urllib2.urlopen(req).read()
        soup = BeautifulSoup(get_html.text)
        names=p.findall(str(soup))
        name_collect.extend(names)
    return set(name_collect)

def get_collotins_name(startNode='kaifulee',scale=1000000,name_path='crawled_names.csv'):
    names=get_singleUser_followings(name=startNode)
    collection_name=[]
    crawled_collection=[]
    crawler_nums=0
    while crawler_nums<=scale:
        for line in names:
            try:
                temp=get_singleUser_followings(name=line)
            except Exception as e:
                print e
                continue
            pd.Series(list(temp)).to_csv('meddian.csv',mode='a+c')
            collection_name.extend(temp)
        print "we have crawled numbers:",crawler_nums
        pd.Series(list(names)).to_csv(name_path,mode='a+c')
        crawled_collection.extend(names)
        crawled=set(crawled_collection)
        names=list(set(collection_name)^crawled)
        crawler_nums=len(crawled)
    return True

if __name__=="__main__":
    tokens=pd.read_csv('tokens.csv',index_col=0).values.flatten()
    pool = Pool(8)
    pool.map(get_user_info,tokens)
    pool.close()
    pool.join()
    
    
