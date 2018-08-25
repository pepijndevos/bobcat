from pycparser import c_parser, c_generator, c_ast, parse_file
import generate
import parser

ast = parse_file("decl.h", use_cpp=True, cpp_path='gcc', cpp_args=['-E'])
vis = generate.FuncDefVisitor()
vis.visit(ast)

code = """
squarei: [dupi muli]
dropi dupi
absi, squarei, squarei
addi, idi
swapi
subi
"""

code = """
seq(success success running)
"""

ast = parser.parser.parse(code)
decl_code = []
generate.compile_ast(vis.func, decl_code, ast, 'test')

gen = c_generator.CGenerator()
for f in decl_code:
    print(gen.visit(f))

