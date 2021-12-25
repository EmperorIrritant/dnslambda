import unittest
import dnslambda_server

lambda_handler = dnslambda_server.lambda_handler

class TestLambdaServer(unittest.TestCase):

    def dnsresponse_parse(self, lambda_handler_response):
        response_lines = lambda_handler_response.split("\n")
        for response_line in response_lines:
            if len(response_line.split(" ")) not in (4, 5):
                return False
        return True

    def test_lambda_handler(self):
        test_event = {"query": "example.com"}
        test_context = {}
        self.assertIs(self.dnsresponse_parse(lambda_handler(test_event, test_context)), True, "Output error")

if __name__ == '__main__':
    unittest.main()