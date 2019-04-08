#coding=utf8
# author L
# date 2017-08-14
try:
    from bs4 import BeautifulSoup
except:
    print('pip3 install beautifulsoup4')
from collections import OrderedDict
import re, os

columns_head = ('漏洞等级', '主机IP', '端口', '协议', '服务', '漏洞名称')
columns_tail = ('详细描述', '解决办法', '威胁分值', '危险插件', '发现日期', 'CVE编号', 'NSFOCUS', 'CNNVD编号', 'CNCVE编号', 'CVSS评分', 'CNVD编号')
columns_tail_default_list = tuple(zip(columns_tail, [''] * len(columns_tail)))
ip_re = re.compile(r'(?s)IP地址</th>(?:.*?)<td>(.*?)</td>')


def scan_vulns(detail_table):
    clear_re = re.compile(r'\S+')
    vulns_detail_map = dict()
    for tr in detail_table.findAll('tr', {'class':"solution"}):
        table_id = tr.get('id')
        infos = OrderedDict(columns_tail_default_list)
        for item in tr.findAll('tr'):
            key = item.th.get_text()
            value = item.td.get_text().strip().replace(',', '，')
            if key in infos:
                if key in ('详细描述', '解决办法'):
                    value = ''.join(clear_re.findall(value))
                infos[key] = value
        vulns_detail_map[table_id] = ','.join(infos.values())
    return vulns_detail_map


def scan(filename):
    try:
        with open(filename, encoding='utf8') as f:
            data = f.read()
        bsObj = BeautifulSoup(data, 'html.parser')
        vuln_list = bsObj.find('table', {'id':"vuln_list", 'class':"report_table"}).tbody
        vuln_detail = bsObj.find('div', {'id':'vul_detail'})
        vuln_detail_map = scan_vulns(vuln_detail)

        with open('report.csv', 'a') as f:
            ip = ip_re.search(data).group(1)
            for tr in vuln_list.findAll('tr'):
                items = tr.contents
                port = items[1].get_text()
                protocol = items[3].get_text()
                server = items[5].get_text()
                for span in items[7].findAll('span'):
                    vuln_name = span.get_text()
                    level = span.get('class')[0].split('_')[-1]
                    table_id = span.get('onclick').split('\'')[-2]
                    record = (level, ip, port, protocol, server, vuln_name, vuln_detail_map[table_id])
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


