import logging

import os

import pytest

from stack_machine.ast import TopAST, NumberExprAST, StmtNopAST, StmtDropAST, StmtDupAST, StmtPushAST, StmtNotAST, \
    StmtXorAST, StmtOrAST, StmtAndAST, StmtSubAST, StmtAddAST
from stack_machine.codegen import CodeGen
from stack_machine.parser import Parser

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("clean_up_files")
@pytest.mark.parametrize("input_str,expected", [
    ("push 1 push 2 push 3", "[sp:2][value:3]"),
    ("push 1 push 2 add", "[sp:0][value:3]"),
    ("push 1 push 2 sub", "[sp:0][value:-1]"),
    ("push 1 push 2 and", "[sp:0][value:0]"),
    ("push 1 push 3 and", "[sp:0][value:1]"),
    ("push 1 push 2 or", "[sp:0][value:3]"),
    ("push 1 push 3 or", "[sp:0][value:3]"),
    ("push 1 push 4 or", "[sp:0][value:5]"),
    ("push 1 push 2 xor", "[sp:0][value:3]"),
    ("push 1 push 3 xor", "[sp:0][value:2]"),
    ("push 1 push 3 not", "[sp:1][value:-4]"),
    ("push 1 push 2 dup", "[sp:1][value:2]"),
    ("push 1 push 2 drop", "[sp:0][value:1]"),
])
def test_parser(input_str, expected):
    parser = Parser()
    logger.info(input_str)
    top = parser.parse_toplevel(input_str)
    codegen = CodeGen()
    mod = codegen.codegen_TopAST(top)
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

