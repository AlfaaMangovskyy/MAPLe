from static import *

if __name__ == "__main__":
    while True:
        text = input("MAPLe Bash > ")
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        print(tokens)

        parser = Parser(tokens)
        ast = parser.parse()
        print(ast)

        inter = Interpreter(ast)
        ret = inter.run()
        print(ret)