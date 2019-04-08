#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt

#os.getdefaultcoding
#??????
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


#??????
def file_conuting(file):
	global all_file_line_num
	global file_num
	global all_file_size

	file_size = 0
	file_size = os.path.getsize(file)
	#print '??????§³??{0}'.format(file_size)
	all_file_size = all_file_size + file_size


	file_num = file_num+1
	#print '????????????:'+file
	file_line_num = 0
	with open(file) as f:
		for line in f.readlines():
			if line.strip() != '':
				file_line_num = file_line_num+1
	#print '????????????????(???????):'+str(file_line_num)
	all_file_line_num = all_file_line_num+file_line_num

#??????¡¤??
pwd = os.getcwd()
print "???¡¤???:{0}".format(pwd)
#??????????
num = 1
print '??????¦Ì????:'
for dir in os.listdir(pwd):
	print '[*]'+dir
print '+++++++++++++++++++++++++++'
#???????

for parent,dirnames,filenames in os.walk(pwd):
	for filename in filenames:
		#print '-----------------------'
		#print '??????:'+parent
		#print '???????:'+filename

		if filename.endswith(ext_no_cout):
			print '??????:'+filename
			continue
		file_which_for_count.append(os.path.join(parent,filename))
		#print '????????:'+str(file_which_for_count)


		#print '??????¡¤????:'+os.path.join(parent,filename)
		#print '-----------------------'
'''
#????????
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



#????????
for file in  file_which_for_count:
	#print '==================================='
	#print file
	file_conuting(file)


print '#################################'
print '?????:'
print '[*]??????(??????????????????§³?):'+str(all_file_line_num)
print '[*]?????:'+str(file_num)
r_num = all_file_size
print '[*]?????§³:'+str(r_num)+'Bytes'
r_num_k = all_file_size/1024.0
print '[*]?????§³KB:'+str(r_num_k)
r_num_m = r_num_k/1024.0
print '[*]?????§³MB:'+str(r_num_m)
r_num_g = r_num_m/1024.0
print  '[*]?????§³GB:'+str(r_num_g)
'''
xls=xlwt.Workbook()
xls.tab_width=4
sheet = xls.add_sheet("Sheet1")
sheet.write(0,0,u'??????')
sheet.write(0,0,u'??????(??????????????????§³?)')

xls.save('out.xls')
'''

os.system('pause')








