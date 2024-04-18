from tokenizer import Tokenizer
from pars import RecursiveDescentParser

def main():
    NameFile = "Instrucciones.s"
    with open(NameFile, "r") as archivo:
        text = archivo.read()
    lexer = Tokenizer()

    '''
    for tok in lexer.tokenizer(text):
        print(tok)
    '''
    parser = RecursiveDescentParser()
    ast = parser.parse(lexer.tokenizer(text))
    ast = ast + "00000000000000000000000000000000"
    with open("Binario_Inst.txt", "w") as archivo:
        archivo.write(ast)

if __name__ == '__main__':
    main()
