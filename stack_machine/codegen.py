import logging

from llvmlite import ir, binding

logger = logging.getLogger(__name__)


class CodeGen(object):
    def __init__(self):
        self.mod = ir.Module()
        self.mod.triple = binding.get_default_triple()
        self.builder = None

    def _codegen(self, node):

        method = '_codegen_' + node.__class__.__name__
        return getattr(self, method)(node)

    def codegen_TopAST(self, node, test=False):

        fnty = ir.FunctionType(ir.IntType(64), ())
        func = ir.Function(self.mod, fnty, "main")
        bb_entry = func.append_basic_block("entry")
        self.builder = ir.IRBuilder(bb_entry)

        self._declare_stack()
        self._declare_stack_pointer()

        for stmt in node.nodes:
            self._codegen(stmt)
        # self._stack_dump()

        stack = self.mod.globals["stack"]
        sp = self.mod.globals["sp"]
        sp_value = self.builder.load(sp)
        new_sp_value = self.builder.sub(sp_value, ir.Constant(ir.IntType(64), 1))
        stack_addr = self.builder.gep(stack, [ir.Constant(ir.IntType(64), 0), new_sp_value], inbounds=True)
        stack_addr_value = self.builder.load(stack_addr)
        # if test:
        #     self._call_printf("[sp:%ld][value:%ld]", new_sp_value, stack_addr_value)

        self.builder.ret(stack_addr_value)

        return self.mod

    def _codegen_NumberExprAST(self, node):
        return ir.Constant(ir.IntType(64), int(node.val))

    def _codegen_StmtAddAST(self, node):
        right_value = self._stack_peek()
        self._stack_pop()
        left_value = self._stack_peek()
        self._stack_pop()
        result_value = self.builder.add(left_value, right_value)
        self._stack_push(result_value)

    def _codegen_StmtSubAST(self, node):
        right_value = self._stack_peek()
        self._stack_pop()
        left_value = self._stack_peek()
        self._stack_pop()
        result_value = self.builder.sub(left_value, right_value)
        self._stack_push(result_value)

    def _codegen_StmtPushAST(self, node):
        number = self._codegen(node.number)
        self._stack_push(number)

    def _codegen_StmtDupAST(self, node):
        top_value = self._stack_peek()
        self._stack_push(top_value)

    def _codegen_StmtDropAST(self, node):
        self._stack_pop()

    def _codegen_StmtPrintAST(self, node):
        stack = self.mod.globals["stack"]
        sp = self.mod.globals["sp"]
        sp_value = self.builder.load(sp)
        new_sp_value = self.builder.sub(sp_value, ir.Constant(ir.IntType(64), 1))
        stack_addr = self.builder.gep(stack, [ir.Constant(ir.IntType(64), 0), new_sp_value], inbounds=True)
        stack_addr_value = self.builder.load(stack_addr)
        self._call_printf("[sp:%ld][value:%ld]", new_sp_value, stack_addr_value)


    @staticmethod
    def _make_byte_array(buf):
        b = bytearray(buf)
        n = len(b)
        return ir.Constant(ir.ArrayType(ir.IntType(8), n), b)

    def _global_constant(self, name, value):
        if name in self.mod.globals:
            return self.mod.globals[name]
        data = ir.GlobalVariable(self.mod, value.type, name=name)
        data.global_constant = True
        data.initializer = value
        return data

    def _declare_printf(self):
        if self.mod.globals.get("printf"):
            fn = self.mod.globals["printf"]
        else:
            fnty = ir.FunctionType(ir.IntType(32), (ir.PointerType(ir.IntType(8)),), var_arg=True)
            fn = ir.Function(self.mod, fnty, "printf")
            self.mod.globals["printf"] = fn
        return fn

    def _call_printf(self, print_format="", *args):
        fn = self._declare_printf()
        cstring = ir.IntType(8).as_pointer()

        value = self._make_byte_array((print_format + '\00').encode('ascii'))
        count = 0
        while self.mod.globals.get("{0}_{1}".format("printf_format", count)):
            count += 1
        data = self._global_constant("{0}_{1}".format("printf_format", count), value)
        self.mod.globals["{0}_{1}".format("printf_format", count)] = data

        ptr_fmt = self.builder.bitcast(data, cstring)
        self.builder.call(fn, [ptr_fmt] + list(args))

    def _declare_stack(self):
        stack = ir.GlobalVariable(self.mod, ir.ArrayType(ir.IntType(64), 1000), name="stack")
        value = ir.Constant(ir.ArrayType(ir.IntType(64), 1000), [0] * 1000)
        stack.initializer = value
        self.mod.globals["stack"] = stack

    def _declare_stack_pointer(self):
        sp = ir.GlobalVariable(self.mod, ir.IntType(64), name="sp")
        value = ir.Constant(ir.IntType(64), 0)
        sp.initializer = value
        self.mod.globals["sp"] = sp

    def _stack_push(self, value=None):
        stack = self.mod.globals["stack"]
        sp = self.mod.globals["sp"]
        sp_value = self.builder.load(sp)
        stack_addr = self.builder.gep(stack, [ir.Constant(ir.IntType(64), 0), sp_value], inbounds=True)
        self.builder.store(value, stack_addr)
        new_sp_value = self.builder.add(sp_value, ir.Constant(ir.IntType(64), 1))
        self.builder.store(new_sp_value, sp)

    def _stack_peek(self):
        stack = self.mod.globals["stack"]
        sp = self.mod.globals["sp"]
        sp_value = self.builder.load(sp)
        new_sp_value = self.builder.sub(sp_value, ir.Constant(ir.IntType(64), 1))
        stack_addr = self.builder.gep(stack, [ir.Constant(ir.IntType(64), 0), new_sp_value], inbounds=True)
        stack_addr_value = self.builder.load(stack_addr)

        return stack_addr_value

    def _stack_pop(self):
        sp = self.mod.globals["sp"]
        sp_value = self.builder.load(sp)
        new_sp_value = self.builder.sub(sp_value, ir.Constant(ir.IntType(64), 1))
        self.builder.store(new_sp_value, sp)

    def _stack_dump(self):  # This method is only for debugging
        sp = ir.Constant(ir.IntType(64), 0)
        stack = self.mod.globals["stack"]
        sp_value = sp
        for _ in range(100):
            stack_addr = self.builder.gep(stack, [ir.Constant(ir.IntType(64), 0), sp_value], inbounds=True)
            stack_value = self.builder.load(stack_addr)
            self._call_printf("[%2ld]-[%5ld]\n", sp_value, stack_value)
            sp_value = self.builder.add(sp_value, ir.Constant(ir.IntType(64), 1))
