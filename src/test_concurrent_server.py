"""Test concurrent server."""
import pytest
from client import main


def test_response_logs():
    """test_response_logs."""
    from concurent_server import response_error
    assert response_error() == "HTTP/1.1 500 Internal Server Error"


def test_dir_uri_returns_files_expected():
    """Test_dir_uri_returns_files_expected."""
    from concurent_server import resolve_uri
    res = resolve_uri('dir_for_test')
    assert type(res) == list


def test_a_response_ok():
    """Test if server response with HTTP 200 ok message."""
    from concurent_server import response_ok
    res = response_ok("GET www.google.com HTTP/1.1\r\nHost:\r\n")
    assert "HTTP/1.1 200 OK" in res.values()


def test_case_fail():
    """test_case_fail."""
    with pytest.raises(Exception):
        main()


def test_response_error():
    """Test if server response with HTTP 500 Internal Server Error."""
    from concurent_server import response_error
    res = response_error()
    assert res == 'HTTP/1.1 500 Internal Server Error'


def test_response_error_400_invalid_get():
    """Test_response_error_400_invalid_get."""
    from concurent_server import parse_request
    assert parse_request("r\nHeader: Value\r\n\r\n") == "400 BAD REQUEST"


def test_response_parse_request_200():
    """Test_response_parse_request_200."""
    from concurent_server import parse_request
    assert parse_request("GET www.google.com HTTP/1.1\r\nHost:\r\n") == "HTTP"
    +"/1.1 200 OK www.google.com"


def test_parse_request_no_host_412():
    """Test_parse_request_no_host."""
    from concurent_server import parse_request
    assert parse_request('GET resource HTTP/1.1\r\n www.some.com\r\n\r\n') == "412 PRECONDITION FAILED - Host required"


def test_parse_request_message_well_formed_returns_uri():
    """Test for well formed request."""
    from concurent_server import parse_request
    assert parse_request("GET URI HTTP/1.1\r\nHost:\r\n") == "HTTP/1.1 "
    +"200 OK URI"


def test_file_return_contents_with_div():
    """Test_file_return_contents_with_div."""
    from concurent_server import resolve_uri
    res = resolve_uri('dir_for_test/another.txt')
    assert res[1] == '<div>hello world this is a test of our http server!</div>'


def test_make_response_body():
    """Test_make_response_body."""
    from concurent_server import resolve_uri
    res = resolve_uri('dir_for_test/another.txt')
    assert res == ['', '<div>hello world this is a test of our http server!</div>']
