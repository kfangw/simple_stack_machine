import logging

from err import LexError
from stack_machine.constants import TokenKind, Token

logger = logging.getLogger(__name__)


class Lexer(object):
    def __init__(self, buf):
        assert len(buf) >= 1
        self.buf = buf
        self.pos = 0
        self.c = self.buf[0]

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
        while self.c:
            # Skip whitespace
            while self.c.isspace():
                self._advance()
            # Keyword
            if self.c.isalpha():
                keyword_str = ''
                while self.c.isalpha():
                    keyword_str += self.c
                    self._advance()
                if keyword_str in self._keyword_map:
                    yield Token(kind=self._keyword_map[keyword_str], value=keyword_str, pos=self.pos)
            # Number
            elif self.c.isdigit():
                num_str = ''
                while self.c.isdigit():
                    num_str += self.c
                    self._advance()
                yield Token(kind=TokenKind.NUMBER, value=num_str, pos=self.pos)
            elif self.c:
                raise LexError('Unknown Token at pos:{0}'.format(self.pos))
        yield Token(kind=TokenKind.EOF, value='', pos=self.pos)

    def _advance(self):
        try:
            self.pos += 1
            self.c = self.buf[self.pos]
        except IndexError:
            self.c = ''
