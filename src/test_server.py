"""Test server."""
import pytest
from client import main
from server import server_main


def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message"
    res = main(message)
    # print('this is what main(message) returns: ', res)
    assert res == "This is a test message"


def test_case_fail():
    """test_case_fail."""
    with pytest.raises(Exception):
        main()

def test_message_shorter_than_one_buffer():
    message = "A"
    res = main(message)
    assert len(res) == 1

def test_message_several_buffers():
    message = "Hello World this is a test"
    res = main(message)
    assert len(res) > 5


def test_multiple_msg_buffers_one_length():
    msg1 = "a"
    msg2 = "b"
    msg3 = "c"
    assert len(msg1) == 1
    assert len(msg2) == 1
    assert len(msg3) == 1

def test_message_for_non_ascii():
    non_ascii1 = 'é'
    non_ascii2 = '¨'
    assert len(non_ascii1) == 1
    assert len(non_ascii2) == 1

