from pycparser import c_parser, c_generator, c_ast, parse_file
import generate

ast = parse_file("decl.h")
vis = generate.FuncDefVisitor()
vis.visit(ast)

inargs, outargs, code = generate.concat(vis.func, ["push3", "dup", "add", "add"])
fn = generate.fndecl('test', inargs, outargs, code)

print(vis.gen.visit(fn))
