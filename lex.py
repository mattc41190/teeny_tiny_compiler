import enum
import sys

MAX_STRING_LEN = 10000

EOF = "\0"
SPACE = " "
TAB = "\t"
RETURN = "\r"
NEWLINE = "\n"
HASH = "#"
QUOTE = "\""
PERIOD = "."
DOUBLE_SLASH = "//"
PERCENT = "%"

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords.
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211


class Token(object):
    def __init__(self, tokenText, tokenKind) -> None:
        # print(f"The provided input to tokenize was: {tokenText} it will be tokenized as a: {tokenKind}")
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def isKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value <= 200:
                return kind
        return None


class Lexer(object):
    def __init__(self, input) -> None:
        print(f"The provided input was: {input}")
        self.source = input + "\n"  # Source code to lex as string with new line added for ease of use
        self.curChar = ''  # Current character in the string
        self.curPos = -1  # Current position in the string 
        self.nextChar()


    # Process the next character.
    # Move the file scanner string reader one position or put the EOF character 
    # indicating we are done
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return EOF
        return self.source[self.curPos+1] 

    # Invalid token found, print error and exit.
    def abort(self, message):
        sys.exit(f"Lexing error: {message}")

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar in {SPACE, TAB, RETURN}:
            self.nextChar()

    # Skip comments in the code.
    def skipComments(self):
        if self.curChar == HASH:
            while self.curChar != NEWLINE:
                print(f"Skipping comment fragment: {self.curChar}")
                self.nextChar()

    def handleString(self):
        self.nextChar()  # Move cursor one spot forward (to not cap)
        string_len = 0
        startPos = self.curPos  # Get starting index of stringified material
        endPos = self.curPos  # Get starting index of stringified material

        while self.curChar != QUOTE:  # Until we find the closing quotation mark
            string_len += 1
            if string_len > MAX_STRING_LEN:
                self.abort(f"String starting at: {startPos} exceeds max length of {MAX_STRING_LEN}")
            if self.curChar in {TAB, RETURN, NEWLINE, PERCENT}:
                self.abort(f"Illegal character found in string: {self.curChar}")
            self.nextChar()
        
        endPos = self.curPos
        return (startPos, endPos)

    def handleIdentifier(self):
        startPos = self.curPos 

        while self.peek().isalnum():
            self.nextChar()

        tokenText = self.source[startPos : self.curPos + 1]
        knownKeyword = Token.isKeyword(tokenText)
        if not knownKeyword:
            return Token(tokenText, TokenType.IDENT)
        return Token(tokenText, knownKeyword)


    def handleNumber(self):
        startPos = self.curPos 
        endPos = self.curPos  

        while self.peek().isdigit():  
            self.nextChar()
        
        if self.peek() == PERIOD:
            self.nextChar()

            if not self.peek().isdigit():
                self.abort(f"Character immediately following decimal is not valid: {self.peek()}")
            
            while self.peek().isdigit():  
                self.nextChar()
    
        endPos = self.curPos
        return (startPos, endPos)

    # Get the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComments()

        token =  None

        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == NEWLINE:
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == EOF:
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == "=":
            # Check whether this token is = or ==
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            # Check whether this token is = or >=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            # Check whether this token is = or <=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == "!":
            # Check whether this token is = or <=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort(f"Expected != Got: {self.curChar}{self.peek()}")  
        elif self.curChar.isdigit():
            startPos, endPos = self.handleNumber()
            number = self.source[startPos : endPos]
            token = Token(number, TokenType.NUMBER)
        elif self.curChar.isalpha():
            token = self.handleIdentifier()
        elif self.curChar == QUOTE:
            startPos, endPos = self.handleString()
            text = self.source[startPos : endPos]
            token = Token(text, TokenType.STRING)
        else:
            self.abort(f"Unknown Token: {self.curChar}")

        self.nextChar()
        return token


