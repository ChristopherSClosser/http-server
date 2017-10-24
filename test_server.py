"""Test server."""
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
    res = response_ok()
    assert res == "HTTP/1.1 200 OK"


def test_response_error():
    """Test if server response with HTTP 500 Internal Server Error."""
    from server import response_error
    res = response_error()
    assert res == 'HTTP/1.1 500 Internal Server Error'


def test_response_logs():
    """test_response_logs."""
    from server import response_logs
    message = "This is a test message"
    res = main(message)
    response_logs(res)
    print('response_logs: ', response_logs(res))
    assert response_logs(res)
