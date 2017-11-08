from stack_machine.lexer import Lexer


def test_lexer():
    lexer = Lexer("1 2 ADD 3 SUB AAA")
    for lexeme in lexer.tokens():
        print (lexeme)
