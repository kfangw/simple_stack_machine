class ASTNode(object):
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

    def dump(self):
        return '[Col:{0}]-[Node:{1}]-[Lexeme:{2}]'.format(
            self.pos,
            self.__class__.__name__,
            self.val,
        )


class TopAST(ASTNode):
    def __init__(self, pos):
        super(TopAST, self).__init__(pos, '')
        self.nodes = []

    def dump(self):
        return '\n'.join(
            node.dump() for node in self.nodes
        )


class ExprAST(ASTNode):
    def __init__(self, pos, val):
        super(ExprAST, self).__init__(pos, val)


class NumberExprAST(ExprAST):
    def __init__(self, val, pos):
        super(NumberExprAST, self).__init__(pos, val)


class StatementAST(ASTNode):
    def __init__(self, pos, val):
        super(StatementAST, self).__init__(pos, val)


class StmtAddAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtAddAST, self).__init__(pos, val)


class StmtSubAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtSubAST, self).__init__(pos, val)


class StmtPushAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtPushAST, self).__init__(pos, val)
        self.number = None

    def dump(self):
        return super(StmtPushAST, self).dump() + '\n' + '\t' + self.number.dump()


class StmtDupAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtDupAST, self).__init__(pos, val)


class StmtDropAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtDropAST, self).__init__(pos, val)


class StmtPrintAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtPrintAST, self).__init__(pos, val)
