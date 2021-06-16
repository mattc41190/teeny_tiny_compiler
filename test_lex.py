from lex import Lexer, EOF

SIMPLE_PROGRAM = "LET foo = 123"

def test_nextChar_gets_next_available_char_until_it_hits_eof():
    lexer = Lexer(SIMPLE_PROGRAM)

    while lexer.curChar != EOF:
        print(lexer.curChar)
        lexer.nextChar()


test_nextChar_gets_next_available_char_until_it_hits_eof()