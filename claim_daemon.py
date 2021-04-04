import requests,logging
import sys
import os


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler("healthcheck.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def __getpid(pid):
    pass

def __killpid(pid):
    pass

def __restart():
    pass

def __checkclaim2webstatus():
    url='https://brilliantlife.com.cn:8016/admin/login/?next=/admin/'
    code = 0
    try:
        r=requests.get(url,timeout=5)
        # 获取访问claim2.0网站状态
        code = r.status_code
    except:
        logger.info("网站访问异常无法获取code码")
    # 获取clam2.0进程pid
    pid_list = os.popen("ps -ef |grep 8016|grep python |grep -v grep|awk '{print $2}'").readlines()
    if code == 200:
        logger.info('OK Claim2.0网站访问正常')
    else:
        logger.info("claim2.0 网站访问异常，杀掉claim2.0后台进程")
        for pid in pid_list:
            print ("该次脚本进程为 %s " % (os.getpid()))
            if int(pid) != int(os.getpid()):
                logger.info("杀掉claim2.0进程 %s" % (pid.replace("\n", "")))
                os.system("kill -9 %s" % (pid.replace("\n", "")))
        logger.info("重启claim2.0")
        os.popen("nohup python /opt/production/claim2.0/server/manage.py runserver_plus --cert /home/ssl/server.crt 0.0.0.0:8016 >> /opt/production/claim2.0/server/output.log 2>&1 &")

def __checkclaimwebstatus():
    url='https://brilliantlife.com.cn:8015/admin/login/?next=/admin/'
    code = 0
    try:
        r=requests.get(url,timeout=5)
        # 获取访问claim2.0网站状态
        code = r.status_code
    except:
        logger.info("网站访问异常无法获取code码")
    # 获取clam2.0进程pid
    pid_list = os.popen("ps -ef |grep 8015|grep python |grep -v grep|awk '{print $2}'").readlines()
    if code == 200:
        logger.info('OK claim1.0网站访问正常')
    else:
        logger.info("claim1.0 网站访问异常，杀掉claim1.0后台进程")
        for pid in pid_list:
            print ("该次脚本进程为 %s " % (os.getpid()))
            if int(pid) != int(os.getpid()):
                logger.info("杀掉claim1.0进程 %s" % (pid.replace("\n", "")))
                os.system("kill -9 %s" % (pid.replace("\n", "")))
        logger.info("重启claim1.0")
        os.popen("nohup python /opt/production/claim/server/manage.py runserver_plus --cert /home/ssl/server.crt 0.0.0.0:8015 >> /opt/production/claim/server/output.log 2>&1 &")

def __checknginxstatus():
    nginx_pid = os.popen("systemctl status nginx |grep running").readlines()
    if len(nginx_pid) < 1:
        logger.info("nginx 服务异常,重启nginx服务")
        os.popen("systemctl restart nginx")


def main():
    logger.info("===========启动健康检查脚本=============")
    logger.info("===========检查claim2.0================")
    __checkclaim2webstatus()
    logger.info("===========检查claim1.0================")
    __checkclaimwebstatus()
    logger.info("===========检查nginx ================")
    __checknginxstatus()


if __name__ == '__main__':
    main()