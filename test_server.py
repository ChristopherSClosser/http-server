"""Test server."""
from client import main
import pytest
from server import parse_request


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
    # message = "This is a test message"
    # res = main(message)
    # response_logs(res)
    # print('response_logs: ', response_logs(res))
    # assert response_logs(res)


def test_response_error_400_invalid_get():
    """Test_response_error_400_invalid_get."""
    assert parse_request("r\nHeader: Value\r\n\r\n") == "400 BAD REQUEST"


def test_response_error_412_bad_precondition():
    """Test_response_error_412_bad_precondition."""
    assert parse_request("GET\r\nHeader: Value\r\n\r\n") == "412 PRECONDITION FAILED - HTTP v. 1.1 required"


def test_response_parse_request_200():
    """Test_response_parse_request_200."""
    assert parse_request("GET www.google.com HTTP/1.1\r\nHost:\r\n") == "HTTP/1.1 200 OK www.google.com"


def test_parse_request_no_host_412():
    """Test_parse_request_no_host."""
    assert parse_request('GET resource HTTP/1.1\r\n www.some.com\r\n\r\n') == "412 PRECONDITION FAILED - Host required"


def test_parse_request_message_well_formed_returns_uri():
    """Test for well formed request"""
    assert parse_request("GET URI HTTP/1.1\r\nHost:\r\n") == "HTTP/1.1 200 OK URI"


def test_dir_uri_returns_files_expected():
    """Test_dir_uri_returns_files_expected."""
    from server import resolve_uri
    print('should return a list', resolve_uri('dir_for_test'))
    res = resolve_uri('dir_for_test')
    assert res[0] == ['html.html', 'another.txt']

def test_file_return_contents():
    from server import resolve_uri
    resolve_uri('dir_for_test/another.txt')
    res = resolve_uri('dir_for_test/another.txt')
    assert res[1] == '<div>hello world this is a test of our http server!</div>'
