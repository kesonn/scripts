#!/usr/bin/env python3
# encoding=utf-8
#codeby     道长且阻
#email      @ydhcui/QQ664284092

import re
import socket
import binascii
import hashlib
import struct
import time
import ftplib

class Host(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port

class MssqlNoAuth(object):
    def verify(self,host,user='sa',pwd='',timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host.host,int(host.port)))
            hh = binascii.b2a_hex(host.host.encode())
            husername = binascii.b2a_hex(user.encode())
            lusername = len(user)
            lpassword = len(pwd)
            ladd = len(host.host)+len(str(host.port))+1
            hladd = hex(ladd).replace('0x','')
            hpwd = binascii.b2a_hex(pwd.encode())
            pp = binascii.b2a_hex(str(host.port).encode())
            address = hh+'3a'.encode()+pp
            hhost = binascii.b2a_hex(host.host.encode())
            data = ("02000200000000001234567890000000"
                    "00000000000000000000000000000000"
                    "000000000000ZZ544000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000X33600000000000000000"
                    "00000000000000000000000000000000"
                    "000000000Y3739333400000000000000"
                    "00000000000000000000000000000000"
                    "000000040301060a0901000000000200"
                    "0000000070796d7373716c0000000000"
                    "00000000000000000000000000000000"
                    "00000712345678900000000000000000"
                    "00000000000000000000000000000000"
                    "00ZZ3360000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "00000000000000000000000000000000"
                    "000Y0402000044422d4c696272617279"
                    "0a00000000000d1175735f656e676c69"
                    "73680000000000000000000000000000"
                    "0201004c000000000000000000000a00"
                    "0000000000000000000000000069736f"
                    "5f310000000000000000000000000000"
                    "00000000000000000000000501353132"
                    "000000030000000000000000").encode()
            data1 = data.replace(data[16:16+len(address)],address)
            data2 = data1.replace(data1[78:78+len(husername)],husername)
            data3 = data2.replace(data2[140:140+len(hpwd)],hpwd)
            if lusername >= 16:
                data4 = data3.replace(b'0X',str(hex(lusername)).replace('0x','').encode())
            else:
                data4 = data3.replace(b'X',str(hex(lusername)).replace('0x','').encode())
            if lpassword >= 16:
                data5 = data4.replace(b'0Y',str(hex(lpassword)).replace('0x','').encode())
            else:
                data5 = data4.replace(b'Y',str(hex(lpassword)).replace('0x','').encode())
            data6 = data5.replace(b'ZZ',str(hex(ladd)).replace('0x', '').encode())
            data7 = binascii.a2b_hex(data6)
            sock.send(data7)
            packet = sock.recv(1024)
            if b'master' in packet:
                self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                self.bugreq = "username:%s,password:%s" % (user,pwd)
                self.bugres = packet
                return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            sock.close()

class MysqlNoAuth(object):
    def verify(self,host,user='root',pwd='root',timeout=10):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host.host,int(host.port)))
            packet = sock.recv(254)
            plugin,scramble = self.get_scramble(packet)
            if not scramble:
                return False
            auth_data = self.get_auth_data(user,pwd,scramble,plugin)
            sock.send(auth_data)
            result = sock.recv(1024)
            if result == b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
                self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                self.bugreq = "username:%s,password:%s" % (user,pwd)
                self.bugres = result
                return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            sock.close()

    def get_hash(self,password, scramble):
        hash_stage1 = hashlib.sha1(password.encode()).digest()
        hash_stage2 = hashlib.sha1(hash_stage1).digest()
        to = hashlib.sha1(scramble+hash_stage2).digest()
        reply = [h1 ^ h3 for (h1, h3) in zip(hash_stage1, to)]
        hash = struct.pack('20B', *reply)
        return hash

    def get_scramble(self,packet):
        scramble,plugin = '',''
        try:
            tmp = packet[15:]
            m = re.findall(b"\x00?([\x01-\x7F]{7,})\x00", tmp)
            if len(m)>3:del m[0]
            scramble = m[0] + m[1]
        except:
            return '',''
        try:
            plugin = m[2]
        except:
            pass
        return plugin,scramble

    def get_auth_data(self,user,password,scramble,plugin):
        user_hex = binascii.b2a_hex(user.encode())
        pass_hex = binascii.b2a_hex(self.get_hash(password,scramble))
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" \
             + user_hex.decode() + "0014" + pass_hex.decode()
        if plugin:
            data += binascii.b2a_hex(plugin).decode() \
                 + "0055035f6f73076f737831302e380c5f" \
                 + "636c69656e745f6e616d65086c69626d" \
                 + "7973716c045f7069640539323330360f" \
                 + "5f636c69656e745f76657273696f6e06" \
                 + "352e362e3231095f706c6174666f726d" \
                 + "067838365f3634"
        len_hex = hex(int(len(data)/2)).replace("0x","")
        auth_data = len_hex + "000001" +data
        return binascii.a2b_hex(auth_data)

class MongodbNoAuth(object):
    def verify(self,host,user='',pwd='',timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host.host,int(host.port)))
            data = binascii.a2b_hex("3a000000a741000000000000d4070000"
                                    "0000000061646d696e2e24636d640000"
                                    "000000ffffffff130000001069736d61"
                                    "73746572000100000000")
            sock.send(data)
            result = sock.recv(1024)
            if b"ismaster" in result:
                data = binascii.a2b_hex("480000000200000000000000d40700"
                                        "000000000061646d696e2e24636d64"
                                        "000000000001000000210000000267"
                                        "65744c6f6700100000007374617274"
                                        "75705761726e696e67730000")
                sock.send(data)
                result = sock.recv(1024)
                if b"totalLinesWritten" in result:
                    self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                    self.bugreq = "username:%s,password:%s" % (user,pwd)
                    self.bugres = str(result)
                    return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            sock.close()

class RedisNoAuth(object):
    def verify(self,host,user='',pwd='foobared',timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host.host,int(host.port)))
            s.send("INFO\r\n".encode())
            result = s.recv(1024)
            if b'redis_version' in result:
                self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                self.bugreq = "username:%s,password:%s" % (user,pwd)
                self.bugres = str(result)
                return True
            elif b"Authentication" in result:
                s.send(("AUTH %s\r\n"%(pwd)).encode())
                result = s.recv(1024)
                if b'+OK' in result:
                    self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                    self.bugreq = "username:%s,password:%s" % (user,pwd)
                    self.bugres = str(result)
                    return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            s.close()

class MemcachedNoAuth(object):
    def verify(self,host,user='',pwd='',timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host.host,int(host.port)))
            s.send("stats\r\n".encode())
            result = s.recv(1024)
            if b"version" in result:
                self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                self.bugreq = "username:%s,password:%s" % (user,pwd)
                self.bugres = result
                return True
        except Exception as e:
            pass#print(e)
        finally:
            s.close()

class SshNoAuth(object):
    def verify(self,host,user='root',pwd='',timeout=5):
        socket.setdefaulttimeout(timeout)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=host.host,port=host.port,username=user,password=pwd,timeout=timeout)
            self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
            self.bugreq = "user:%s,pwd:%s" % (user,pwd)
            return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            ssh.close()

class TelnetNoAuth(object):
    def verify(self,host,user='admin',pwd='',timeout=10):
        socket.setdefaulttimeout(timeout)
        try:
            tn = telnetlib.Telnet(host.host,host.port,10)
            #tn.set_debuglevel(3)
            op = tn.read_some()
        except Exception as e:
            pass#print('[*]   ',e)
            return False
        user_match = "(?i)(login|user|username)"
        pass_match = '(?i)(password|pass)'
        login_match = '#|\$|>'
        if re.search(user_match,op):
            try:
                tn.write(str(user)+'\r\n')
                tn.read_until(pass_match,timeout=timeout)
                tn.write(str(pwd)+'\r\n')
                login_info=tn.read_until(login_match,timeout=timeout)
                tn.close()
                if re.search(login_match,login_info):
                    self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                    return True
            except Exception as e:
                pass
        else:
            try:
                info = tn.read_until(user_match,timeout=timeout)
            except Exception as e:
                return False
            if re.search(user_match,info):
                try:
                    tn.write(str(pwd)+'\r\n')
                    tn.read_until(pass_match,timeout=5)
                    tn.write(str(pwd)+'\r\n')
                    login_info = tn.read_until(login_match,timeout=5)
                    tn.close()
                    if re.search(login_match,login_info):
                        self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                        return True
                except Exception as e:
                    return False
            elif re.search(pass_match,info):
                tn.read_until(pass_match,timeout=5)
                tn.write(str(pwd)+'\r\n')
                login_info=tn.read_until(login_match,timeout=5)
                tn.close()
                if re.search(login_match,login_info):
                    self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                    return True

class FtpWeakPass(object):
    def verify(self,host,user='anonymous',pwd='',timeout=5):
        socket.setdefaulttimeout(timeout)
        ftp = ftplib.FTP()
        try:
            ftp.connect(host.host,int(host.port))
            ftp.login(user,pwd)
            self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
            return True
        except Exception as e:
            pass#print('[*]   ',e)
        finally:
            pass#ftp.quit()

class RsyncNoAuth(object):
    def verify(self,host,user='',pwd='',timeout=15):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host.host, int(host.port)))
            sock.sendall("\x40\x52\x53\x59\x4e\x43\x44\x3a\x20\x33\x31\x2e\x30\x0a".encode())
            ret = sock.recv(256)
            if b"RSYNCD" in ret:
                sock.sendall("\x0a".encode())
            data = sock.recv(256)
            if len(data)>0:
                self.bugaddr = "%s:%s@%s:%s"%(user,pwd,host.host,host.port)
                self.bugreq = "username:%s,password:%s" % (user,pwd)
                #self.bugres = data
                return True
        except Exception as e:
            pass#print(e)
        finally:
            sock.close()

if __name__=='__main__':
    s = Tomcat_weak_pass()
    PORT = 8080
    hs = open('port.txt','r').readlines()
    ps = open('pass.txt','r').readlines()
    for h in hs:
        for p in ps:
            h = h.strip()
            p = p.strip()
            print('[*]   ',h,p)
            if s.verify(Host(h,PORT),pwd=p):
                print('  [+]   ',h,p,s)
                open('ret.txt','a+').write('%s://%s@%s\r\n'%(s,p,h))



#select * from result_ports_8_21 where service ='rsync'
#SELECT SERVICE from result_ports_8_21 WHERE 1=1 GROUP BY SERVICE
