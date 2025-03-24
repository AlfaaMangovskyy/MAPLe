import sys, os

def report(header : str, cause : str):
    print(f"Fatal exception reported:\n {header} : {cause}")
    sys.exit(-1)

class MapleType:
    def __init__(self, value):
        self.regname = "UNKNOWN"
        self.value = value
        self.storage = {}

        self.storage["__class__"] = type(self)

        for fn in dir(self):
            if fn.startswith("method_"):
                self.storage[fn.removeprefix("method_")] = MapleMETHOD(getattr(self, fn))

    def __repr__(self):
        return f"{self.regname}({self.value})"

    def op_plus(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support PLUS operations together.")

    def op_minus(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support MINUS operations together.")

    def op_mul(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support MUL operations together.")

    def op_pow(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support POW operations together.")

    def op_div(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support DIV operations together.")

    def op_mod(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support MOD operations together.")

    def op_tetr(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support TETR operations together.")

    def op_compare_or(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support logical alternative operations together.")

    def op_compare_and(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} don't support logical conjuction operations together.")

    def op_compare_not(self):
        report("TypeException", f"{self.regname} doesn't support logical negation operations.")

    def op_compare_eq(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_compare_neq(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_compare_gt(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_compare_gte(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_compare_lt(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_compare_lte(self, other):
        if not isinstance(other, MapleType):
            report("DeveloperFailureException", f"`{other}` is not a MapleType-MRO instance object.")
        report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")

    def op_invoke(self, args : list):
        report("InvokeException", f"A {self.regname}-type object can't be invoked.")

    def op_constructor(const, args : list):
        report("ConstructionException", f"This kind of object can't be constructed from program scope.")

    def op_getindex(self, index):
        report("IndexException", f"{self.regname}-type object is not indexable.")

    def op_represent(self) -> str:
        return f"<{self.regname}-type object>"

class MapleMETHOD(MapleType):
    def __init__(self, value):
        super().__init__(value)
        self.regname = "METHOD"

    def op_invoke(self, args : list):
        for arg in args:
            if not isinstance(arg, MapleType):
                report("DeveloperFailureException", f"`{arg}` is not a MapleType-MRO instance object.")
        return self.value(args)

class MapleCLASS(MapleType):
    def __init__(self, value):
        super().__init__(value)
        self.regname = "CLASS"

    def op_invoke(self, args : list):
        for arg in args:
            if not isinstance(arg, MapleType):
                report("DeveloperFailureException", f"`{arg}` is not a MapleType-MRO instance object.")
        return self.value.op_constructor(self.value, args)

class MapleFLOAT(MapleType):
    def __init__(self, value : float):
        super().__init__(value)
        self.regname = "FLOAT"

    def op_plus(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support PLUS operations together.")
        return MapleFLOAT(self.value + other.value)

    def op_minus(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MINUS operations together.")
        return MapleFLOAT(self.value - other.value)

    def op_mul(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MUL operations together.")
        return MapleFLOAT(self.value * other.value)

    def op_pow(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support POW operations together.")
        return MapleFLOAT(self.value ** other.value)

    def op_div(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support DIV operations together.")
        return MapleFLOAT(self.value / other.value)

    def op_mod(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MOD operations together.")
        return MapleINT(self.value % other.value)

    def op_tetr(self, other):
        if not isinstance(other, (MapleINT)):
            report("TypeException", f"Expected the TETR operation exponent to be INT-type, got {other.regname}.")
        result = 1
        for _ in range(other.value):
            result = self.value ** result
        return MapleFLOAT(result)

    def op_represent(self) -> str:
        return f"{self.value}f"

    def method_ratio(self, args : list[MapleType]):
        if len(args) != 0:
            report("ArgumentException", f"Expected 0 arguments, got {len(args)}.")
        return MapleARRAY([MapleINT(n) for n in self.value.as_integer_ratio()])

class MapleINT(MapleType):
    def __init__(self, value : int):
        super().__init__(value)
        self.regname = "INT"

    def op_plus(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support PLUS operations together.")
        if isinstance(other, MapleFLOAT):
            return MapleFLOAT(self.value + other.value)
        return MapleINT(self.value + other.value)

    def op_minus(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MINUS operations together.")
        if isinstance(other, MapleFLOAT):
            return MapleFLOAT(self.value - other.value)
        return MapleINT(self.value - other.value)

    def op_mul(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MUL operations together.")
        if isinstance(other, MapleFLOAT):
            return MapleFLOAT(self.value * other.value)
        return MapleINT(self.value * other.value)

    def op_pow(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support POW operations together.")
        if isinstance(other, MapleFLOAT):
            return MapleFLOAT(self.value ** other.value)
        return MapleINT(self.value ** other.value)

    def op_div(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support DIV operations together.")
        return MapleFLOAT(self.value / other.value)

    def op_mod(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} don't support MOD operations together.")
        return MapleINT(self.value % other.value)

    def op_tetr(self, other):
        if not isinstance(other, (MapleINT)):
            report("TypeException", f"Expected the TETR operation exponent to be INT-type, got {other.regname}.")
        result = 1
        for _ in range(other.value):
            result = self.value ** result
        return MapleINT(result)

    def op_compare_not(self):
        # Calculate Factorial Instead #
        result = 1
        for e in range(1, self.value + 1, 1):
            result *= e
        return MapleINT(result)

    def op_represent(self) -> str:
        return f"{self.value}"

    def op_compare_eq(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            return MapleBOOLEAN(False)
        return MapleBOOLEAN(self.value == other.value)

    def op_compare_neq(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            return MapleBOOLEAN(True)
        return MapleBOOLEAN(self.value != other.value)

    def op_compare_gt(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")
        return MapleBOOLEAN(self.value > other.value)

    def op_compare_gte(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")
        return MapleBOOLEAN(self.value >= other.value)

    def op_compare_lt(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")
        return MapleBOOLEAN(self.value < other.value)

    def op_compare_lte(self, other):
        if not isinstance(other, (MapleINT, MapleFLOAT)):
            report("TypeException", f"{self.regname} and {other.regname} can't be compared together.")
        return MapleBOOLEAN(self.value <= other.value)

class MapleSTRING(MapleType):
    def __init__(self, value : str):
        super().__init__(value)
        self.regname = "STRING"

    def op_plus(self, other):
        if not isinstance(other, (MapleSTRING)):
            report("TypeException", f"{self.regname} and {other.regname} don't support PLUS operations together.")
        return MapleSTRING(self.value + other.value)

    def op_compare_eq(self, other):
        if not isinstance(other, (MapleSTRING)):
            return MapleBOOLEAN(False)
        return MapleBOOLEAN(self.value == other.value)

    def op_compare_neq(self, other):
        if not isinstance(other, (MapleSTRING)):
            return MapleBOOLEAN(True)
        return MapleBOOLEAN(self.value != other.value)

    def op_represent(self) -> str:
        return f"{self.value}"

class MapleBOOLEAN(MapleType):
    def __init__(self, value : bool):
        super().__init__(value)
        self.regname = "BOOLEAN"

    def op_compare_or(self, other):
        if not isinstance(other, MapleBOOLEAN):
            report("TypeException", f"{self.regname} and {other.regname} don't support logical alternative operations together.")
        return MapleBOOLEAN(self.value or other.value)

    def op_compare_and(self, other):
        if not isinstance(other, MapleBOOLEAN):
            report("TypeException", f"{self.regname} and {other.regname} don't support logical conjuction operations together.")
        return MapleBOOLEAN(self.value and other.value)

    def op_compare_not(self):
        return MapleBOOLEAN(not self.value)

    def op_represent(self) -> str:
        return "true" if self.value else "false"

class MapleARRAY(MapleType):
    def __init__(self, value : list):
        super().__init__(value)
        self.regname = "ARRAY"

    def op_getindex(self, index):
        if not isinstance(index, MapleINT):
            report("TypeException", f"{self.regname}-type object's indexes must be INT-type, not {index.regname}-type.")
        if index.value > len(self.value) - 1:
            report("TypeException", f"Index `{index.value}` out of range `{len(self.value) - 1}`.")
        return self.value[index.value]

    def op_represent(self) -> str:
        return "{ " + ", ".join([n.op_represent() for n in self.value]) + " }"