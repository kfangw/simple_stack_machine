from stack_machine.constants import TokenKind
from stack_machine.lexer import Lexer


def test_lexer():
    lexer = Lexer("add 2 sub 3 push dup 8 drop 10 print")
    lexeme_list = [lexeme for lexeme in lexer.tokens()]
    assert lexeme_list[0].kind == TokenKind.ADD
    assert lexeme_list[1].kind == TokenKind.NUMBER
    assert lexeme_list[2].kind == TokenKind.SUB
    assert lexeme_list[3].kind == TokenKind.NUMBER
    assert lexeme_list[4].kind == TokenKind.PUSH
    assert lexeme_list[5].kind == TokenKind.DUP
    assert lexeme_list[6].kind == TokenKind.NUMBER
    assert lexeme_list[7].kind == TokenKind.DROP
    assert lexeme_list[8].kind == TokenKind.NUMBER
    assert lexeme_list[9].kind == TokenKind.PRINT
    assert lexeme_list[10].kind == TokenKind.EOF

