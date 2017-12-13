"""Test server."""
import pytest
from client import client


def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message\r\n\r\n"
    res = client(message)
    assert 'HTTP/1.1 200 OK\r\n' in res


def test_response_error():
    """Test if server response with HTTP 500 Internal Server Error."""
    from server import response_error
    res = response_error()
    assert b'HTTP/1.1 500 Internal Server Error\r\nDate:' in res


def test_response_logs():
    """test_response_logs."""
    message = "This is a test message\r\n\r\n"
    # import pdb; pdb.set_trace()
    res = client(message)
    # response_logs(message)
    # assert


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


def test_case_fail():
    """test_case_fail."""
    with pytest.raises(Exception):
        client()
