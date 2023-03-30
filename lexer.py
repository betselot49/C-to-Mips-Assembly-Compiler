import re
import nltk


class Lexer:
    def __init__(self, line):
        self.keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include"

        self.operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"
        self.numerals = "^(\d+)$"
        self.characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
        self.identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
        self.headers = "([a-zA-Z]+\.[h])"
        self.word = line

        """{"auto", "break", "case" "char", "const" "continue" "default", "do", "double" "else", "enum", "extern", "float", "for", "goto" "if" "int", "long", "register",
                         "return", "short", "signed", "sizeof", "static" "struct", "switch", "typedef", "union" "unsigned", "void", "volatile", "while", "string", "class", "struc", "include"}"""

    def lexe(self, Source_Code):

        output = []
        count = 0
        for line in self.word:
            count = count + 1
            if (line.startswith("#include")):
                tokens = nltk.word_tokenize(line)
            else:
                tokens = nltk.wordpunct_tokenize(line)
            temp = []
            for token in tokens:
                if (re.findall(self.keywords, token)):
                    temp.append(("keyword", token))
                elif (re.findall(self.headers, token)):
                    temp.append(("header", token))
                elif (re.findall(self.operators, token)):
                    temp.append(("operator", token))
                elif (re.findall(self.numerals, token)):
                    temp.append(("number", token))
                elif (re.findall(self.characters, token)):
                    temp.append(("character", token))
                elif (re.findall(self.identifiers, token)):
                    temp.append(("identifier", token))
            output.append(temp)

        return output
