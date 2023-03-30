class Generator:
    def __init__(self, value) -> None:
        self.tokens = value
        self.datatype = {
            "char": ".byte",
            "int": ".word",
            "float": ".float"
        }
        self.operator = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div"
        }
        self.equalities = {
            "==": "eq",
            "!=": "ne",
            "<=": "le",
            ">=": "ge",
            "<": "lt",
            ">": "gt"
        }
        self.inverse = {
            "==": "ne",
            "!=": "eq",
            "<=": "gt",
            ">=": "lt",
            "<": "ge",
            ">": "le"
        }
        self.io = {"input", "output"}
        self.syscall = {
            "int": 1,
            "float": 2,
            "double": 3,
            "char": 4
        }
        self.size = {
            "char": 1,
            "int": 4,
            "float": 4,
            "double": 8
        }

        self.declared = set()
        self.datasection = ['.data\n']
        self.mainsection = [".text", "\n", "\t.main\n"]
        self.functions = []

    def evaluate(self, value):
        tokens = self.tokens
        if value:
            tokens = value

        for l, i in enumerate(tokens):
            # if i["block"] == "line" and i["type"] in self.io:
            #     evaled = self.inout(i)
            #     self.mainsection.append(evaled)

            # if i["block"] == "line" and i["type"] == "declaration unkown":
            #     self.datasection.append(
            #         "\t" + i["name"] + ": " + self.datatype[i["data"]] + "\n")

            if i["block"] == "line":
                self.line(i, self.mainsection)
            elif i["block"] == "if":
                if i["level"] == 0:
                    self.mainsection.append("\t\tli $t0, 0\n")
                self.ifstatment(i, self.mainsection, l)
            elif i["block"] == "while":
                self.loop(i, self.mainsection, l)

        data = "".join(self.datasection)
        main = "".join(self.mainsection)
        self.functions.append("\tend: \n")
        func = "".join(self.functions)

        return data + main + func

    def inout(self, value):
        temp = []
        if value["type"] == "output":
            if value["data"] == "int":
                temp.append("li $v0, 1 \nlw $a0, " +
                            value["name"] + "\nsyscall\n")
            elif value["data"] == "float":
                temp.append("li $v0, 2 \nlwc1 $f12, " +
                            value["name"] + "\nsyscall\n")
            elif value["data"] == "double":
                temp.append("li $v0, 3 \nlsc1 $f12, " +
                            value["name"] + "\nsyscall\n")
            elif value["data"] == "char":
                temp.append("li $v0, 11 \nlw $a0, " +
                            value["name"] + "\nsyscall\n")
        elif value["type"] == "input":
            if value["data"] == "int":
                temp.append("li $v0, 5\n" + "syscall\n" + "sw $v0, " +
                            value["name"] + "\n")
            elif value["data"] == "float":
                temp.append("li $v0, 6\n" + "syscall\n" + "\nswc1 $f0, " +
                            value["name"] + "\n")
            elif value["data"] == "float":
                temp.append("li $v0, 7 \nsw $f12, " +
                            value["name"] + "\nsyscall\n")
            elif value["data"] == "char":
                temp.append("li $v0, 12 \nsw $a0, " +
                            value["name"] + "\nsyscall\n")
        return "".join(temp)

    def ifstatment(self, block, section, l):
        cond = block["condition"]
        if cond == "last":
            section.append("\t\tbeq $t0, 0, ifState" +
                           str(l) + str(block["level"]) + "\n")
        else:
            section.append(self.condition(cond[0], 1))
            section.append(self.condition(cond[2], 2))
            section.append(
                "\t\tb" + self.equalities[cond[1][1]] + ", $t1" + ", $t2, ifState" + str(l) + str(block["level"]) + "\n")

        new = ["\tifState" + str(l) + str(block["level"]) + ":\n"]
        for i in block["lines"]:
            self.line(i, new)
        new.append("\t\tadd $t0, $t0, 1 \n")
        self.functions.append("".join(new))

    def loop(self, block, section, l):
        temp = ["\t\twhile:\n"]
        cond = block["condition"]
        temp.append("\t" + self.condition(cond[0], 1))
        temp.append("\t" + self.condition(cond[2], 2))

        temp.append(
            "\t\t\tb" + self.inverse[cond[1][1]] + ", $t1, $t2 end" "\n")

        for i in block["lines"]:
            self.line(i, temp)
        temp.append("\t\t\tj while\n")

        section.append("".join(temp))

    def condition(self, value, i):
        if value[0] == "identifier":
            return ("\t\tlw, $t" + str(i) + ", " + str(value[1]) + "\n")
        else:
            return ("\t\tli,  $t" + str(i) + ", " + str(value[1]) + "\n")

    def line(self, token, scope):
        temp = []
        if token["type"] in self.io:
            temp.append(self.inout(token))
            scope.append("".join(temp))

        elif token["type"] == "declaration unknown":
            temp.append("\t" + token["name"])
            self.declared.add(token["name"])
            temp.append(": ")
            if token["dimension"] == 1:
                temp.append(self.datatype[token["data"]] + "\n")
            else:
                if token["value"] is not None:
                    if token["data"] == "char":
                        temp.append(" .asciiz")
                        temp.append(' "' + token["value"] + '"')
                    else:
                        temp.append(" .word")
                        temp.append(" " + ",".join(token["value"]))
                else:
                    temp.append(
                        " .space " + str(token["dimension"] * self.size[token["data"]]))
                temp.append(" \n")

            self.datasection.append("".join(temp))

        elif token["type"] == "declaration" and "index" in token:

            # if token["name"] not in self.declared:
            #     temp.append("\t" + token["name"])
            #     self.declared.add(token["name"])
            #     temp.append(": ")
            #     temp.append(
            #         ".space " + str((token["dimension"] * self.size[token["data"]]) + 4))
            #     temp.append(" \n")
            #     self.datasection.append("".join(temp))
            # if "index" in token:
            scope.append(self.operate(
                token["value"], token["name"], token["data"], token["index"]))

        elif token["type"] == "declaration":
            if token["name"] not in self.declared:
                temp.append("\t" + token["name"])
                self.declared.add(token["name"])
                temp.append(": ")
                temp.append(self.datatype[token["data"]])
                temp.append(" \n")

            self.datasection.append("".join(temp))
            scope.append(self.operate(
                token["value"], token["name"], token["data"]))

    def operate(self, value, name, data, index=None):
        temp = []
        if index:
            temp.append("\t\tli $t7, " + str(index * self.size[data]) + "\n")
            if value[0][0] == "identifier":
                if data == "char":
                    temp.append("\t\tlb $t0," + value[0][1] + "\n")
                    temp.append("\t\tsb $t0, " + name + "($t7)\n")
                    return "".join(temp)
                else:
                    temp.append("\t\tlw $t0," + value[0][1] + "\n")
                    temp.append("\t\tsw $t0, " + name + "($t7)\n")
                    return "".join(temp)
            else:
                temp.append("\t\tli $t0," + value[0][1] + "\n")
                if data == "char":
                    temp.append("\t\tsb $t0, " + name + "($t7)\n")
                else:
                    temp.append("\t\tsw $t0, " + name + "($t7)\n")
                return "".join(temp)

        # for i in range(1, len(value), 2):

        elif value[0][0] == "identifier":
            if data == "char":
                temp.append("\t\tlb $t0," + value[0][1] + "\n")
                temp.append("\t\tsb $t0, " + name + "\n")
                return "".join(temp)
            else:
                temp.append("\t\tlw $t0," + value[0][1] + "\n")
        else:
            temp.append("\t\tli $t0," + value[0][1] + "\n")
        print(value)
        for i in range(1, len(value), 2):
            op, val = value[i], value[i + 1]

            if val[0] == "identifier":
                temp.append("\t\tlw $t7, " + val[1] + "\n")
                temp.append(
                    "\t\t" + self.operator[op[1]] + " $t0, $t0, $t7" + "\n")
            else:
                temp.append(
                    "\t\t" + self.operator[op[1]] + " $t0, $t0, " + val[1] + "\n")
        temp.append("\t\tsw $t0, " + name + "\n")
        return "".join(temp)
