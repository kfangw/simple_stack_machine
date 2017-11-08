from stack_machine.constants import TokenKind
from stack_machine.lexer import Lexer


def test_lexer():
    lexer = Lexer("nop 1 add 2 sub 3 and 4 or xor 5 not push dup 8 drop 10")
    lexeme_list = [lexeme for lexeme in lexer.tokens()]
    assert lexeme_list[0].kind == TokenKind.NOP
    assert lexeme_list[1].kind == TokenKind.NUMBER
    assert lexeme_list[2].kind == TokenKind.ADD
    assert lexeme_list[3].kind == TokenKind.NUMBER
    assert lexeme_list[4].kind == TokenKind.SUB
    assert lexeme_list[5].kind == TokenKind.NUMBER
    assert lexeme_list[6].kind == TokenKind.AND
    assert lexeme_list[7].kind == TokenKind.NUMBER
    assert lexeme_list[8].kind == TokenKind.OR
    assert lexeme_list[9].kind == TokenKind.XOR
    assert lexeme_list[10].kind == TokenKind.NUMBER
    assert lexeme_list[11].kind == TokenKind.NOT
    assert lexeme_list[12].kind == TokenKind.PUSH
    assert lexeme_list[13].kind == TokenKind.DUP
    assert lexeme_list[14].kind == TokenKind.NUMBER
    assert lexeme_list[15].kind == TokenKind.DROP
    assert lexeme_list[16].kind == TokenKind.NUMBER
    assert lexeme_list[17].kind == TokenKind.EOF

