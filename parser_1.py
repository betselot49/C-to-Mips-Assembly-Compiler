class Parser:
    def __init__(self, value):
        self.token = value

        self.datatype = {"int", "char", "float", "double", "bool"}
        self.branch = {"if", "else", "else if", "while"}
        self.io = {"scanf", "printf"}
        self.declared = {}

    def analyze(self, tokens):
        i = 0
        while i < len(tokens):
            if tokens[i][0][1] == "for":

                index = 3
                if tokens[i][2][0] == "keyword":
                    index += 1
                pushed = tokens[i][2: 3 + index]
                tokens.insert(i, pushed)
                i += 1
                condition = tokens[i][3+index: 6 + index]
                increment = tokens[i][7+index: 13+index]

                whiled = [('keyword', 'while'), ('character', '(')] + \
                    condition + [('character', ')'), ('character', '{')]
                tokens[i] = whiled
                while tokens[i][0][1] != "}":
                    i += 1
                tokens.insert(i, increment)
                i += 1

            i += 1

    def evaluate(self, value):
        tokens = self.token
        if value:
            tokens = self.token

    def line(self, val=None, x=0):
        tokens = self.token
        if val:
            tokens = self.token
        self.analyze(tokens)
        output = []
        if not val:
            tokens = val
        i = 0
        n = len(tokens)
        while i < n:
            j = 0
            while i < n and tokens[i][0][1] in self.branch:
                temp = {"block": "if", "level": j}
                if tokens[i][0][1] == "while":
                    temp["block"] = "while"
                    temp["condition"] = tokens[i][2], tokens[i][3], tokens[i][4]
                elif tokens[i][0][1] == "if":
                    temp["condition"] = (
                        tokens[i][2], tokens[i][3], tokens[i][4])
                elif tokens[i][0][1] == "else" and tokens[i][1][1] == "if":
                    temp["condition"] = (
                        tokens[i][3], tokens[i][4], tokens[i][5])
                else:
                    temp["condition"] = "last"
                j += 1
                i += 1
                new = []
                while tokens[i][0][1] != "}":
                    new.append(self.lineEval(tokens[i]))
                    i += 1
                temp["lines"] = new
                output.append(temp)
            if i < n and j == 0:
                output.append(self.lineEval(tokens[i]))
            i += 1
        return output

    def lineEval(self, token):
        temp = {"block": "line"}
        if token[0][0] == "identifier" and token[0][1] in self.declared:
            token = [("keyword", self.declared[token[0][1]]["data"])] + token
        if token[0][1] in self.io:
            identify = token[-2][1]
            temp["name"] = identify
            temp["data"] = self.declared[identify]["data"]
            if token[0][1] == "scanf":
                temp["type"] = "input"
            else:
                temp["type"] = "output"
            return temp

        elif token[0][1] in self.datatype:
            if ("operator", "=") not in token:

                temp["type"] = "declaration unknown"
                temp["data"] = token[0][1]
                temp["name"] = token[1][1]
                temp["value"] = None
                temp["dimension"] = 1
                if ("character", "[") in token:
                    temp["dimension"] = self.array(token)
            else:
                temp["type"] = "declaration"
                temp["data"] = token[0][1]
                temp["name"] = token[1][1]
                temp["dimension"] = 1
                if ("character", "[]") in token:
                    mapped = self.mapper(token, temp["data"])
                    temp["type"] = "declaration unknown"
                    temp["value"] = mapped
                    temp["dimension"] = len(mapped)
                elif ("character", "[") in token:
                    temp["type"] = "declaration"
                    temp["index"] = self.array(token)
                    if temp["data"] == "char":
                        temp["value"] = token[7:len(token)-1]
                    elif temp["data"] == "float":
                        temp["value"] = token[6:len(token)-1]
                    else:
                        temp["value"] = token[6:len(token)-1]

                else:
                    if temp["data"] == "char":
                        temp["value"] = token[4:len(token)-1]
                    elif temp["data"] == "float":
                        temp["value"] = token[3:len(token)-1]
                    else:
                        temp["value"] = token[3:len(token)-1]
            self.declared[token[1][1]] = temp
            return temp

    def floatCalc(self, value):
        stack = []
        temp = []
        for i in value:
            if i[0] == "numeral" or i[0] == "character":
                temp.append(i[1])
            # else:
                # stack.append(("floa",("")

    def array(self, token):
        i = token.index(("character", "["))
        return int(token[i+1][1])

    def mapper(self, token, data):
        i = token.index(("character", "[]"))
        i += 3
        if data == "char":
            return token[i][1]
        stack = []
        while token[i][1] != "};":
            if token[i][1] != ",":
                stack.append(token[i][1])
            i += 1
        stack.pop()
        return stack
