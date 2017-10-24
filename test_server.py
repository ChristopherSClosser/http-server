"""Test server."""
import pytest
from client import main


def test_valid_client_string():
    """test_valid_client_string."""
    message = "This is a test message"
    res = main(message)
    print('this is what main(message) returns: ', res)
    assert res == 22


def test_case_fail():
    """test_case_fail."""
    with pytest.raises(Exception):
        main()
