#!/usr/bin/env python3
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
import time
import re


class TopsecReport(object):
    def __init__(self, context, template='topsec_report_tpl.docx'):
        self.doc = DocxTemplate(template)
        context['bugs'] = self.bugs_clear(context['bugs'])
        jinja_env = jinja2.Environment()
        jinja_env.filters['eval'] = lambda x:eval(x)
        self.doc.render(context,jinja_env)

    def save(self, path):
        self.doc.save(path)

    def parse_xml(self, value):
        result = []
        text  = re.compile(r'<p>(.*?)</p>')
        #image = re.compile(r'<img src="\./upload\.php\?fid=([a-z\d]{8}(?:-[a-z\d]{4}){3}-[a-z\d]{12})"')
        # test code
        image = re.compile(r'<img src="\./upload\.php\?fid=(.+?)"')
        for s in text.finditer(value):
            img = image.search(s[0])
            if img:
                img_obj = InlineImage(self.doc, img[1], width=Mm(170))
                result.append(img_obj)
            else:
                result.append(s[1])
        return result

    def del_tag(self, s, tag):
        s = re.sub(r'<{0}.*?>(.*?)</{0}>'.format(tag), '', s)
        s = re.sub(r'<{0}.*?>'.format(tag), '', s)
        return s

    def bugs_clear(self, bugs, clear_keys=['bugreq'], filter_tags=['br']):
        for i, bug in enumerate(bugs, 1):
            bug['num'] = str(i)
            for key, value in bug.items():
                if key in clear_keys:
                    for tag in filter_tags:
                        value = self.del_tag(value, tag)
                    bug[key] = self.parse_xml(value)
        return bugs


if __name__ == '__main__':
    buglist = []
    buglist.append({
        'bugname':'sql注入',
        'bugrank':'高危',
        'bugaddr':'http://127.0.0.1/addr?sa=1',
        'bugreq': '''<p>asdasdasdasdsadasdasdasdadf</p><p><br></p><p>ddfdsfsdfs</p><p><br></p><p>sddfsdfsdf</p>''',
        #'bugreq':[['text', 'test text'], ['img', '1.png'], ['text', 'test text 2'], ['img', '1']],
        'bugres':'resresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresres',
        'bugdesc':'descdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdesc',
        'bugplan':'planplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplan',
        'bugnumber':'cve-2017-12345|cnvd-2017-1234',
        'bugowasp':'A7:2017-跨站脚本(XSS)',
        'bugtag':'sdfsdfsd',
        'bugnote':'sdfsdf',
    })
    buglist.append({
        'bugname':'存储XSS',
        'bugrank':'高危',
        'bugaddr':'http://666.0.0.1/addr?sa=1',
        'bugreq': '''<p>asdasdasdasdsadasdasdasdadf</p><p></p><p>ddfdsfsdfs</p><p><br></p><p>sddfsdfsdf</p>''',
        'bugen':'enenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenenen',
        'bugres':'resresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresres',
        'bugdesc':'descdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdesc',
        'bugplan':'planplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplan',
        'bugnumber':'cve-2017-12345|cnvd-2017-1234',
        'bugowasp':'A7:2017-跨站脚本(XSS)',
        'bugtag':'sdfsdfsd',
        'bugnote':'sdfsdf'
    })

    buglist.append({
        'bugname':'sql注入',
        'bugrank':'高危',
        'bugaddr':'http://127.0.0.1/addr?sa=1',
        'bugreq': '''<p>asdasdasdasdsadasdasdasdadf</p><br></p><p>ddfdsfsdfs</p><p><br></p><p>sddfsdfsdf</p>''',
        'bugres':'resresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresresres',
        'bugdesc':'descdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdescdesc',
        'bugplan':'planplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplanplan',
        'bugnumber':'cve-2017-12345|cnvd-2017-1234',
        'bugowasp':'A7:2017-跨站脚本(XSS)',
        'bugtag':'sdfsdfsd',
        'bugnote':'sdfsdf'
    })

    date = time.strftime('%Y-%m-%d', time.localtime())
    user = 'TWELVE'
    revision = [
        {'version': '1.0', 'date': date, 'user': user, 'spec': '创建'},
        {'version': '2.0', 'date': date, 'user': 'user2', 'spec': '修改'},
    ]
    fields = [
        {'num': 1, 'host': 'http://github.com', 'note': 'autoreport脚本测试'},
        {'num': 2, 'host': 'www.topsec.com.cn', 'note': 'ceshi'}
    ]
    context = {
            'name': '妇产科系统',
            'user': 'TWELVE',
        'revision': revision,
          'fields': fields,
            'date': date,
            'bugs': buglist
    }
    project = TopsecReport(context)
    project.save('report.docx')
