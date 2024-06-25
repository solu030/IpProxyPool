import requests,time
import Spider
import config,mysql

def test_ip(ip):
    proxy = get_proxy(ip)
    head = config.get_header()
    try:
        req = requests.get(url=config.TEST_IP, headers=head,proxies=proxy,timeout=config.SHORT_TIMEOUT)  #访问失败会停止程序报错
        if req.status_code != 200:
            return False
        # proxy_ip = Spider.par_ip(requests.get(url=config.GET_IP, headers=head,proxies=proxy))
        # if proxy_ip not in config.LOCAL_IP:
        #     return True   #高匿代理 免费的很少而且我们没有需求
        return True
    except Exception as e:
        print(ip + "访问失败!")
        return False

def get_proxy(ip):
    proxy = {
        'http': 'http://{}'.format(ip),
        'https': 'https://{}'.format(ip),
    }
    return proxy

def test_main():
    while True:
        ip_count = mysql.ip_count()
        if ip_count <= config.TEST_IP_NUM:     #数据库数据少，等待
            time.sleep(config.TIME_OUT)
            continue
        for i in range(config.TEST_IP_NUM):
            ip = mysql.get_random()        #随机取出ip进行测试
            if not ip:
                continue
            if not test_ip(ip):
                mysql.dec_score(ip)     #返回False则不可用，减分
            else:
                mysql.add_score(ip)
            score = mysql.get_score(ip)      #获取score进行删除或设置上限
            if not score:
                continue
            elif score > config.MAX_SCORE:
                mysql.set_max(ip)
            elif score <=0:
                mysql.delete_ip(ip)



if __name__ == '__main__':
    # test_main()
    ip = '218.87.205.185:16388'
    proxy = get_proxy(ip)
    head = config.get_header()
    req = requests.get(url=config.TEST_IP, headers=head,timeout=5,proxies=proxy)  #访问失败会停止程序报错
    for i in req:
        print(req.text)