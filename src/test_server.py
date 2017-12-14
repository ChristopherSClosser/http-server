"""Test server."""
import pytest
from client import client
from server import parse_request


def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message"
    res = client(message)
    assert 'HTTP/1.1 200 OK' in res


def test_a_response_ok():
    """Test if server response with HTTP 200 ok message."""
    from server import response_ok
    res = response_ok()
    assert b'HTTP/1.1 200 OK' in res


def test_a_response_ok():
    """Test if server response with HTTP 200 ok message."""
    from server import response_ok
    res = response_ok("GET www.google.com HTTP/1.1\r\nHost:\r\n", None)
    assert "HTTP/1.1 200 OK" in res.values()


def test_case_fail():
    """test_case_fail."""
    with pytest.raises(Exception):
        client()


def test_response_logs():
    """test_response_logs."""
    from server import response_logs
    message = "This is a test message"
    res = client(message)
    response_logs(res)
    assert response_logs(res)


def test_message_shorter_than_one_buffer():
    """Test_message_shorter_than_one_buffer."""
    message = "A"
    res = client(message)
    assert len(res) == 56


def test_message_several_buffers():
    """Test_message_several_buffers."""
    message = "Hello World this is a test\r\n"
    res = client(message)
    assert len(res) > 5


def test_multiple_msg_buffers_one_length():
    """Test_multiple_msg_buffers_one_length."""
    msg1 = "a"
    msg2 = "b"
    msg3 = "c"
    assert len(msg1) == 1
    assert len(msg2) == 1
    assert len(msg3) == 1


def test_message_for_non_ascii():
    """Test_message_for_non_ascii."""

    # assert len(non_ascii1) == 1
    # assert len(non_ascii2) == 1


def test_response_error_400_invalid_get():
    """Test_response_error_400_invalid_get."""
    res = parse_request("r\nHeader: Value\r\n\r\n")
    assert "400 BAD REQUEST" in res


def test_response_error_412_bad_precondition():
    """Test_response_error_412_bad_precondition."""
    res = parse_request("GET\r\nHeader: Value\r\n\r\n") assert "412 PRECONDITION FAILED - HTTP v. 1.1 required" in res


# def test_response_parse_request_200():
#     """Test_response_parse_request_200."""
#     res = parse_request("GET www.google.com HTTP/1.1\r\nHost:\r\n")
#     assert res[2] == 'www.google.com'
#
#
# def test_parse_request_no_host_412():
#     """Test_parse_request_no_host."""
#     assert parse_request('GET resource HTTP/1.1\r\n www.some.com\r\n\r\n') == "412 PRECONDITION FAILED - Host required"
#
#
# def test_parse_request_message_well_formed_returns_uri():
#     """Test for well formed request."""
#     assert parse_request("GET URI HTTP/1.1\r\nHost:\r\n") == "HTTP/1.1 200 OK URI"
#
#
# def test_dir_uri_returns_files_expected():
#     """Test_dir_uri_returns_files_expected."""
#     from server import resolve_uri
#     res = resolve_uri('src/dir_for_test')
#     assert type(res) == list
#
#
# def test_file_return_contents_with_div():
#     """Test_file_return_contents_with_div."""
#     from server import resolve_uri
#     res = resolve_uri('src/dir_for_test/another.txt')
#     assert res[1] == '<div>hello world this is a test of our http server!</div>'
#
#
# def test_file_check_file_extension():
#     """Test_file_check_file_extension."""
#     from server import resolve_uri
#     res = resolve_uri('src/dir_for_test/jam.png')
#     assert '</img>' in res[1]
#
#
# def test_make_response_body():
#     """Test_make_response_body."""
#     from server import resolve_uri
#     res = resolve_uri('src/dir_for_test/another.txt')
#     assert res == ['', '<div>hello world this is a test of our http server!</div>']
#
#
# @pytest.fixture(scope="session")
# def fake_socket():
#     """Set-up testing for HTTP respose structure."""
#     if sys.version_info.major == 3:
#         from io import BytesIO
#     else:
#         from StringIO import StringIO as BytesIO
#
#     class FakeSocket(object):
#
#         def __init__(self, response_str):
#             self._file = BytesIO(response_str)
#
#         def makefile(self, *args, **kwargs):
#             return self._file
#
#     return FakeSocket
#
#
# @pytest.mark.parametrize('message', ['', 'M', 'Hello World!', 'aaaaaaab',
#                                      'aaaaaaabaaaaaaab', 'éclair', 'This is a \
# sentence longer than the others and has spaces too, with punctuation.'])
# def test_fail_on_sending_message(message):
#     """Test that message received from server is a 400 response."""
#     from client import client
#     assert client(message).split('\r\n')[0] == 'HTTP/1.1 400 Bad Request'
#
#
# def test_success_on_sending_http_requests():
#     """Test that message received from server is a 200 response."""
#     from client import client
#     req = 'GET /sample.txt HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     assert client(req).split('\r\n')[0] == 'HTTP/1.1 200 OK'
#
#
# def test_success_sending_http_request_retrieves_file_body():
#     """Test that message received has a file body."""
#     from client import client
#     req = 'GET /sample.txt HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     assert client(req).split('\r\n\r\n')[1] == """This is a very simple text file.
# Just to show that we can serve it up.
# It is three lines long.
# """
#
#
# def test_fail_on_getting_missing_file():
#     """Test that message received from server is a 404 response."""
#     from client import client
#     req = 'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     assert client(req).split('\r\n')[0] == 'HTTP/1.1 404 Not Found'
#
#
# def test_fail_on_sending_non_get_http_requests():
#     """Test that message received from server is a 405 response."""
#     from client import client
#     req = 'POST /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     assert client(req).split('\r\n')[0] == 'HTTP/1.1 405 Method Not Allowed'
#
#
# def test_ok_response_well_formatted(fake_socket):
#     """Test that formatting of 200 HTTP response is correct."""
#     from server import response_ok
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_ok(b'', 'text/plain'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 200
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_ok_response_body_is_there(fake_socket):
#     """Test that request has a body."""
#     from server import response_ok
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     response_str = response_ok(b'htmlhtml', 'text/plain')
#     source = fake_socket(response_str)
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.read(len(response_str)) == b'htmlhtml'
#
#
# def test_ok_response_mime_type_is_there(fake_socket):
#     """Test that request has a proper mime_type."""
#     from server import response_ok
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     response_str = response_ok(b'htmlhtml', 'text/plain')
#     source = fake_socket(response_str)
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.getheader('Content-Type') == 'text/plain'
#
#
# def test_error_response_500_well_formatted(fake_socket):
#     """Test that error reponse of 500 HTTP response is correct."""
#     from server import response_error
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_error(500, 'Internal Server Error'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 500
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_error_response_501_well_formatted(fake_socket):
#     """Test that error reponse of 501 HTTP response is correct."""
#     from server import response_error
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_error(501, 'Not Implemented'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 501
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_error_response_400_well_formatted(fake_socket):
#     """Test that error reponse of 400 HTTP response is correct."""
#     from server import response_error
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_error(400, 'Bad Request'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 400
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_error_response_404_well_formatted(fake_socket):
#     """Test that error reponse of 404 HTTP response is correct."""
#     from server import response_error
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_error(404, 'Not Found'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 404
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_error_response_405_well_formatted(fake_socket):
#     """Test that error reponse of 405 HTTP response is correct."""
#     from server import response_error
#     from datetime import datetime as time
#
#     if sys.version_info.major == 3:
#         from http.client import HTTPResponse
#     else:
#         from httplib import HTTPResponse
#
#     source = fake_socket(response_error(405, 'Method Not Allowed'))
#     response = HTTPResponse(source)
#     response.begin()
#     assert response.status == 405
#     assert time.strptime(response.getheader('Date'),
#                          '%a, %d %b %Y %H:%M:%S %Z')
#
#
# def test_valid_parse_http_request():
#     """Test the parse_request accepts valid GET http request."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     assert parse_request(req) == b'/index.html'
#
#
# def test_request_parse_invalid_missing_host_header():
#     """Test for invalid missing host header."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# From: frog@j.money.com\r\n\
# User-Agent: Mozilla/3.0Gold\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_number_of_lines():
#     """Test if not three lines in request, raises ValueError."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_line_formatting():
#     """Test if line is properly formatted with carriage returns."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# DATE:\r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_method_uri_protocol_line_formatting():
#     """Test if the first line of req is properly formatted with white space."""
#     from server import parse_request
#     req = b'GET / index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# @pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'get'])
# def test_request_parse_invalid_method_is_not_get(method):
#     """Test if the method is for a GET request."""
#     from server import parse_request
#     req = '{} /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'.format(method).encode('utf8')
#     with pytest.raises(NotImplementedError):
#         parse_request(req)
#
#
# @pytest.mark.parametrize('protocol', ['HTTP/1.2', 'HTTP/1.0', 'HTTP',
#                                       'http/1.1'])
# def test_request_parse_invalid_protocol_is_not_http_11(protocol):
#     """Test if the protocol is for HTTP/1.1."""
#     from server import parse_request
#     req = 'GET /index.html {}\r\n\
# Host: www.example.com\r\n\
# \r\n'.format(protocol).encode('utf8')
#     with pytest.raises(NotImplementedError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_uri_is_not_file_path():
#     """Test if the uri is a valid file path."""
#     from server import parse_request
#     req = b'GET index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_left_justified_header_name():
#     """Test if the header name is left justifiied."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
#     Content-Type: text/plain\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_missing_colon_header_name():
#     """Test if the header name is missing a colon."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com\r\n\
# Content-Type : text/plain\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
#
#
# def test_request_parse_invalid_url_for_host_value():
#     """Test if the URL for the Host uses proper characters."""
#     from server import parse_request
#     req = b'GET /index.html HTTP/1.1\r\n\
# Host: www.example.com!\r\n\
# Content-Type: text/plain\r\n\
# \r\n'
#     with pytest.raises(ValueError):
#         parse_request(req)
