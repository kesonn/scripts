import re
import ipaddress

def gethosts(hosts):
    result = []
    hosts = hosts.replace(' ', '')
    if re.search('[a-z]',hosts,re.I):
        hosts = hosts if '://' in hosts else 'http://%s'%hosts
        h = gethostbyname(getdomain(hosts))
        if h:result.append(h)
    else:
        if '/' in hosts:
            result = [str(i) for i in list(ipaddress.IPv4Network(hosts,False).hosts())]
        elif '-' in hosts:
            ret = []
            hosts = hosts.split('-')
            h = hosts[0].split('.')
            for i in range(int(h[3]),int(hosts[1])+1):
                h[3] = str(i)
                ret.append('.'.join(h))
            result = ret
        else:
            result = [hosts] if hosts else []
    return result




for i in gethosts('47.1.1.1-47'):
    print(i)