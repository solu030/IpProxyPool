import os
import time
import django
import Spider,mysql,test
from multiprocessing import Process
import config
# import threading

def clear():
    # IpModel.objects.all().delete()
    mysql.delete_all()
    config.IP_COUNT = 0
def run_web():
    clear()     #免费ip不具有时效性
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip代理池.settings')
    # django.setup()
    os.system('python manage.py runserver 127.0.0.1:8000')
    print("接口完成启动!")
def ip_test():  #测试ip并更改分数或删除
    test.test_main()
def ip_save():    #爬取ip并save 只爬取所有ip一次
    Spider.save_ip()

if __name__ == '__main__':
    p1 = Process(target=run_web)
    p1.start()
    time.sleep(config.SHORT_TIMEOUT) #save test依赖django项目的运行,优先启动django 并清空ip表
    p2 = Process(target=ip_save)
    p2.start()
    test_list = []
    for i in range(config.TEST_NUM):
        p = Process(target=ip_test)
        p.start()
        test_list.append(p)
    p2.join()
    for p in test_list:
        p.join()        #主进程等待所有子进程
    p1.join()       #阻断主进程


    # t1 = threading.Thread(target=run_web)
    # t1.start()
    # t2 = threading.Thread(target=ip_save)
    # t2.start()

