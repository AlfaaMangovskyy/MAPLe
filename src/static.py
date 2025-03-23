from typegraph import *

TT_INT        = "INT"
TT_FLOAT      = "FLOAT"
TT_STRING     = "STRING"

TT_PLUS       = "PLUS"
TT_MINUS      = "MINUS"
TT_MUL        = "MUL"
TT_DIV        = "DIV"
TT_POW        = "POW"
TT_MOD        = "MOD"
TT_TETR       = "TETR"
TT_ABS        = "ABS"
TT_LPAREN     = "LPAREN"
TT_RPAREN     = "RPAREN"

TT_OR         = "OR"
TT_AND        = "AND"
TT_NOT        = "NOT"

TT_KEYWORD    = "KEYWORD"
TT_NAMESPACE  = "NAMESPACE"
TT_DOT        = "DOT"
TT_EOF        = "EOF"

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

KEYWORDS = [
    "if",
    "else",
    "func",
    "for",
    "while",
]

class Token:
    def __init__(self, _type : str, value = None):
        self.type = _type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type} : {self.value}"
        return f"{self.type}"

class Lexer:
    def __init__(self, text : str):
        self.pos = -1
        self.text = text
        self.char = None
        self.advance()

        self.tokens : list[Token] = []

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.char = None
            return self.char
        self.char = self.text[self.pos]
        return self.char

    def tokenize(self):
        self.tokens.clear()

        while self.char:
            if self.char in " \n":
                self.advance()
            elif self.char == "+":
                self.tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.char == "-":
                self.advance()
                if self.char in "0123456789":
                    self.make_number(True)
                else:
                    self.tokens.append(Token(TT_MINUS))
            elif self.char == "*":
                self.advance()
                if self.char == "*":
                    self.advance()
                    if self.char == "*":
                        self.tokens.append(Token(TT_TETR))
                        self.advance()
                    else:
                        self.tokens.append(Token(TT_POW))
                else:
                    self.tokens.append(Token(TT_MUL))
            elif self.char == "/":
                self.tokens.append(Token(TT_DIV))
                self.advance()
            elif self.char == "%":
                self.tokens.append(Token(TT_MOD))
                self.advance()
            elif self.char == "|":
                self.advance()
                if self.char == "|":
                    self.tokens.append(Token(TT_OR))
                    self.advance()
                else:
                    self.tokens.append(Token(TT_ABS))
            elif self.char == "&":
                self.advance()
                if self.char == "&":
                    self.tokens.append(Token(TT_AND))
                    self.advance()
                else:
                    report("SyntaxException", "Unknown operator: `&`. Did you mean `&&`?")
            elif self.char == "(":
                self.tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.char == ")":
                self.tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.char == "!":
                self.tokens.append(Token(TT_NOT))
                self.advance()
            elif self.char in "0123456789":
                self.make_number()
            elif self.char in "'\"":
                self.make_string()
            elif self.char in ALPHABET:
                self.make_namespace()

        self.tokens.append(Token(TT_EOF))
        return self.tokens

    def make_number(self, negative : bool = False):
        num = ""
        dot = 0 # Pokemon Horizons Mentioned

        if negative:
            num += "-"

        while True:
            if self.char == ".":
                dot += 1
            if dot > 1:
                self.advance()
                break
            num += self.char
            self.advance()
            if self.char == None:
                break
            if not self.char in "0123456789.":
                break

        if dot > 0:
            self.tokens.append(Token(TT_FLOAT, float(num)))
        else:
            self.tokens.append(Token(TT_INT, int(num)))
        if dot > 1:
            self.tokens.append(Token(TT_DOT))

    def make_string(self):
        string = ""
        starter = self.char
        self.advance()

        while True:
            if self.char == None:
                report("SyntaxError", f"Expected `{starter}`")
            if self.char == starter:
                self.advance()
                break
            string += self.char
            self.advance()

        self.tokens.append(Token(TT_STRING, string))

    def make_namespace(self):
        namespace = ""

        while True:
            # print(self.char) #
            if self.char == None:
                break
            if not self.char in ALPHABET:
                break
            namespace += self.char
            self.advance()

        if namespace in KEYWORDS:
            self.tokens.append(Token(TT_KEYWORD, namespace))
        else:
            self.tokens.append(Token(TT_NAMESPACE, namespace))



class Node: pass

class NumberNode(Node):
    def __init__(self, token : Token):
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token.value}n"

class StringNode(Node):
    def __init__(self, token : Token):
        self.token = token

    def __repr__(self) -> str:
        return f"'{self.token.value}'"

class BooleanNode(Node):
    def __init__(self, token : Token):
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token.value}"

class BinOpNode(Node):
    def __init__(self, left, op : Token, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"({self.left}, {self.op}, {self.right})"

class NegationNode(Node):
    def __init__(self, node : Node):
        self.node = node

    def __repr__(self) -> str:
        return f"!({self.node})"

class AbsoluteNode(Node):
    def __init__(self, node : Node):
        self.node = node

    def __repr__(self) -> str:
        return f"|{self.node}|"



class Parser:
    def __init__(self, tokens : list[Token] = []):
        self.tokens = tokens
        self.pos = -1
        self.token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos > len(self.tokens) - 1:
            self.token = None
            return self.token
        self.token = self.tokens[self.pos]
        return self.token

    def parse(self):
        return self.logic()

    def factor(self):
        if self.token.type in (TT_INT, TT_FLOAT):
            token = self.token
            self.advance()
            return NumberNode(token)

        elif self.token.type == TT_STRING:
            token = self.token
            self.advance()
            return StringNode(token)

        elif self.token.type == TT_NOT:
            self.advance()
            return NegationNode(self.factor())

        elif self.token.type == TT_NAMESPACE:
            if self.token.value in ("true", "false"):
                token = self.token
                self.advance()
                return BooleanNode(token)

            report("NamespaceException", f"Unknown namespace: `{self.token.value}`.")

        elif self.token.type == TT_ABS:
            self.advance()
            subscript = self.expr()

            if self.token.type != TT_ABS:
                report("SyntaxError", "Expected `|` as a finish for the Absolute Value Operation.")
            self.advance()

            return AbsoluteNode(subscript)

        elif self.token.type == TT_LPAREN:
            self.advance()
            subscript = self.logic()

            if self.token.type != TT_RPAREN:
                report("SyntaxError", "Expected `)`.")
            self.advance()

            return subscript

        report("SyntaxException", "Expected a STRING, BOOLEAN, INT or FLOAT object.")

    def power(self):
        return self.binOp(self.factor, (TT_POW, TT_TETR))
    def term(self):
        return self.binOp(self.power, (TT_MUL, TT_DIV, TT_MOD))
    def expr(self):
        return self.binOp(self.term, (TT_PLUS, TT_MINUS))
    def logic(self):
        return self.binOp(self.expr, (TT_AND, TT_OR))

    def binOp(self, func, ops : list[str]):
        left = func()

        # print(self.token.type, "in", ops) #
        while self.token.type in ops:
            op = self.token
            self.advance()
            right = func()
            left = BinOpNode(left, op, right)

        return left



class Interpreter:
    def __init__(self, ast : Node):
        self.ast = ast

    def run(self):
        return self.visit(self.ast)

    def visit(self, node : Node):
        func = getattr(self, f"visit_{type(node).__name__}", self.visit_error)
        return func(node)

    def visit_error(self, node : Node):
        report("DeveloperFailureException", f"No visit method defined for `{type(node).__name__}`-type node.")

    def visit_NumberNode(self, node : NumberNode):
        if node.token.type == TT_INT:
            return MapleINT(node.token.value)
        elif node.token.type == TT_FLOAT:
            return MapleFLOAT(node.token.value)

    def visit_StringNode(self, node : StringNode):
        return MapleSTRING(node.token.value)

    def visit_BooleanNode(self, node : BooleanNode):
        return MapleBOOLEAN(True if node.token.value == "true" else False)

    def visit_BinOpNode(self, node : BinOpNode):
        left : MapleType = self.visit(node.left)
        right : MapleType = self.visit(node.right)

        if node.op.type == TT_PLUS:
            return left.op_plus(right)
        elif node.op.type == TT_MINUS:
            return left.op_minus(right)
        elif node.op.type == TT_MUL:
            return left.op_mul(right)
        elif node.op.type == TT_POW:
            return left.op_pow(right)
        elif node.op.type == TT_DIV:
            return left.op_div(right)
        elif node.op.type == TT_MOD:
            return left.op_mod(right)
        elif node.op.type == TT_TETR:
            return left.op_tetr(right)
        elif node.op.type == TT_AND:
            return left.op_compare_and(right)
        elif node.op.type == TT_OR:
            return left.op_compare_or(right)

    def visit_NegationNode(self, node : NegationNode):
        subscript : MapleType = self.visit(node.node)
        return subscript.op_compare_not()

    def visit_AbsoluteNode(self, node : AbsoluteNode):
        subscript : MapleType = self.visit(node.node)
        if isinstance(subscript, MapleINT):
            return MapleINT(abs(subscript.value))
        if isinstance(subscript, MapleFLOAT):
            return MapleFLOAT(abs(subscript.value))
        report("TypeException", f"{subscript.regname}-type object doesn't have an Absolute Value.")