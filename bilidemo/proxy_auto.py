import requests
import random


def zhima_proxy():
    targetUrl = "http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=&city=0&yys=0&port=12&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
    while True:
        pro_data = eval(requests.get(targetUrl).text)
        if pro_data['code'] == 0:
            break
    # ����������
    proxyHost = pro_data['data'][0]['ip']
    proxyPort = pro_data['data'][0]['port']
    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    return (proxies)


def jg_proxy():
    proxy_host = 'tunnel.alicloudecs.com'
    # ͨ������Ʒ����-��������-������������ȡ�˿ں�
    proxy_port = 500
    # proxy_username = 'dwadwa'  # (��Ʒ����-������&������֤-�û���/���� ��ȡ)
    # proxy_pwd = 'dwadwa'  # (��Ʒ����-������&������֤-�û���/���� ��ȡ)

    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
    }
    proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
    }
    return proxies

def xsy_proxy():
    proxy_host = 'dynamic.xingsudaili.com'
    # ͨ������Ʒ����-��������-������������ȡ�˿ں�
    proxy_port = 10010
    proxy_username = 'dwadwa'  # (��Ʒ����-������&������֤-�û���/���� ��ȡ)
    proxy_pwd = 'dwadwa'  # (��Ʒ����-������&������֤-�û���/���� ��ȡ)

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_username,
        "pass": proxy_pwd,
    }
    proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
    }
    return proxies



def auto_proxy_():
    ips_ =['http://117.44.31.125:4212',
     'http://117.44.26.85:4212',
     'http://117.43.214.134:4214',
     'http://117.43.212.207:4212',
     'http://111.74.63.73:4212',
     'http://115.150.34.18:4212',
     'http://117.43.213.177:4212',
     'http://182.99.128.137:4214',
     'http://115.150.34.110:4230',
     'http://218.64.198.150:4214',
     'http://117.43.212.210:4212',
     'http://218.64.197.192:4231',
     'http://182.84.154.49:4230',
     'http://117.44.43.208:4212',
     'http://182.99.128.220:4214',
     'http://218.64.196.19:4214',
     'http://117.44.27.181:4230',
     'http://59.55.7.155:4230',
     'http://182.107.232.121:4231',
     'http://117.43.213.23:4214']
    return random.choice(ips_)


def auto_proxy():
    ips = [{'http': 'http://112.194.42.140:1133'},
           {'http': 'http://114.99.3.227:3256'},
           {'http': 'http://115.206.110.180:8060'},
           {'http': 'http://123.171.42.178:3256'},
           {'http': 'http://117.94.222.112:3256'},
           {'http': 'http://111.72.25.205:3256'},
           {'http': 'http://121.232.148.21:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://111.177.192.79:3256'},
           {'http': 'http://111.72.25.40:3256'},
           {'http': 'http://27.208.94.176:8060'},
           {'http': 'http://117.94.222.80:3256'},
           {'http': 'http://121.230.211.212:3256'},
           {'http': 'http://106.45.104.69:3256'},
           {'http': 'http://121.230.211.142:3256'},
           {'http': 'http://27.208.94.176:8060'},
           {'http': 'http://111.77.112.188:3256'},
           {'http': 'http://115.226.146.124:8888'},
           {'http': 'http://202.109.157.63:9000'},
           {'http': 'http://175.7.199.100:3256'},
           {'http': 'http://182.84.144.167:3256'},
           {'http': 'http://121.230.210.9:3256'},
           {'http': 'http://163.125.220.82:8118'},
           {'http': 'http://111.72.25.204:3256'},
           {'http': 'http://182.84.145.187:3256'},
           {'http': 'http://113.123.0.151:3256'},
           {'http': 'http://121.230.210.211:3256'},
           {'http': 'http://115.226.146.124:8888'},
           {'http': 'http://115.226.146.124:8888'},
           {'http': 'http://121.237.106.24:3000'},
           {'http': 'http://121.237.106.24:3000'},
           {'http': 'http://163.125.220.18:8118'},
           {'http': 'http://121.226.21.115:3256'},
           {'http': 'http://39.96.25.191:8090'},
           {'http': 'http://111.72.25.73:3256'},
           {'http': 'http://106.45.104.151:3256'},
           {'http': 'http://121.232.148.229:3256'},
           {'http': 'http://163.125.220.158:8118'},
           {'http': 'http://121.230.210.119:3256'},
           {'http': 'http://182.84.144.254:3256'},
           {'http': 'http://180.122.147.114:3000'},
           {'http': 'http://117.69.230.143:3256'},
           {'http': 'http://117.35.254.214:3000'},
           {'http': 'http://106.45.104.164:3256'},
           {'http': 'http://117.65.1.54:3256'},
           {'http': 'http://117.94.222.83:3256'},
           {'http': 'http://121.232.148.248:3256'},
           {'http': 'http://182.84.145.223:3256'},
           {'http': 'http://111.225.153.218:3256'},
           {'http': 'http://117.69.230.85:3256'},
           {'http': 'http://121.232.148.103:3256'},
           {'http': 'http://117.35.254.5:3000'},
           {'http': 'http://112.195.240.246:3256'},
           {'http': 'http://123.171.42.199:3256'},
           {'http': 'http://39.96.25.191:8090'},
           {'http': 'http://123.171.42.190:3256'},
           {'http': 'http://111.225.153.144:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://117.69.230.41:3256'},
           {'http': 'http://115.209.75.183:3000'},
           {'http': 'http://115.209.75.183:3000'},
           {'http': 'http://117.94.222.177:3256'},
           {'http': 'http://114.98.114.245:3256'},
           {'http': 'http://47.104.15.198:80'},
           {'http': 'http://106.45.104.61:3256'},
           {'http': 'http://140.255.139.120:3256'},
           {'http': 'http://113.123.0.123:3256'},
           {'http': 'http://111.72.25.103:3256'},
           {'http': 'http://114.99.3.146:3256'},
           {'http': 'http://163.125.28.39:8118'},
           {'http': 'http://125.87.95.64:3256'},
           {'http': 'http://111.225.153.99:3256'},
           {'http': 'http://180.122.148.50:3000'},
           {'http': 'http://117.94.180.36:3000'},
           {'http': 'http://123.171.42.73:3256'},
           {'http': 'http://121.232.148.29:3256'},
           {'http': 'http://163.125.250.210:8118'},
           {'http': 'http://121.232.148.53:3256'},
           {'http': 'http://117.94.222.176:3256'},
           {'http': 'http://219.159.38.198:56210'},
           {'http': 'http://111.77.113.181:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://113.124.87.238:9999'},
           {'http': 'http://123.171.42.215:3256'},
           {'http': 'http://106.45.105.58:3256'},
           {'http': 'http://139.155.41.15:8118'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://47.75.132.50:8118'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://182.87.138.19:3256'},
           {'http': 'http://117.94.222.181:3256'},
           {'http': 'http://27.150.87.12:3256'},
           {'http': 'http://114.103.139.68:3256'},
           {'http': 'http://123.171.42.197:3256'},
           {'http': 'http://123.171.42.177:3256'},
           {'http': 'http://112.195.242.233:3256'},
           {'http': 'http://111.72.25.174:3256'},
           {'http': 'http://222.66.202.6:80'},
           {'http': 'http://106.45.104.214:3256'},
           {'http': 'http://117.69.230.125:3256'},
           {'http': 'http://125.72.106.160:3256'},
           {'http': 'http://123.171.42.127:3256'},
           {'http': 'http://117.94.222.176:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://218.86.23.149:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://121.226.21.161:3256'},
           {'http': 'http://111.77.112.111:3256'},
           {'http': 'http://118.117.189.37:3256'},
           {'http': 'http://182.84.144.212:3256'},
           {'http': 'http://122.234.90.166:9000'},
           {'http': 'http://112.95.24.237:8118'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://106.45.105.194:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://182.34.16.222:9999'},
           {'http': 'http://175.7.199.172:3256'},
           {'http': 'http://123.171.42.190:3256'},
           {'http': 'http://114.103.139.229:3256'},
           {'http': 'http://140.255.139.93:3256'},
           {'http': 'http://121.232.148.71:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://182.84.144.61:3256'},
           {'http': 'http://223.113.89.138:808'},
           {'http': 'http://123.171.42.120:3256'},
           {'http': 'http://59.55.160.253:3256'},
           {'http': 'http://125.72.106.195:3256'},
           {'http': 'http://114.98.114.25:3256'},
           {'http': 'http://117.24.81.159:3256'},
           {'http': 'http://118.117.188.71:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://117.69.230.165:3256'},
           {'http': 'http://223.241.118.6:1133'},
           {'http': 'http://101.132.170.11:8080'},
           {'http': 'http://59.55.162.122:3256'},
           {'http': 'http://60.168.80.200:1133'},
           {'http': 'http://114.103.139.130:3256'},
           {'http': 'http://111.77.112.147:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://111.77.112.72:3256'},
           {'http': 'http://117.94.222.176:3256'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://117.64.224.143:1133'},
           {'http': 'http://101.200.127.149:3129'},
           {'http': 'http://59.55.162.4:3256'},
           {'http': 'http://180.122.147.76:3000'},
           {'http': 'http://219.159.38.198:56210'},
           {'http': 'http://114.230.107.102:3256'},
           {'http': 'http://121.230.211.163:3256'}]
    return random.choice(ips)