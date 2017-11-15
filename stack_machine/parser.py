from stack_machine.ast import TopAST, NumberExprAST, StmtNopAST, StmtDropAST, StmtDupAST, StmtPushAST, StmtNotAST, \
    StmtXorAST, StmtOrAST, StmtAndAST, StmtSubAST, StmtAddAST
from stack_machine.constants import TokenKind
from stack_machine.err import ParseError
from stack_machine.lexer import Lexer


class Parser(object):

    def __init__(self):
        self.token_generator = None
        self.cur_tok = None

    # top ::= ( statement | expression )+
    def parse_toplevel(self, buf):
        self.token_generator = Lexer(buf).tokens()
        self.cur_tok = None
        top = TopAST(0)
        while self._get_next_token():
            if self.cur_tok.kind == TokenKind.NUMBER:
                top.nodes.append(self._parse_number())
            else:
                top.nodes.append(self._parse_statement())
        return top

    def _parse_number(self):
        return NumberExprAST(self.cur_tok.value, self.cur_tok.pos)

    def _parse_statement(self):
        if self.cur_tok.kind == TokenKind.NOP:
            return self._parse_nop_statement()
        elif self.cur_tok.kind == TokenKind.ADD:
            return self._parse_add_statement()
        elif self.cur_tok.kind == TokenKind.SUB:
            return self._parse_sub_statement()
        elif self.cur_tok.kind == TokenKind.AND:
            return self._parse_and_statement()
        elif self.cur_tok.kind == TokenKind.OR:
            return self._parse_or_statement()
        elif self.cur_tok.kind == TokenKind.XOR:
            return self._parse_xor_statement()
        elif self.cur_tok.kind == TokenKind.NOT:
            return self._parse_not_statement()
        elif self.cur_tok.kind == TokenKind.PUSH:
            return self._parse_push_statement()
        elif self.cur_tok.kind == TokenKind.DUP:
            return self._parse_dup_statement()
        elif self.cur_tok.kind == TokenKind.DROP:
            return self._parse_drop_statement()
        return ''

    def _parse_nop_statement(self):
        return StmtNopAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_add_statement(self):
        return StmtAddAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_sub_statement(self):
        return StmtSubAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_and_statement(self):
        return StmtAndAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_or_statement(self):
        return StmtOrAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_xor_statement(self):
        return StmtXorAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_not_statement(self):
        return StmtNotAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_push_statement(self):
        push_statement = StmtPushAST(self.cur_tok.pos, self.cur_tok.value)
        self._get_next_token()
        if self.cur_tok.kind != TokenKind.NUMBER:
            raise ParseError("{0} push should be followed by number".format(push_statement.dump()))
        number_expr = self._parse_number()
        push_statement.number = number_expr
        return push_statement

    def _parse_dup_statement(self):
        return StmtDupAST(self.cur_tok.pos, self.cur_tok.value)

    def _parse_drop_statement(self):
        return StmtDropAST(self.cur_tok.pos, self.cur_tok.value)

    def _get_next_token(self):
        self.cur_tok = next(self.token_generator)
        if self.cur_tok.kind == TokenKind.EOF:
            return False
        return True
