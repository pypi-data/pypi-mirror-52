import requests
from payeezy.__make_headers import make_headers
from payeezy.__generate_hmac import generate_hmac


class Transaction(object):
    def __init__(self, api_key, api_secret, token, url, payload):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = token
        self.url = url
        self.payload = payload
        self.transaction_response = None

    def __get_transaction_response(self):
        return self.transaction_response

    def __set_transaction_response(self, response_value):
        self.transaction_response = response_value

    def run_transaction(self):
        authorization, nonce, timestamp = generate_hmac(self.api_key, self.api_secret, self.token, self.payload)
        headers = make_headers(self.api_key, self.token, authorization, nonce, timestamp)
        transaction_results = requests.post(url=self.url, data=self.payload, headers=headers)
        self.__set_transaction_response(transaction_results)

    def is_transaction_approved(self):
        """
        Returns True if transaction approved and False otherwise.

        The gateway_resp_code will always be “00” for a successful transaction, indicating that there were no errors
        attempting to process the transaction. The bank_resp_code will vary based on the response from the issuing bank.

        Complete list of bank response codes:
        https://support.payeezy.com/hc/en-us/articles/203730509-First-Data-Payeezy-Gateway-Bank-Response-Codes
        """
        # TODO find humane way to manage the codes
        VALID_HTTP_STATUS_CODES = [200, 201, 202]
        VALID_BANK_RESPONSE_CODES = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111',
                                     '164']

        response = self.__get_transaction_response()

        # get response status code
        http_status_code = response.status_code

        if http_status_code in VALID_HTTP_STATUS_CODES:
            # get response data
            response_data = response.json()

            # get gateway_resp_code
            gateway_response_code = response_data['gateway_resp_code']

            # compare gate_way_resp code to '00'
            gateway_response_is_valid = False
            if gateway_response_code == '00':
                gateway_response_is_valid = True

            # get bank_resp_code
            bank_response_code = response_data['bank_resp_code']

            # compare bank_resp_code to valid(successful) codes
            bank_response_is_valid = False
            if bank_response_code in VALID_BANK_RESPONSE_CODES:
                bank_response_is_valid = True

            # transaction approved if BOTH gateway_resp_code and bank_resp_code are valid(successful) codes:
            if gateway_response_is_valid and bank_response_is_valid:
                return True

        # transaction failed
        return False

    def report_transaction_error_messages(self):
        """
        Gets error messages from response to HTTP request for invalid transactions.
        Returns list.
        """
        response = self.__get_transaction_response()

        # get response data from response object
        response_data = response.json()

        # get error messages
        response_error = response_data['Error']
        response_error_messages = response_error['messages']

        # add all error messages to the report
        error_messages_to_report = []
        for response_error_message in response_error_messages:
            error_description = response_error_message['description']
            error_messages_to_report.append(error_description)

        return error_messages_to_report
