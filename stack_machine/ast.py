class ASTNode(object):
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

    def dump(self):
        return '{0}[{1}]'.format(
            self.__class__.__name__, self.val
        )


class TopAST(ASTNode):
    def __init__(self, pos):
        super(TopAST, self).__init__(pos, '')
        self.nodes = []

    def dump(self):
        return '\n'.join(
            '{0}[{1}]'.format(
                node.__class__.__name__, node.val
            ) for node in self.nodes
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


class StmtNopAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtNopAST, self).__init__(pos, val)


class StmtAddAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtAddAST, self).__init__(pos, val)


class StmtSubAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtSubAST, self).__init__(pos, val)


class StmtAndAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtAndAST, self).__init__(pos, val)


class StmtOrAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtOrAST, self).__init__(pos, val)


class StmtXorAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtXorAST, self).__init__(pos, val)


class StmtNotAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtNotAST, self).__init__(pos, val)


class StmtPushAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtPushAST, self).__init__(pos, val)


class StmtDupAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtDupAST, self).__init__(pos, val)


class StmtDropAST(StatementAST):
    def __init__(self, pos, val):
        super(StmtDropAST, self).__init__(pos, val)

