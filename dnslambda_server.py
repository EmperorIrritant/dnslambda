#!/usr/bin/env python3
#
# This is an example of sending DNS queries over HTTPS (DoH) with dnspython.
# Requires use of the requests module's Session object.
#
# See https://2.python-requests.org/en/latest/user/advanced/#session-objects
# for more details about Session objects
import requests

import dns.message
import dns.query
import dns.rdatatype


def main():
    where = '1.1.1.1'
    qname = 'example.com.'
    with requests.sessions.Session() as session:
        q = dns.message.make_query(qname, dns.rdatatype.A)
        r = dns.query.https(q, where, session=session)
        for answer in r.answer:
            print(answer)

if __name__ == '__main__':
    main()