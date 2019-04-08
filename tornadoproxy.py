#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.iostream

class ProxyHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(
                      self.request.uri,
            method  = self.request.method,
            headers = self.request.headers,
        )
        response = yield tornado.gen.Task(client.fetch,req)
        if response.error:
            self.write(str(response.error))
        else:
            self.set_status(response.code)
            for k,v in response.headers.items():
                self.set_header(k, v)
            self.write(response.body)
        self.finish()
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        client = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(
                      self.request.uri,
            method  = self.request.method,
            headers = self.request.headers,
            body    = self.request.body
        )
        response = yield tornado.gen.Task(client.fetch,req)
        if response.error:
            self.write(str(response.error))
        else:
            self.set_status(response.code)
            for k,v in response.headers.items():
                self.set_header(k, v)
            self.write(response.body)
        self.finish()
    @tornado.web.asynchronous
    def connect(self):
        host,port = self.request.uri.split(':')
        client = self.request.connection.stream
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(sock)
        upstream.connect((host, int(port)), start_tunnel)
        def read_from_client(data):
            upstream.write(data)
        def read_from_upstream(data):
            client.write(data)
        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()
        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()
        def start_tunnel():
            print('CONNECT tunnel established to %s', self.request.uri)
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')
        def on_proxy_response(data=None):
            if data:
                first_line = data.splitlines()[0]
                http_v, status, text = first_line.split(None, 2)
                if int(status) == 200:
                    start_tunnel()
                    return
            self.set_status(500)
            self.finish()
        def start_proxy_tunnel():
            upstream.write('CONNECT %s HTTP/1.1\r\n' % self.request.uri)
            upstream.write('Host: %s\r\n' % self.request.uri)
            upstream.write('Proxy-Connection: Keep-Alive\r\n\r\n')
            upstream.read_until('\r\n\r\n', on_proxy_response)

def run_proxy(port):
    app = tornado.web.Application([
        (r'.*', ProxyHandler),
    ])
    app.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

if __name__ == '__main__':
    run_proxy(8888)


