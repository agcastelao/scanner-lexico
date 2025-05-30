import sys
import re

RESERVED = {"main", "int", "float", "char", "if", "else", "while", "do", "for"}
OPERATORS = {'+', '-', '*', '/', '<', '<=', '>', '>=', '==', '!=', '='}
DELIMITERS = {'(', ')', '{', '}', ',', ';'}

def is_identifier(token):
    return re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token)

def is_integer(token):
    return re.fullmatch(r'\d+', token)

def is_float(token):
    return re.fullmatch(r'\d+\.\d+', token) and token.count('.') == 1

def is_char_const(token):
    return re.fullmatch(r"'(.)'", token)

def tokenize_line(line, line_num):
    tokens = []
    words = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[0-9.]+|'[^']*'|==|!=|<=|>=|[{}(),;+\-*/<>=!]", line)
    col = 0
    for word in words:
        col = line.find(word, col) + 1

        if word.count('.') > 1:
            tokens.append((word, "LEXICAL ERROR", line_num, col))
        elif word == '!':
            tokens.append((word, "LEXICAL ERROR", line_num, col))
        elif word in RESERVED:
            tokens.append((word, "KEYWORD", line_num, col))
        elif is_identifier(word):
            tokens.append((word, "IDENTIFIER", line_num, col))
        elif is_integer(word):
            tokens.append((word, "INTEGER", line_num, col))
        elif is_float(word):
            tokens.append((word, "FLOAT", line_num, col))
        elif is_char_const(word):
            tokens.append((word, "CHAR", line_num, col))
        elif word in OPERATORS:
            tokens.append((word, "OPERATOR", line_num, col))
        elif word in DELIMITERS:
            tokens.append((word, "DELIMITER", line_num, col))
        else:
            tokens.append((word, "LEXICAL ERROR", line_num, col))
    return tokens

def main():
    if len(sys.argv) < 2:
        print("Uso: python scanner.py <arquivo>")
        return
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f, 1):
                tokens = tokenize_line(line, i)
                for t in tokens:
                    print(t)
    except FileNotFoundError:
        print("Arquivo não encontrado.")

if __name__ == "__main__":
    main()
