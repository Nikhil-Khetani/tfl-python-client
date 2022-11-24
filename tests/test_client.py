'''
test_client.py
'''
from tfl.client import Client

def test_client_not_empty():
    '''
    test_client_not_empty
    '''
    assert Client().test=='test'
