import logging

from stack_machine.ast import TopAST, StmtDropAST, StmtDupAST, StmtPushAST, StmtSubAST, StmtAddAST
from stack_machine.parser import Parser

logger = logging.getLogger(__name__)


def test_parser():
    input_str = "push 1 push 2 add push 3 sub push 4 push 5 push 6 dup drop push 1"
    parser = Parser()
    top = parser.parse_toplevel(input_str)
    assert isinstance(top, TopAST)
    assert isinstance(top.nodes[0], StmtPushAST)
    # assert isinstance(top.nodes[2], NumberExprAST)
    assert isinstance(top.nodes[1], StmtPushAST)
    # assert isinstance(top.nodes[4], NumberExprAST)
    assert isinstance(top.nodes[2], StmtAddAST)
    assert isinstance(top.nodes[3], StmtPushAST)
    # assert isinstance(top.node[7], NumberExprAST)
    assert isinstance(top.nodes[4], StmtSubAST)
    assert isinstance(top.nodes[5], StmtPushAST)
    # assert isinstance(top.nodes[10], NumberExprAST)
    assert isinstance(top.nodes[6], StmtPushAST)
    # assert isinstance(top.nodes[13], NumberExprAST)
    assert isinstance(top.nodes[7], StmtPushAST)
    # assert isinstance(top.nodes[16], NumberExprAST)
    assert isinstance(top.nodes[8], StmtDupAST)
    assert isinstance(top.nodes[9], StmtDropAST)
    assert isinstance(top.nodes[10], StmtPushAST)
    # assert isinstance(top.nodes[22], NumberExprAST)
