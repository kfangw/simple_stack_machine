import logging

import os

import pytest

from stack_machine.codegen import CodeGen
from stack_machine.parser import Parser

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("clean_up_files")
@pytest.mark.parametrize("input_str,expected", [
    ("push 1 push 2 push 3 print",                  "[sp:2][value:3]"),
    ("push 1 push 2 add print",                     "[sp:0][value:3]"),
    ("push 1 push 2 sub print",                     "[sp:0][value:-1]"),
    ("push 1 push 2 dup print",                     "[sp:2][value:2]"),
    ("push 1 push 2 drop print",                    "[sp:0][value:1]"),
    ("push 1 print",                                "[sp:0][value:1]"),
    ("push 1 push 2 print",                         "[sp:1][value:2]"),
    ("push 1 push 2 add print",                     "[sp:0][value:3]"),
    ("push 1 push 2 add push 3 print",              "[sp:1][value:3]"),
    ("push 1 push 2 add push 3 sub print",          "[sp:0][value:0]"),
    ("push 1 push 2 add push 3 sub push 4 print",   "[sp:1][value:4]"),
])
def test_parser(input_str, expected):
    parser = Parser()
    logger.info(input_str)
    top = parser.parse_toplevel(input_str)
    codegen = CodeGen()
    mod = codegen.codegen_TopAST(top, test=True)
    ll_file = open("test.ll", "w")
    ll_file.write(repr(mod))
    ll_file.close()

    os.system("llc test.ll")
    os.system("gcc test.s -o test_exec")
    os.system("./test_exec > test_result")
    test_result_file = open("test_result", "r")
    test_result = test_result_file.readline()
    test_result_file.close()
    assert test_result == expected

