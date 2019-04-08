# author L
# date 2017-08-16
try:
    from bs4 import BeautifulSoup
except:
    print('pip3 install beautifulsoup4')
from collections import OrderedDict
import re, os

columns_head = ('漏洞等级', '主机IP', '端口', '协议', '服务', '漏洞名称')
columns_tail = ('漏洞描述', '解决方案', '威胁分值', 'NSFOCUS', 'CVE编号', 'BUGTRAQ', 'CNNVD编号', 'CVSS评分', 'CNVD编号') 
columns_tail_default_list = tuple(zip(columns_tail, [''] * len(columns_tail)))
ip_re = re.compile(r'(?s)<td>IP地址</td><td>(.*?)</td>')
info_head = re.compile('<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>')


def return_level(string):
    levels = {'l':'low', 'm':'middle', 'h':'high'}
    return levels[string[-1]]


def scan_vulns(detail_table):
    clear_re = re.compile(r'\S+')
    vulns_detail_map = dict()
    for tbody in detail_table.findAll('tbody', {'class':'lt'}):
        vuln_id = tbody.tr.a.get('name')
        infos = OrderedDict(columns_tail_default_list)
        for item in tbody.findAll('tr', class_='odd'):
            key = item.th.get_text()
            value = item.td.get_text().strip().replace(',', '，')
            if key in infos:
                if key in ('漏洞描述', '解决方案'):
                    value = ''.join(clear_re.findall(value))
                infos[key] = value
        vulns_detail_map[vuln_id] = ','.join(infos.values())
    return vulns_detail_map


def scan(filename):
    try:
        with open(filename, encoding='utf8') as f:
            data = f.read()
        bsObj = BeautifulSoup(data, 'html.parser')
        vuln_list = bsObj.find('table', {'class':"cmn_table", 'style':"word-wrap:break-word;word-break:break-all;"})
        vuln_detail = bsObj.find('h3', {'id':'vulSolution'}).next_element.next_element.next_element
        vuln_detail_map = scan_vulns(vuln_detail)
        
        with open('report.csv', 'a') as f:
            vuln_lambda = lambda tag: tag.name=='a' and tag.get('href').startswith('#tag')
            ip = ip_re.search(data).group(1)
            for tr in vuln_list.findAll('tr')[2:]:
                tr_text = tr.prettify().replace('\n ', '')
                port, protocol, server = info_head.search(tr_text).groups()
                for vuln in tr.findAll(vuln_lambda):
                    level = return_level(vuln.get('class')[0])
                    vuln_name = vuln.get_text()
                    vuln_id = vuln.get('href')[1:]
                    record = (level, ip, port, protocol, server, vuln_name, vuln_detail_map[vuln_id])
                    f.write(','.join(record) + '\n')
    except Exception as e:
        print(filename, e)


def main():
    with open('report.csv', 'w') as f:
        f.write(','.join(columns_head + columns_tail)+'\n')
    for filename in os.listdir():
        if filename.endswith('.html'):
            scan(filename)


if __name__ == '__main__':
    main()
