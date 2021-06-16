from lex import Lexer, TokenType, EOF

input = "+- */ >>= \n # Hello \n = != \"This is a string...\" +-123 9.8654*/ IF+-123 foo*THEN/"

def main():
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()