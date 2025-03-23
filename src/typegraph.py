import sys, os

def report(header : str, cause : str):
    print(f"Fatal exception reported:\n {header} : {cause}")
    sys.exit(-1)

class MapleType:
    def __init__(self, value):
        self.regname = "UNKNOWN"
        self.value = value

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

class MapleFLOAT(MapleType):
    def __init__(self, value : float):
        self.regname = "FLOAT"
        self.value = value

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

class MapleINT(MapleType):
    def __init__(self, value : int):
        self.regname = "INT"
        self.value = value

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

class MapleSTRING(MapleType):
    def __init__(self, value : str):
        self.regname = "STRING"
        self.value = value

    def op_plus(self, other):
        if not isinstance(other, (MapleSTRING)):
            report("TypeException", f"{self.regname} and {other.regname} don't support PLUS operations together.")
        return MapleSTRING(self.value + other.value)

class MapleBOOLEAN(MapleType):
    def __init__(self, value : bool):
        self.regname = "BOOLEAN"
        self.value = value

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