import requests
import config,mysql
from lxml import etree
# from app01.models import IpModel  导出app会报错
def par_ip(req):
    et = etree.HTML(req.text)
    ip = et.xpath('//*')[2].text
    ip = ip.split(":")[1].split('"')[1]
    print(ip)
    return ip

def save_ip():
   parser_list = config.parserList
   for parser in parser_list:
       url_list = parser.get('urls')
       for url in url_list :
           head = config.get_header()
           req = requests.get(url,headers=head)
           # req.encoding = config
           et = etree.HTML(req.text)
           proxies = et.xpath(parser['pattern_proxy'])
           # print(proxies[3].text)
           proxy_list = []
           for proxy in proxies:
               proxy = proxy.text
               if proxy is None:
                   continue
               if proxy_list and len(proxy) < 10:
                  proxy_list[len(proxy_list)-1] = proxy_list[len(proxy_list)-1] + ":" + proxy
                  continue
               proxy_list.append(proxy)

           # for i in proxy_list:
           #     IpModel.objects.create(ip=i) django不让用orm
           for i in proxy_list:
               if not i or config.IP_COUNT >= config.MAX_IP:
                   continue
               mysql.insert_ip(i)                #在这里用python写入数据库
               config.IP_COUNT += 1

if __name__ == '__main__':
    save_ip()
    # parser_list = config.parserList
    # url_list = parser_list[1].get('urls')
    # url = url_list[0]
    # head = config.get_header()
    # req = requests.get(url, headers=head)
    # et = etree.HTML(req.text)
    # proxies = et.xpath(parser_list[1]['pattern_proxy'])
    # for proxy in proxies:
    #     proxy = proxy.text
    #     print(proxy)


