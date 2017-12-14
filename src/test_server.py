"""Test server."""
import pytest
from client import client
from server import parse_request, resolve_uri
import sys


@pytest.fixture(scope="session")
def fake_socket():
    """Set-up testing for HTTP respose structure."""
    if sys.version_info.major == 3:
        from io import BytesIO
    else:
        from StringIO import StringIO as BytesIO

    class FakeSocket(object):

        def __init__(self, response_str):
            self._file = BytesIO(response_str)

        def makefile(self, *args, **kwargs):
            return self._file

    return FakeSocket


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
    assert len(res) == 65


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


@pytest.mark.parametrize('message', ['', 'M', 'Hello World!', 'aaaaaaab',
                                     'aaaaaaabaaaaaaab', 'éclair', 'This is a \
sentence longer than the others and has spaces too, with punctuation.'])
def test_fail_on_sending_message(message):
    """Test that message received from server is a 400 response."""
    from client import client
    assert client(message).split('\r\n')[0] == 'HTTP/1.1 400 Bad Request'


def test_fail_on_getting_missing_file():
    """Test that message received from server is a 404 response."""
    from client import client
    req = 'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    assert client(req).split('\r\n')[0] == 'HTTP/1.1 404 Not Found'


def test_fail_on_sending_non_get_http_requests():
    """Test that message received from server is a 405 response."""
    from client import client
    req = 'POST /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    assert client(req).split('\r\n')[0] == 'HTTP/1.1 405 Method Not Allowed'


def test_ok_response_well_formatted(fake_socket):
    """Test that formatting of 200 HTTP response is correct."""
    from server import response_ok
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_ok(b'', 'text/plain'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 200
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_ok_response_body_is_there(fake_socket):
    """Test that request has a body."""
    from server import response_ok
    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    response_str = response_ok(b'htmlhtml', 'text/plain')
    source = fake_socket(response_str)
    response = HTTPResponse(source)
    response.begin()
    assert response.read(len(response_str)) == b'htmlhtml'


def test_ok_response_mime_type_is_there(fake_socket):
    """Test that request has a proper mime_type."""
    from server import response_ok
    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    response_str = response_ok(b'htmlhtml', 'text/plain')
    source = fake_socket(response_str)
    response = HTTPResponse(source)
    response.begin()
    assert response.getheader('Content-Type') == 'text/plain'


def test_error_response_500_well_formatted(fake_socket):
    """Test that error reponse of 500 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(500, 'Internal Server Error'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 500
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_501_well_formatted(fake_socket):
    """Test that error reponse of 501 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(501, 'Not Implemented'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 501
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_400_well_formatted(fake_socket):
    """Test that error reponse of 400 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(400, 'Bad Request'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 400
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_404_well_formatted(fake_socket):
    """Test that error reponse of 404 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(404, 'Not Found'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 404
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_error_response_405_well_formatted(fake_socket):
    """Test that error reponse of 405 HTTP response is correct."""
    from server import response_error
    from datetime import datetime as time

    if sys.version_info.major == 3:
        from http.client import HTTPResponse
    else:
        from httplib import HTTPResponse

    source = fake_socket(response_error(405, 'Method Not Allowed'))
    response = HTTPResponse(source)
    response.begin()
    assert response.status == 405
    assert time.strptime(response.getheader('Date'),
                         '%a, %d %b %Y %H:%M:%S %Z')


def test_valid_parse_http_request():
    """Test the parse_request accepts valid GET http request."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    assert parse_request(req) == b'/index.html'


def test_request_parse_invalid_missing_host_header():
    """Test for invalid missing host header."""
    req = b'GET /index.html HTTP/1.1\r\n\
From: frog@j.money.com\r\n\
User-Agent: Mozilla/3.0Gold\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_number_of_lines():
    """Test if not three lines in request, raises ValueError."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_line_formatting():
    """Test if line is properly formatted with carriage returns."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
DATE:\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_method_uri_protocol_line_formatting():
    """Test if the first line of req is properly formatted with white space."""
    req = b'GET / index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


@pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'get'])
def test_request_parse_invalid_method_is_not_get(method):
    """Test if the method is for a GET request."""
    req = '{} /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'.format(method).encode('utf8')
    with pytest.raises(NotImplementedError):
        parse_request(req)


@pytest.mark.parametrize('protocol', ['HTTP/1.2', 'HTTP/1.0', 'HTTP',
                                      'http/1.1'])
def test_request_parse_invalid_protocol_is_not_http_11(protocol):
    """Test if the protocol is for HTTP/1.1."""
    req = 'GET /index.html {}\r\n\
Host: www.example.com\r\n\
\r\n'.format(protocol).encode('utf8')
    with pytest.raises(NotImplementedError):
        parse_request(req)


def test_request_parse_invalid_uri_is_not_file_path():
    """Test if the uri is a valid file path."""
    req = b'GET index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_left_justified_header_name():
    """Test if the header name is left justifiied."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
    Content-Type: text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_missing_colon_header_name():
    """Test if the header name is missing a colon."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com\r\n\
Content-Type : text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_request_parse_invalid_url_for_host_value():
    """Test if the URL for the Host uses proper characters."""
    req = b'GET /index.html HTTP/1.1\r\n\
Host: www.example.com!\r\n\
Content-Type: text/plain\r\n\
\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_resolve_uri_html_directory():
    """Test if returns HTML file, with the contents of a sub-directory."""
    assert resolve_uri('') == (b'<!DOCTYPE html>\n<html>\n<body>\nhtml.html\njam.png\nanother.txt\n</body>\n</html>\n', 'text/html')
