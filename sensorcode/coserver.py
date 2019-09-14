from select import select
import multiprocessing as mp
import queue
import socket
import struct
import time
import sys
import random

con_msg = struct.Struct('BBBB')

def dqueue(q):
    while not q.empty():
        yield q.get()

def mupdate():
    while True:
        yield random.randrange(500),

def handle(conqueue, update, fmt, msock, dport):
    gen = update()
    pfmt = struct.Struct(fmt)
    connections = {}
    while True:
        try:
            for msg,conn in dqueue(conqueue):
                if msg == b'CONN':
                    print('Connection on ' + conn[0])
                    connections[conn[0]] = (conn[0], dport)
                elif msg == b'DCON':
                    print('Disconnect from ' + conn[0])
                    connections.pop(conn[0], None)

            data = next(gen)
            for key, value in connections.items():
                msock.sendto(pfmt.pack(*data),value)
        except KeyboardInterrupt:
            break

class UdpCoserver:
    def __init__(self, fmt, port, generator = None, framecallback = lambda x: x, host = '', remote = 'localhost'):
        # Meta setup
        self.conport = port
        self.pushport = port + 1
        self.host = host
        self.remote = remote
        self.generator = generator
        self.fmt = fmt
        self.packfmt = struct.Struct(fmt)
        self.connectalive = False
        self.framecallback = framecallback

    def __polldata(self):
        # Create receive socket
        self.rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rsock.bind((self.host, self.pushport))

        # Send connect frame
        self.rsock.sendto(b'CONN', (self.remote, self.conport))

        # Yield next frame
        while self.connectalive:
            data, addr = self.rsock.recvfrom(self.packfmt.size)
            yield self.framecallback(self.packfmt.unpack(data))

    def serve(self):
        # Bind listen socket
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.lsock.setblocking(0)
        self.lsock.bind((self.host, self.conport))

        # Create push socket
        self.psock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create handler process
        self.pqueue = mp.Queue()
        self.handler = mp.Process(target=handle, args=(self.pqueue,self.generator,self.fmt,self.psock,self.pushport))
        self.handler.daemon = True

        # Serve forever
        try:
            self.handler.start()
            while True:
                read,_,_ = select([self.lsock], [], [], 2)
                if len(read) > 0:
                    connection = self.lsock.recvfrom(con_msg.size)
                    self.pqueue.put(connection)
        except KeyboardInterrupt:
            self.handler.terminate()
            self.lsock.close()
            self.psock.close()

    def connect(self):
        self.connectalive = True
        return self.__polldata()

    def disconnect(self):
        if self.connectalive:
            self.rsock.sendto(b'DCON', (self.remote, self.conport))
            self.connectalive = False
            return True
        else:
            return False

if __name__ == '__main__':
    server = UdpCoserver('i', 5555, generator = mupdate)
    server.serve()
