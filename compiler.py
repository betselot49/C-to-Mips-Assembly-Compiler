from space import Checker
from lexer import Lexer
from parser_1 import Parser
from generator import Generator
# import nltk
# nltk.download()

def main(value):
    # with open(value, "r") as file:
    #     lines = file.readlines()

    code = Checker(value).returns()
    tokenized = Lexer(code).lexe(code)
    print(tokenized)
    parsed = Parser(tokenized).line(tokenized)
    print(parsed)

    generated = Generator(parsed).evaluate(parsed)
    return generated



