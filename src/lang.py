from static import *

# if __name__ == "__main__":
#     while True:
#         text = input("MAPLe Bash > ")
#         lexer = Lexer(text)
#         tokens = lexer.tokenize()
#         print(tokens)

#         parser = Parser(tokens)
#         ast = parser.parse()
#         print(ast)

#         inter = Interpreter(ast)
#         ret = inter.run()
#         print(ret)

import sys

if len(sys.argv) > 1:
    path = sys.argv[1]

    with open(path, "r") as source:
        script = source.read()
        source.close()

    lexer = Lexer(script)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    inter = Interpreter(ast)
    returned = inter.run()

    print(returned)