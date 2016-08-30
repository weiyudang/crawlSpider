##手机参数爬虫信息说明
>- 程序及说明
该爬虫是对[中关村在线](http://www.zol.com.cn/)的手机参数信息进行爬取。具体代码见iphone_crawl.py
> - iphone_crawl.py 通过6个函数实现对中关村在线手机信息的爬取
>getUrlOfPage()：该函数构建手机网页页码信息
>getUrlOfPhoneParam（）：该函数通过页码信息构造出参数页面网址
>getParam（）：获取手机参数信息并保存
>to_txt（）：写入txt文件
>mapPageUrl（）为多线程而构造的函数
>main() 为主函数

> - 文件分割说明：
>单个手机之间分割符号"\t\t\t",手机名称与手机参数分割符号为"\t\t",参数与参数之间分割符号为”\t".分割程序实例如下（python):



    phoneInfo=open("phoneInfo.txt").read().split('\t\t\t')
    for phone in phoneInfo[:10]:
        infoTemp=phone.split('\t\t')
        phoneBrand=infoTemp[0]
        phoneInfo=infoTemp[1].split("\t")[1:]
        print phoneInfo[0]