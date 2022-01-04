# dnslambda
DNS proxy with AWS Lambda

The application has a DNS proxy server running as a AWS Lambda function that resolves requests with DNS on HTTPS (DoT) and a local DNS proxy client that listens for both TCP and UDP requests.

DNS query resolution must be low latency for it to be useful, and as fast as Lambda can be, it may still not be useful enough even with caching implemented on both client and server side. This project only aims to add a little more privacy to DNS resolution, by proxying the queries through Lambda's often changing IP addresses, with no strictly logging of client IP addresses.

# Project Status

- Functional client and server, with only A records tested, but communication between server and client through AWS is not implemented yet
