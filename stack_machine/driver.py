import os

from stack_machine.codegen import CodeGen
from stack_machine.parser import Parser

import logging

logger = logging.getLogger(__name__)


class Driver(object):
    def __init__(self, base_dir, input_file_name, output_file_name, keep_ir=False):
        self.base_dir = base_dir
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.keep_ir = keep_ir

    def codegen(self):
        parser = Parser()
        input_file = open(self.input_file_name, "r")
        input_str = input_file.readline()
        logger.info(input_str)
        top = parser.parse_toplevel(input_str)
        codegen = CodeGen()
        mod = codegen.codegen_TopAST(top)
        ll_file = open("{0}.ll".format(self.input_file_name), "w")
        ll_file.write(repr(mod))
        ll_file.close()

    def llc_compile(self):
        os.system("llc {0}".format("{0}.ll".format(self.input_file_name)))
        os.system("gcc {0}.s -o {1}".format(self.input_file_name, self.output_file_name))

    def compile(self):
        self.codegen()
        self.llc_compile()
        self.clean_up()

    def clean_up(self):
        if not self.keep_ir:
            os.remove("{0}.ll".format(self.input_file_name))
            os.remove("{0}.s".format(self.input_file_name))
