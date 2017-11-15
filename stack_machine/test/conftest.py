import os

import pytest


@pytest.fixture(scope="function")
def clean_up_files():

    yield
    os.remove("test.ll")
    os.remove("test.s")
    os.remove("test_exec")
    os.remove("test_result")