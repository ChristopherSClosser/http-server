"""Test server."""
import pytest
from client import main


def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message"
    res = main(message)
    print('this is what main(message) returns: ', res)
    assert res == 22


def test_a_response_ok():
    """Test if server response with HTTP 200 ok message."""
    from server import response_ok
    # message = "This is a test message"
    res = response_ok()
    assert res == "HTTP/1.1 200 OK"


def test_response_error():
    """test_response_error."""
    from server import resonse_error
    res = resonse_error()
    assert res == 'HTTP/1.1 500 Internal Server Error'
