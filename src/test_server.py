"""Test server."""
import pytest
from client import main


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


<<<<<<< HEAD
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


=======
>>>>>>> master
def test_message_shorter_than_one_buffer():
    """Test_message_shorter_than_one_buffer."""
    message = "A"
    res = main(message)
    assert len(res) == 1


def test_message_several_buffers():
    """Test_message_several_buffers."""
    message = "Hello World this is a test"
    res = main(message)
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
<<<<<<< HEAD

    # assert len(non_ascii1) == 1
    # assert len(non_ascii2) == 1
=======
    non_ascii1 = 'é'
    non_ascii2 = '¨'
    assert len(non_ascii1) == 1
    assert len(non_ascii2) == 1
>>>>>>> master
