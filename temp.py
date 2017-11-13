from llvmlite import ir, binding

def main():
    # Create some useful types
    fnty = ir.FunctionType(ir.IntType(64), ())

    # Create an empty module...
    module = ir.Module(name=__file__)
    # and declare a function named "fpadd" inside it

    func = ir.Function(module, fnty, name="main")

    # Now implement the function
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    int10 = ir.Constant(ir.IntType(64), 10)
    cc = builder.add(int10, int10)
    dd = builder.add(int10, cc)

    module.triple = binding.get_default_triple()

    printf(module, builder, "value test : %d\n", cc)
    printf(module, builder, "value test : %d\n", cc)
    builder.ret(ir.Constant(ir.IntType(64), 0))

    print(module)


def make_byte_array(buf):
    b = bytearray(buf)
    n = len(b)
    return ir.Constant(ir.ArrayType(ir.IntType(8), n), b)


def global_constant(module, name, value):
    if name in module.globals:
        return module.globals[name]
    data = ir.GlobalVariable(module, value.type, name=name)
    data.global_constant = True
    data.initializer = value
    return data


def printf(module, builder, print_format="", *args):
    if module.globals.get("printf"):
        fn = module.globals["printf"]
    else:
        fnty = ir.FunctionType(ir.IntType(32), (ir.PointerType(ir.IntType(8)), ), var_arg=True)
        fn = ir.Function(module, fnty, "printf")
        module.globals["printf"] = fn
    # Make global constant for format string
    cstring = ir.IntType(8).as_pointer()

    value = make_byte_array((print_format + '\00').encode('ascii'))
    count = 0
    while module.globals.get("{0}_{1}".format("printf_format", count)):
        count += 1
    data = global_constant(module, "{0}_{1}".format("printf_format", count), value)
    module.globals["{0}_{1}".format("printf_format", count)] = data

    ptr_fmt = builder.bitcast(data, cstring)
    builder.call(fn, [ptr_fmt] + list(args))


if __name__ == "__main__":
    main()
