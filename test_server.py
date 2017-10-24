import pytest

def test_valid_client_string():
    from client import main
    assert main("This is a test message") != None