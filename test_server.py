"""Test server."""
import pytest
from client import main

'''
'''
def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message"
    res = main(message)
    print('this is what main(message) returns: ', res)
    assert res == 22


''''''
def test_a_response_ok():
    """test if server response with HTTP 200 ok message"""
    from server import response_ok
   # message = "This is a test message"
    res = response_ok()
    print('this is what main(message) returns: ', res)
   

#def test_response_ok_ITSNOTOK():