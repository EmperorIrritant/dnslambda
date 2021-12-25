import requests
from random import choice

import dns.message
import dns.query
import dns.rdatatype

dohservers = ['https://dns.google/dns-query', 'https://cloudflare-dns.com/dns-query', 'https://doh.appliedprivacy.net/query']
server = choice(dohservers)

def lambda_handler(event, context):
    qname = event["query"]
    with requests.sessions.Session() as session:
        q = dns.message.make_query(qname, dns.rdatatype.A)
        r = dns.query.https(q, server, session=session)
        return "\n".join([responseline.to_text() for responseline in r.answer])
