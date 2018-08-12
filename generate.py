from pycparser import c_parser, c_generator, c_ast, parse_file
from copy import deepcopy

class RenameVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.sym = {}

    def visit_Decl(self, node):
        node.name = self.sym.setdefault(node.name, gensym(node.name))
        self.generic_visit(node)

    def visit_TypeDecl(self, node):
        node.declname = self.sym.setdefault(node.declname, gensym(node.declname))

class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.gen = c_generator.CGenerator()
        self.func = {}

    def visit_FuncDef(self, node):
        inargs = []
        outargs = []
        if node.decl.type.args:
            for decl in node.decl.type.args.params:
                if 'const' in decl.type.quals:
                    inargs.append(decl)
                elif isinstance(decl.type, c_ast.PtrDecl):
                    decl.type = decl.type.type
                    outargs.append(decl)
                else:
                    print("non-const, non-pointer argument, skipping", node.decl.name)
                    return
            self.func[node.decl.name] = (inargs, outargs)

def fncall(name, inargs, outargs):
    inid = [c_ast.ID(a) for a in inargs]
    outid = [c_ast.UnaryOp('&', c_ast.ID(a)) for a in outargs]
    fn = c_ast.FuncCall(c_ast.ID(name),
        c_ast.ExprList(inid + outid))
    return c_ast.If(fn, c_ast.Return(c_ast.Constant("int", "0")), None)

def fndecl(name, inargs, outargs, code):
    ptroutargs = [deepcopy(arg) for arg in outargs]
    rename = RenameVisitor()
    for arg in ptroutargs:
        rename.visit(arg)
        arg.type = c_ast.PtrDecl([], arg.type)

    fdecl = c_ast.FuncDecl(
            c_ast.ParamList(inargs+ptroutargs),
            c_ast.TypeDecl(
                name, [],
                c_ast.IdentifierType(['int'])))
    decl = c_ast.Decl(name, [], [], [], fdecl, None, None)
    assign = []
    for ptr, var in zip(ptroutargs, outargs):
        assign.append(
                c_ast.Assignment('=',
                    c_ast.UnaryOp('*', c_ast.ID(ptr.name)),
                    c_ast.ID(var.name)))

    comp = c_ast.Compound(code + assign +
            [c_ast.Return(c_ast.Constant("int", "0"))])
    return c_ast.FuncDef(decl, None, comp)
    

symidx = {}
def gensym(base='var'):
    idx = symidx.setdefault(base, 0) + 1
    symidx[base] = idx
    return "%s_%d" % (base, idx)

def concat(lookup, fns):
    gen = c_generator.CGenerator()
    stack = {}
    inargs = []
    code = []
    for fn in fns:
        rename = RenameVisitor()
        finargs, foutargs = lookup[fn]
        finnames = []
        foutnames = []

        for finarg in finargs:
            finarg = deepcopy(finarg)
            rename.visit(finarg)

            fintype = gen.visit(finarg.type)
            typestack = stack.setdefault(fintype, [])
            if len(typestack) > 0:
                a = typestack.pop()
                finnames.append(a.name)
            else:
                inargs.append(finarg)
                finnames.append(finarg.name)

        for foutarg in foutargs:
            foutarg = deepcopy(foutarg)
            rename.visit(foutarg)

            fouttype = gen.visit(foutarg.type)
            typestack = stack.setdefault(fouttype, [])
            typestack.append(foutarg)
            foutnames.append(foutarg.name)
            code.append(foutarg)

        code.append(fncall(fn, finnames, foutnames))

    outargs = [a for args in stack.values() for a in args] 
    return inargs, outargs, code

