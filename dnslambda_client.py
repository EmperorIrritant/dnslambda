import dnslib.server
from dnslib.dns import DNSRecord, RR, DNSError
import argparse, sys, time
import socket
import struct
import socketserver

import dnslambda_server

class DNSRequestHandler(socketserver.BaseRequestHandler):

    udplen = 0

    def handle(self):
        # Receive data from request
        if self.server.socket_type == socket.SOCK_STREAM:
            self.protocol = 'tcp'
            data = self.request.recv(8192)
            if len(data) < 2:
                return
            length = struct.unpack("!H", bytes(data[:2]))[0]
            while len(data) - 2 < length:
                new_data = self.request.recv(8192)
                if not new_data:
                    break
                data += new_data
            data = data[2:]
        else:
            self.protocol = 'udp'
            data, connection = self.request

        # Parse data to DNSRecord
        request = dnslib.server.DNSRecord.parse(data)
        # Extract query information from DNSRecord
        qname, qtype = str(request.q.qname), request.q.qtype
        try:
            # call get_reply() with query information
            reply = self.get_reply((qname, qtype))

            # make DNSRecord from get_reply response
            response = request.reply()
            response.add_answer(*RR.fromZone(reply))

            # pack DNSRecord object with dnslib
            if self.protocol == 'udp':
                rdata = response.pack()
                if self.udplen and len(rdata) > self.udplen:
                    truncated_reply = reply.truncate()
                    rdata = truncated_reply.pack()
            else:
                rdata = reply.pack()
            # pack with struct.pack
            # send reply back to the client
            if self.protocol == 'tcp':
                rdata = struct.pack("!H", len(rdata)) + rdata
                self.request.sendall(rdata)
            else:
                connection.sendto(rdata, self.client_address)
        except DNSError as e:
            print(e)

    def get_reply(self, data):
        # call Lambda with AWS user credentials (Later - call using a Role given by Cognito)
        # get response from Lambda as text
        qname, qtype = data
        event = {"query": {"qname": qname, "qtype": qtype}}
        return dnslambda_server.lambda_handler(event, {})

class DummyResolver():
    def __init__(self):
        pass

def main():
    p = argparse.ArgumentParser(description="DNS Proxy")
    p.add_argument("--port","-p",type=int,default=53,
                    metavar="<port>",
                    help="Local proxy port (default:53)")
    p.add_argument("--address","-a",default="",
                    metavar="<address>",
                    help="Local proxy listen address (default:all)")
#    p.add_argument("--upstream","-u",default="8.8.8.8:53",
#            metavar="<dns server:port>",
#                    help="Upstream DNS server:port (default:8.8.8.8:53)")
#    p.add_argument("--tcp",action='store_true',default=False,
#                    help="TCP proxy (default: UDP only)")
#    p.add_argument("--timeout","-o",type=float,default=5,
#                    metavar="<timeout>",
#                    help="Upstream timeout (default: 5s)")
#    p.add_argument("--passthrough",action='store_true',default=False,
#                    help="Dont decode/re-encode request/response (default: off)")
#    p.add_argument("--log",default="request,reply,truncated,error",
#                    help="Log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)")
#    p.add_argument("--log-prefix",action='store_true',default=False,
#                    help="Log prefix (timestamp/handler/resolver) (default: False)")
    args = p.parse_args()

#    args.dns,_,args.dns_port = args.upstream.partition(':')
#    args.dns_port = int(args.dns_port or 53)

#    print("Starting Proxy Resolver (%s:%d -> %s:%d) [%s]" % (
#                        args.address or "*",args.port,
#                        args.dns,args.dns_port,
#                        "UDP/TCP" if args.tcp else "UDP"))

    resolver = DummyResolver()
    handler = DNSRequestHandler
#    logger = DNSLogger(args.log,args.log_prefix)

    try:
        udp_server = dnslib.server.DNSServer(resolver,
                                port=args.port,
                                address=args.address,
                                handler=handler)
    #                           logger=logger,
        udp_server.start_thread()

        tcp_server = dnslib.server.DNSServer(resolver,
                                port=args.port,
                                address=args.address,
                                tcp=True,
                                handler=handler)
    #                               logger=logger,
        tcp_server.start_thread()

        while udp_server.isAlive():
            time.sleep(1)
    except Exception as e:
        print(args.port)
        print(f"Exiting: {e}")

if __name__ == '__main__':
    main()
