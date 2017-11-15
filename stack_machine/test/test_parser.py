import logging

from stack_machine.ast import TopAST, NumberExprAST, StmtNopAST, StmtDropAST, StmtDupAST, StmtPushAST, StmtNotAST, \
    StmtXorAST, StmtOrAST, StmtAndAST, StmtSubAST, StmtAddAST
from stack_machine.parser import Parser

logger = logging.getLogger(__name__)


def test_parser():
    input_str = "nop push 1 push 2 add push 3 sub push 4 and push 5 or push 6 xor not dup drop push 1"
    parser = Parser()
    top = parser.parse_toplevel(input_str)
    assert isinstance(top, TopAST)
    assert isinstance(top.nodes[0], StmtNopAST)
    assert isinstance(top.nodes[1], StmtPushAST)
    # assert isinstance(top.nodes[2], NumberExprAST)
    assert isinstance(top.nodes[2], StmtPushAST)
    # assert isinstance(top.nodes[4], NumberExprAST)
    assert isinstance(top.nodes[3], StmtAddAST)
    assert isinstance(top.nodes[4], StmtPushAST)
    # assert isinstance(top.nodes[7], NumberExprAST)
    assert isinstance(top.nodes[5], StmtSubAST)
    assert isinstance(top.nodes[6], StmtPushAST)
    # assert isinstance(top.nodes[10], NumberExprAST)
    assert isinstance(top.nodes[7], StmtAndAST)
    assert isinstance(top.nodes[8], StmtPushAST)
    # assert isinstance(top.nodes[13], NumberExprAST)
    assert isinstance(top.nodes[9], StmtOrAST)
    assert isinstance(top.nodes[10], StmtPushAST)
    # assert isinstance(top.nodes[16], NumberExprAST)
    assert isinstance(top.nodes[11], StmtXorAST)
    assert isinstance(top.nodes[12], StmtNotAST)
    assert isinstance(top.nodes[13], StmtDupAST)
    assert isinstance(top.nodes[14], StmtDropAST)
    assert isinstance(top.nodes[15], StmtPushAST)
    # assert isinstance(top.nodes[22], NumberExprAST)
