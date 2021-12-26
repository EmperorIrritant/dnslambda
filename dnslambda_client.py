import dnslib.server

class DNSRequestHandler(dnslib.server.DNSHandler):
    def handle(self):
        # Receive data from request
        # Parse data to DNSRecord
        # Extract query information from DNSRecord
        # call get_reply() with query information
        # make DNSRecord from get_reply response
        # pack DNSRecord object with dnslib
        # pack with struct.pack
        # send reply back to the client
        pass

    def get_reply(self, data):
        # call Lambda with AWS user credentials (Later - call using a Role given by Cognito)
        # get response from Lambda as text
        pass

class DummyResolver():
    def __init__(self):
        pass

if __name__ == '__main__':

    import argparse, sys, time

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
    p.add_argument("--tcp",action='store_true',default=False,
                    help="TCP proxy (default: UDP only)")
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
    udp_server = dnslib.server.DNSServer(resolver,
                           port=args.port,
                           address=args.address,
                           handler=handler)
#                           logger=logger,
    udp_server.start_thread()

    if args.tcp:
        tcp_server = dnslib.server.DNSServer(resolver,
                               port=args.port,
                               address=args.address,
                               tcp=True,
                               handler=handler)
#                               logger=logger,
        tcp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)