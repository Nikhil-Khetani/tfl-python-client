'''exceptions.py'''
import json

class TFLAPIException(Exception):    
    """
    Exception for unparseable responses for TFL API.
    """
    def __init__(self, response, status_code, text):
        self.code = 0
        try:
            json_res = json.loads(text)
        except ValueError:
            self.message = f'Invalid JSON error message from TFL: {response.text}'
        else:
            self.code = json_res['httpStatusCode']
            self.message = json_res['message']
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return f'APIError(code={self.code}): {self.message}'

class TFLRequestException(Exception):
    """
    Exception for when TFL API request is unsuccessful.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'TFLRequestException: {self.message}'
