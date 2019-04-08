#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt

#os.getdefaultcoding
#变量区
dir = ""
file_num = 0
'''
ext_which_for_count = ('.h','.vb','.sh','.cs','.cpp','.sql',
	'inc','.rc','.java','.cls','.htm','.c','.tli','.php','.asp','.hh',
	'.txt','.aspx','.jsp','.cc','.php3','.ctl','.pas','.tlh',
	'.frm','.hpp','.html','.properties','.cxx')
'''
ext_no_cout = ('.rar','.zip','.7z')

file_which_for_count = []

all_file_line_num = 0

file_num = 0

#file_size = 0

all_file_size = 0


#统计函数
def file_conuting(file):
	global all_file_line_num
	global file_num
	global all_file_size
	
	file_size = 0
	file_size = os.path.getsize(file)
	#print '文件的大小是{0}'.format(file_size)
	all_file_size = all_file_size + file_size
	
	
	file_num = file_num+1
	#print '当前统计的文件是:'+file
	file_line_num = 0
	with open(file) as f:
		for line in f.readlines():
			if line.strip() != '':
				file_line_num = file_line_num+1
	#print '当前统计的文件行数是(除去空行):'+str(file_line_num)
	all_file_line_num = all_file_line_num+file_line_num

#得到当前路径
pwd = os.getcwd()
print "当前路径为:{0}".format(pwd)
#当前目录文件夹
num = 1
print '当前目录下的文件:'
for dir in os.listdir(pwd):
	print '[*]'+dir
print '+++++++++++++++++++++++++++'
#遍历文件

for parent,dirnames,filenames in os.walk(pwd):
	for filename in filenames:
		#print '-----------------------'
		#print '父目录是:'+parent
		#print '文件名是:'+filename
		
		if filename.endswith(ext_no_cout):
			print '压缩文件:'+filename
			continue
		file_which_for_count.append(os.path.join(parent,filename))
		#print '要统计的文件:'+str(file_which_for_count)
		
		
		#print '文件的全路径是:'+os.path.join(parent,filename)
		#print '-----------------------'
'''
#要统计的文件
jsp = 0
htm = 0
properties = 0
html = 0
txt = 0
for file in  file_which_for_count:

	
	if file.endswith('.jsp'):
		jsp = jsp+1
		
	if file.endswith('.htm'):
		htm = htm+1
	if file.endswith('.html'):
		html = html+1
		
print 'jsp:'+str(jsp)
print 'htm:'+str(htm)
'''

	
	
#要统计的文件
for file in  file_which_for_count:
	#print '==================================='
	#print file
	file_conuting(file)
	

print '#################################'
print '统计结果:'
print '[*]代码量(代码总行数【除去空行】):'+str(all_file_line_num)
print '[*]文件数:'+str(file_num)
r_num = all_file_size
print '[*]文件大小:'+str(r_num)+'Bytes'
r_num_k = all_file_size/1024.0
print '[*]文件大小KB:'+str(r_num_k)
r_num_m = r_num_k/1024.0
print '[*]文件大小MB:'+str(r_num_m)
r_num_g = r_num_m/1024.0
print  '[*]文件大小GB:'+str(r_num_g)
'''
xls=xlwt.Workbook()
xls.tab_width=4
sheet = xls.add_sheet("Sheet1")
sheet.write(0,0,u'系统名称')
sheet.write(0,0,u'代码量(代码总行数【除去空行】)')

xls.save('out.xls')
'''

os.system('pause')



	
	

			

