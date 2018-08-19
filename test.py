from pycparser import c_parser, c_generator, c_ast, parse_file
import generate
import parser

ast = parse_file("decl.h")
vis = generate.FuncDefVisitor()
vis.visit(ast)

code = """
square: [dup mul]
drop dup
abs, square, square
add, id
swap
sub
"""

ast = parser.parser.parse(code)
decl_code = []
generate.compile_ast(vis.func, decl_code, ast, 'test')

gen = c_generator.CGenerator()
for f in decl_code:
    print(gen.visit(f))

