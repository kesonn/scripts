#!/usr/bin/env python
# -*- coding: utf-8 -*-
#20150815 修改了对win系统log颜色代码的支持 //道长

import platform
import logging
import argparse
import signal
import sys
from threading import Thread
from urlparse import urlparse
from socket import *
from threading import Thread
from time import sleep
#import struct

# Constants
SOCKTIMEOUT = 5
RESENDTIMEOUT=300
VER="\x05"
METHOD="\x00"
SUCCESS="\x00"
SOCKFAIL="\x01"
NETWORKFAIL="\x02"
HOSTFAIL="\x04"
REFUSED="\x05"
TTLEXPIRED="\x06"
UNSUPPORTCMD="\x07"
ADDRTYPEUNSPPORT="\x08"
UNASSIGNED="\x09"

BASICCHECKSTRING = "Georg says, 'All seems fine'"


# Globals
READBUFSIZE = 1024


LEVEL = {
    "INFO" : logging.INFO,
    "DEBUG" : logging.DEBUG,
}

def add_coloring_to_emit_windows(fn):
    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    out_handle = property(_out_handle)
    def _set_color(self, code):
        import ctypes
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)
    setattr(logging.StreamHandler, '_set_color', _set_color)
    def new(*args):
        FOREGROUND_BLUE      = 0x0001 # text color contains blue.
        FOREGROUND_GREEN     = 0x0002 # text color contains green.
        FOREGROUND_RED       = 0x0004 # text color contains red.
        FOREGROUND_INTENSITY = 0x0008 # text color is intensified.
        FOREGROUND_WHITE     = FOREGROUND_BLUE|FOREGROUND_GREEN |FOREGROUND_RED
        STD_INPUT_HANDLE     = -10
        STD_OUTPUT_HANDLE    = -11
        STD_ERROR_HANDLE     = -12
        FOREGROUND_BLACK     = 0x0000
        FOREGROUND_BLUE      = 0x0001
        FOREGROUND_GREEN     = 0x0002
        FOREGROUND_CYAN      = 0x0003
        FOREGROUND_RED       = 0x0004
        FOREGROUND_MAGENTA   = 0x0005
        FOREGROUND_YELLOW    = 0x0006
        FOREGROUND_GREY      = 0x0007
        FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.
        BACKGROUND_BLACK     = 0x0000
        BACKGROUND_BLUE      = 0x0010
        BACKGROUND_GREEN     = 0x0020
        BACKGROUND_CYAN      = 0x0030
        BACKGROUND_RED       = 0x0040
        BACKGROUND_MAGENTA   = 0x0050
        BACKGROUND_YELLOW    = 0x0060
        BACKGROUND_GREY      = 0x0070
        BACKGROUND_INTENSITY = 0x0080 # background color is intensified.
        levelno = args[1].levelno
        if(levelno>=50):
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY
        elif(levelno>=40):
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif(levelno>=30):
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif(levelno>=20):
            color = FOREGROUND_GREEN
        elif(levelno>=10):
            color = FOREGROUND_MAGENTA
        else:
            color =  FOREGROUND_WHITE
        args[0]._set_color(color)
        ret = fn(*args)
        args[0]._set_color( FOREGROUND_WHITE )
        return ret
    return new

def add_coloring_to_emit_ansi(fn):
    def new(*args):
        levelno = args[1].levelno
        if(levelno>=50):
            color = '\x1b[31m' # red
        elif(levelno>=40):
            color = '\x1b[31m' # red
        elif(levelno>=30):
            color = '\x1b[33m' # yellow
        elif(levelno>=20):
            color = '\x1b[32m' # green
        elif(levelno>=10):
            color = '\x1b[35m' # pink
        else:
            color = '\x1b[0m' # normal
        args[1].msg = color + args[1].msg +  '\x1b[0m'  # normal
        return fn(*args)
    return new


if platform.system()=='Windows':
    logging.StreamHandler.emit = add_coloring_to_emit_windows(logging.StreamHandler.emit)
else:
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)

formatter = logging.Formatter('- %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(stream_handler)

transferLog = logging.getLogger("transfer")
transferLog.addHandler(stream_handler)

class SocksCmdNotImplemented(Exception):
    pass

class SocksProtocolNotImplemented(Exception):
    pass

class RemoteConnectionFailed(Exception):
    pass

class session(Thread):
    def __init__(self,pSocket,connectString):
        Thread.__init__(self)
        self.pSocket = pSocket
        self.connectString = connectString
        o = urlparse(connectString)
        try:
            self.httpPort = o.port
        except:
            if o.scheme == "https":
                self.httpPort = 443
            else:
                self.httpPort = 80
        self.httpScheme = o.scheme
        self.httpHost = o.netloc.split(":")[0]
        self.httpPath = o.path
        self.cookie = None
        if o.scheme == "http":
            self.httpScheme = urllib3.HTTPConnectionPool
        else:
            self.httpScheme = urllib3.HTTPSConnectionPool

    def parseSocks5(self,sock):
        log.debug("SocksVersion5 detected")
        nmethods,methods=(sock.recv(1),sock.recv(1))
        sock.sendall(VER+METHOD)
        ver=sock.recv(1)
        if ver=="\x02": # this is a hack for proxychains
            ver,cmd,rsv,atyp=(sock.recv(1),sock.recv(1),sock.recv(1),sock.recv(1))
        else:
            cmd,rsv,atyp=(sock.recv(1),sock.recv(1),sock.recv(1))
        target = None
        targetPort = None
        if atyp=="\x01":# IPv4
            # Reading 6 bytes for the IP and Port
            target = sock.recv(4)
            targetPort = sock.recv(2)
            target =".".join([str(ord(i)) for i in target])
        elif atyp=="\x03":# Hostname
            targetLen = ord(sock.recv(1)) # hostname length (1 byte)
            target = sock.recv(targetLen)
            targetPort  = sock.recv(2)
            target = "".join([unichr(ord(i)) for i in target])
        elif atyp=="\x04":# IPv6
            target = sock.recv(16)
            targetPort = sock.recv(2)
            tmp_addr=[]
            for i in xrange(len(target)/2):
                tmp_addr.append(unichr(ord(target[2*i])*256+ord(target[2*i+1])))
            target=":".join(tmp_addr)
        targetPort = ord(targetPort[0])*256+ord(targetPort[1])
        if cmd=="\x02":#BIND
            raise SocksCmdNotImplemented("Socks5 - BIND not implemented")
        elif cmd=="\x03":#UDP
            raise SocksCmdNotImplemented("Socks5 - UDP not implemented")
        elif cmd=="\x01":#CONNECT
            serverIp = target
            try:
                serverIp = gethostbyname(target)
            except:
                log.error("oeps")
            serverIp="".join([chr(int(i)) for i in serverIp.split(".")])
            self.cookie = self.setupRemoteSession(target,targetPort)
            if self.cookie:
                sock.sendall(VER+SUCCESS+"\x00"+"\x01"+serverIp+chr(targetPort/256)+chr(targetPort%256))
                return True
            else:
                sock.sendall(VER+REFUSED+"\x00"+"\x01"+serverIp+chr(targetPort/256)+chr(targetPort%256))
                raise RemoteConnectionFailed("[%s:%d] Remote failed" %(target,targetPort))


        raise SocksCmdNotImplemented("Socks5 - Unknown CMD")

    def parseSocks4(self,sock):
        log.debug("SocksVersion4 detected")
        cmd=sock.recv(1)
        if cmd == "\x01": # Connect
            targetPort = sock.recv(2)
            targetPort = ord(targetPort[0])*256+ord(targetPort[1])
            target = sock.recv(4)
            sock.recv(1)
            target =".".join([str(ord(i)) for i in target])
            serverIp = target
            try:
                serverIp = gethostbyname(target)
            except:
                log.error("oeps")
            serverIp="".join([chr(int(i)) for i in serverIp.split(".")])
            self.cookie = self.setupRemoteSession(target,targetPort)
            if self.cookie:
                sock.sendall(chr(0)+chr(90)+serverIp+chr(targetPort/256)+chr(targetPort%256))
                return True
            else:
                sock.sendall("\x00"+"\x91"+serverIp+chr(targetPort/256)+chr(targetPort%256))
                raise RemoteConnectionFailed("Remote connection failed")
        else:
            raise SocksProtocolNotImplemented("Socks4 - Command [%d] Not implemented" % ord(cmd))

    def handleSocks(self,sock):
        # This is where we setup the socks connection
        ver = sock.recv(1)
        if ver == "\x05":
            return self.parseSocks5(sock)
        elif ver == "\x04":
            return self.parseSocks4(sock)

    def setupRemoteSession(self,target,port):
        headers = {"X-CMD": "CONNECT", "X-TARGET": target, "X-PORT": port}
        self.target = target
        self.port = port
        cookie = None
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        #response = conn.request("POST", self.httpPath, params, headers)
        response = conn.urlopen('POST', self.connectString+"?cmd=connect&target=%s&port=%d" % (target,port), headers=headers, body="")
        if response.status == 200:
            status = response.getheader("x-status")
            if status == "OK":
                cookie = response.getheader("set-cookie")
                log.info("[%s:%d] HTTP [200]: cookie [%s]" % (self.target,self.port,cookie))
            else:
                if response.getheader("X-ERROR") != None:
                    log.error(response.getheader("X-ERROR"))
        else:
            log.error("[%s:%d] HTTP [%d]: [%s]" % (self.target,self.port,response.status,response.getheader("X-ERROR")))
            log.error("[%s:%d] RemoteError: %s" % (self.target,self.port,response.data))
        conn.close()
        return cookie

    def closeRemoteSession(self):
        headers = {"X-CMD": "DISCONNECT", "Cookie":self.cookie}
        #headers = {"Cookie":self.cookie}
        params=""
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        response = conn.request("POST", self.httpPath+"?cmd=disconnect", params, headers)
        if response.status == 200:
            log.info("[%s:%d] Connection Terminated" % (self.target,self.port))
        conn.close()

    def reader(self):
        conn = urllib3.PoolManager()
        while True:
            try:
                if not self.pSocket: break
                data =""
                headers = {"X-CMD": "READ", "Cookie": self.cookie, "Connection": "Keep-Alive"}
                response = conn.urlopen('POST', self.connectString+"?cmd=read", headers=headers, body="")
                data = None
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") != None:
                            cookie = response.getheader("set-cookie")
                        data = response.data
                        # Yes I know this is horrible, but its a quick fix to issues with tomcat 5.x bugs that have been reported, will find a propper fix laters
                        try:
                            if response.getheader("server").find("Apache-Coyote/1.1") > 0:
                                data = data[:len(data)-1]
                        except:
                            pass
                        if data == None: data=""
                    else:
                        data = None
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target,self.port,response.status,status,response.getheader("X-ERROR")))
                else:
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target,self.port,response.status))
                if data == None:
                    # Remote socket closed
                    break
                if len(data) == 0:
                    sleep(0.1)
                    continue
                transferLog.info("[%s:%d] <<<< [%d]" % (self.target,self.port,len(data)))
                self.pSocket.send(data)
            except Exception , ex:
                raise ex
        self.closeRemoteSession()
        log.debug("[%s:%d] Closing localsocket" % (self.target,self.port))
        try:
            self.pSocket.close()
        except:
            log.debug("[%s:%d] Localsocket already closed" % (self.target,self.port))

    def writer(self):
        global READBUFSIZE
        conn = urllib3.PoolManager()
        while True:
            try:
                self.pSocket.settimeout(1)
                data = self.pSocket.recv(READBUFSIZE)
                if not data: break
                headers = {"X-CMD": "FORWARD", "Cookie": self.cookie,"Content-Type": "application/octet-stream", "Connection":"Keep-Alive"}
                response = conn.urlopen('POST', self.connectString+"?cmd=forward", headers=headers, body=data)
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") != None:
                            self.cookie = response.getheader("set-cookie")
                    else:
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target,self.port,response.status,status,response.getheader("x-error")))
                        break
                else:
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target,self.port,response.status))
                    break
                transferLog.info("[%s:%d] >>>> [%d]" % (self.target,self.port,len(data)))
            except timeout:
                continue
            except Exception,ex:
                raise ex
                break
        self.closeRemoteSession()
        log.debug("Closing localsocket")
        try:
            self.pSocket.close()
        except:
            log.debug("Localsocket already closed")

    def run(self):
        try:
            if self.handleSocks(self.pSocket):
                log.debug("Staring reader")
                r = Thread(target=self.reader, args=())
                r.start()
                log.debug("Staring writer")
                w = Thread(target=self.writer, args=())
                w.start()
                r.join()
                w.join()
        except SocksCmdNotImplemented, si:
            log.error(si.message)
            self.pSocket.close()
        except SocksProtocolNotImplemented, spi:
            log.error(spi.message)
            self.pSocket.close()
        except Exception, e:
            log.error(e.message)
            self.pSocket.close()

def askGeorg(connectString):
    response = requests.get(connectString)
    if response.status == 200:
        if BASICCHECKSTRING in response.data.strip():
            log.info(BASICCHECKSTRING)
            return True
    return False

if __name__ == '__main__':
    print """       _____
  _____   ______  __|___  |__  ______  _____  _____   ______
 |     | |   ___||   ___|    ||   ___|/     \|     | |   ___|
 |     \ |   ___||   |  |    ||   ___||     ||     \ |   |  |
 |__|\__\|______||______|  __||______|\_____/|__|\__\|______|
                    |_____|
                    ... every office needs a tool like Georg

  willem@sensepost.com / @_w_m__
  sam@sensepost.com / @trowalts
  etienne@sensepost.com / @kamp_staaldraad
   """
    log.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='Socks server for reGeorg HTTP(s) tunneller')
    parser.add_argument("-l","--listen-on",metavar="",help="The default listening address",default="127.0.0.1")
    parser.add_argument("-p","--listen-port",metavar="",help="The default listening port",type=int,default="6666")
    parser.add_argument("-r","--read-buff",metavar="",help="Local read buffer, max data to be sent per POST",type=int,default="1024")
    parser.add_argument("-u","--url",metavar="",required=True,help="The url containing the tunnel script")
    parser.add_argument("-v","--verbose",metavar="",help="Verbose output[INFO|DEBUG]",default="INFO")
    args = parser.parse_args()
    if (LEVEL.has_key(args.verbose)):
        log.setLevel(LEVEL[args.verbose])
        log.info("Log Level set to [%s]" % args.verbose)

    log.info("Starting socks server [%s:%d], tunnel \nAt [%s]" % (args.listen_on,args.listen_port,args.url))
    log.info("Checking if Georg is ready")
    if not askGeorg(args.url):
        log.info("Georg is not ready, please check url")
        exit()
    READBUFSIZE = args.read_buff
    servSock = socket(AF_INET,SOCK_STREAM)
    servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    servSock.bind((args.listen_on,args.listen_port))
    servSock.listen(1000)
    while True:
        try:
            sock,addr_info=servSock.accept()
            sock.settimeout(SOCKTIMEOUT)
            log.debug("Incomming connection")
            session(sock,args.url).start()
        except KeyboardInterrupt,ex:
            break
        except Exception,e:
            log.error(e)
    servSock.close()
