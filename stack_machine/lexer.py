from stack_machine.constants import TokenKind, Token

from err import LexError


class Lexer(object):
    """Lexer for Kaleidoscope.

    Initialize the lexer with a string buffer. tokens() returns a generator that
    can be queried for tokens. The generator will emit an EOF token before
    stopping.
    """

    def __init__(self, buf):
        assert len(buf) >= 1
        self.buf = buf
        self.pos = 0
        self.lastchar = self.buf[0]

        self._keyword_map = {
            'nop': TokenKind.NOP,
            'add': TokenKind.ADD,
            'sub': TokenKind.SUB,
            'and': TokenKind.AND,
            'or': TokenKind.OR,
            'xor': TokenKind.XOR,
            'not': TokenKind.NOT,
            'push': TokenKind.PUSH,
            'dup': TokenKind.DUP,
            'drop': TokenKind.DROP,
        }

    def tokens(self):
        while self.lastchar:
            # Skip whitespace
            while self.lastchar.isspace():
                self._advance()
            # Keyword
            if self.lastchar.isalpha():
                id_str = ''
                while self.lastchar.isalpha():
                    id_str += self.lastchar
                    self._advance()
                if id_str in self._keyword_map:
                    yield Token(kind=self._keyword_map[id_str], value=id_str)
            # Number
            elif self.lastchar.isdigit():
                num_str = ''
                while self.lastchar.isdigit():
                    num_str += self.lastchar
                    self._advance()
                yield Token(kind=TokenKind.NUMBER, value=num_str)
            elif self.lastchar:
                raise LexError('Unknown Token at pos:{0}'.format(self.pos))
        yield Token(kind=TokenKind.EOF, value='')

    def _advance(self):
        try:
            self.pos += 1
            self.lastchar = self.buf[self.pos]
        except IndexError:
            self.lastchar = ''
