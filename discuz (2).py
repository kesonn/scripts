#coding=utf8

class BasePlugin(object):
    filters = {
        'filter_system' : None     #操作系统
        'filter_version' : None    #版本信息
        'filter_port' : None       #默认端口
    }
    def __init__(self):
        vul_type = 'bin'    #bin | web
        vul_name = ''       #漏洞名称
        vul_tag = ''        #漏洞标签
        vul_level = '低'    #漏洞等级
        vul_desc = ''       #漏洞描述
        vul_solution = ''   #修复建议

        plugin_every = True #是否匹配每个url


    @property
    def port(self):
        return self.port

    @port.getter
    def port(self,port):
        self.port = port

    def filter(self):
        if self.type == 'bin':
            pass






class Discuz(BasePlugin):
    '''
    当漏洞类型为bin时传入主机和端口
      漏洞类型为web时：
        如果所有url都匹配则传入请求包
        否则传入url地址
    '''
    def test(self,req):
        pass

class BaseHostVul(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port

class BaseAppsVul(object):
    def __init__(self,url):
        self.url = url
