#encoding:utf-8
import SocketServer
from Crypto.Cipher import AES
import os
import random
from secret import KEY,KEYSIZE,IV,FLAG  #隐藏的参数

HOST="127.0.0.1"#请修改为服务器对外服务的IP
PORT = 18883

def pad(instr, length):
        if(length == None):
                print("Length to pad error")
        elif(len(instr) % length == 0):
                print("No Padding")
                return instr
        else:
                return instr + '\x04' * (length - (len(instr) % length ))

def encrypt_block(key, plaintext):
        encobj = AES.new(key, AES.MODE_ECB)
        return encobj.encrypt(plaintext).encode('hex')

def decrypt_block(key, ctxt):
        decobj = AES.new(key, AES.MODE_ECB)
        return decobj.decrypt(ctxt).encode('hex')

def xor_block(first,second):
        if(len(first) != len(second)):
                print("Blocks need to be the same length!")
                return -1

        first = list(first)
        second = list(second)
        for i in range(0,len(first)):
                first[i] = chr(ord(first[i]) ^ ord(second[i]))
        return ''.join(first)

def encrypt_cbc(key,IV, plaintext):
        if(len(plaintext) % len(key) != 0):
                plaintext = pad(plaintext,len(key))
        blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
        for i in range(0,len(blocks)):
                if (i == 0):
                        ctxt = xor_block(blocks[i],IV)
                        ctxt = encrypt_block(key,ctxt)
                else:
                        tmp = xor_block(blocks[i],ctxt[-1 * (len(key) * 2):].decode('hex'))
                        ctxt = ctxt + encrypt_block(key,tmp)
        return ctxt

def decrypt_cbc(key,IV,ctxt):
        ctxt = ctxt.decode('hex')
        if(len(ctxt) % len(key) != 0):
                print("Invalid key.")
                return -1
        blocks = [ctxt[x:x+len(key)] for x in range(0,len(ctxt),len(key))]
        for i in range(0,len(blocks)):
                #print blocks[0].encode('hex')
                if (i == 0):
                        ptxt = decrypt_block(key,blocks[i])
                        ptxt = xor_block(ptxt.decode('hex'),IV)
                        #print ptxt.encode('hex')
                else:
                        tmp = decrypt_block(key,blocks[i])
                        tmp = xor_block(tmp.decode('hex'),blocks[i-1])
                        ptxt = ptxt + tmp
        return ptxt


def mkprofile(email):
    if((";" in email)):
        return -1
    if(("@" not in email)):
        return -1
    if(("." not in email)):
        return -1
    prefix = "comment1=nice%20CBCAES;userdata="
    suffix = ";coment2=are%20you%20clever%20expert!"

    ptxt = prefix + email + suffix
    print(ptxt)
    return encrypt_cbc(KEY,IV,ptxt)


def parse_profile(data):
    print("DATA:")
    #print data
    ptxt = decrypt_cbc(KEY,IV,data.encode('hex'))
    ptxt = ptxt.replace("\x04","")
    print(ptxt)
    if ";admin=true;" in ptxt:
        return 1
    return 0


class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.sendall("Welcome, input with 'encrypt:email' to get encrypted data of email, with 'decrypt:hexcode' to decrypt data testing if you are admin, if you are admin, you will get the key!\n")
        data = self.request.recv(1024)[:-1]
        print(data)
        if(len(data) > 512):
            self.request.sendall("Too long data.\n")
            self.request.close()
            return

        if(data.startswith("encrypt:")):
            data = data[8:]
            resp = mkprofile(data)
            if (resp == -1):
                self.request.sendall("You must input email(like test@qq.com), no Cheating!\n")
            else:
                self.request.sendall(resp + '\n')
        elif(data.startswith("decrypt:")):
            self.request.sendall("Parsing cipher...\n")
            data = data[8:].decode('hex')
            if (len(data) % KEYSIZE != 0):
                self.request.sendall("Invalid Ciphertext length\n")
                self.request.close()
                return

            if(parse_profile(data) == 1):
                self.request.sendall("Congratulations!\nThe KEY is: ")
                self.request.sendall(FLAG+'\n')
                self.request.close()

            else:
                self.request.sendall("You are not admin.\n")

        else:
            self.request.sendall("Pase Error\n")
            self.request.close()


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    print(HOST)
    print(PORT)
    server = ThreadedServer((HOST, PORT), MyServer)
    server.allow_reuse_address = True
    server.serve_forever()

