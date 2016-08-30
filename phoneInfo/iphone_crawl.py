#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from multiprocessing import Pool
def getUrlOfPage():
    urlPages=[]
    url_title="http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_"
    for page in xrange(1,50):
        url=url_title+str(page)+".html"
        urlPages.append(url)
    return urlPages

def getUrlOfPhoneParam(pageurl):
    # urlp="http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_1.html"
    urlPrefix="http://detail.zol.com.cn/"
    pageNum=pageurl.split(".")[3].split("_")[-1]
    urlCont=BeautifulSoup(urllib2.urlopen(pageurl))
    urlsReviews=urlCont.find(id="J_PicMode").find_all('a',class_="comment-num")
    ##href=/403/402871/review.shtml
    UrlsPage=[]
    for review in urlsReviews:
        paramUrl=urlPrefix+review['href'][:-12]+"param.shtml"
        UrlsPage.append(paramUrl)
    print "This  is "+pageNum+" page running"

    return UrlsPage

def getParam(urlparam):
    try:
        paramWeb=BeautifulSoup(urllib2.urlopen(urlparam))
        phoneName = paramWeb.find('h1', id="page-title").string+'\t\t'
        params= paramWeb.find("div",id="newTb").text.replace(u"纠错","")
        paralist=[line for line in params.split('\n\n') if len(line.strip()) > 4]
        phoneInfo  = phoneName + "\t".join(paralist[:-6])+'\t\t\t'
    except Exception as e:
        phoneInfo=""
        print e
    to_txt(phoneInfo.encode('utf-8'))  ########



def to_txt(str):
    with open("phoneInfo.txt","a+") as ph:
        ph.write(str)
def mapPageUrl(pageurl):

    UrlsPage=getUrlOfPhoneParam(pageurl)
    map(getParam,UrlsPage)


def main():
    Pages=getUrlOfPage()
    # urlparams=[]
    # for pageUrl  in Pages:
    #     urlparams.extend(getUrlOfPhoneParam(pageUrl))
    pool=Pool(6)
    pool.map(mapPageUrl,Pages)
    pool.close()
    pool.join()

if __name__=="__main__":
    main()



