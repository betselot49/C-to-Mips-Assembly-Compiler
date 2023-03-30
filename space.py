class Checker:
    def __init__(self, value):
        # with open(value, "r") as file:
        #     self.lines = file.readlines()
        self.lines = value
        self.code = self.removeComments()
        self.blockPass = self.blockChecker()

        # self.variables = set()
        # self.functions = set()

    def returns(self):
        if self.blockPass:
            return self.code
        return False

    def removeComments(self):  # removes comment, white spaces and header files
        answer = []
        block = False
        comment = False
        temp = []
        temp2 = []
        i, j = 0, 0
        while i < len(self.lines):
            line = self.lines[i]
            if line[0] == "#":
                line = "\n"
            if line[-1] == "\n":
                line = line[:-1]
            j = 0
            temp = []
            while j < len(line):
                word = line[j]
                j += 1
                if block:
                    if word == "*" and line[j] == "/":
                        temp, temp2 = temp2, []
                        block = False
                        j += 1
                    continue
                elif word == "/" and j < len(line):
                    if line[j] == "*":
                        temp2, temp = temp, []
                        block = True
                        j += 1
                        continue
                    elif line[j] == "/":
                        break
                temp.append(word)
            appended = "".join(temp).strip()
            if appended:
                answer.append(appended)
            i += 1
        return answer

    def blockChecker(self):   # checks the correct block element is done
        stack = []
        blockElements = {"{", "(", "["}
        equiv = {"]": "[", ")": "(", "}": "{"}
        for line in (self.code):
            for word in (line):
                if word in blockElements:
                    stack.append(word)
                elif word in equiv:
                    if not stack or stack.pop() != equiv[word]:
                        return False
        return len(stack) == 0


# x = Checker("c.c")
# print(x.code)
