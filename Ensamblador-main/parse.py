from instr_arr import *  # Importa clases y constantes de instrucciones.
from types import FunctionType as function  # Importa FunctionType con un alias 'function' para mayor claridad.
from os.path import exists  # Se utiliza para verificar si un archivo de entrada existe.
__all__ = ['Parser']  # Define lo que se importará al usar 'from module import *'.

class _Parser:
    # Esta función especial permite a una instancia del _Parser ser llamada como una función.
	def __call__(self, *args) -> list:
        # Si el argumento es una lista, procesa la lista de líneas de ensamblador.
		if type(args[0]) == list:
			return _Parser.interpret_arr(*args)
        # Si el argumento es un archivo existente, procesa ese archivo.
		elif exists(*args):
			return _Parser.interpret_arr(_Parser.read_file(*args))
        # Si el argumento es una cadena, se asume que es una línea de código de ensamblador.
		elif type(args[0]) == str:
			return _Parser.interpret_arr(args[0].split('\n'))
		raise Exception()  # Si ninguna condición coincide, lanza una excepción.

    # Determina si una línea del código de ensamblador es válida para su procesamiento.
	@staticmethod
	def valid_line(x : str, allow_colon : bool = False) -> bool:
        # Líneas vacías, comentarios, y directivas se consideran no válidas.
		if x[0][0] == "#" or x[0][0] == "\n" or x[0][0] == "" or x[0][0] == ".":
			return False
        # Si no se permiten etiquetas y la línea termina con ':', también es inválida.
		if not allow_colon and x[-1] == ":":
			return False
		return True

    # Elimina los comentarios en línea de la cadena de código de ensamblador.
	@staticmethod
	def handle_inline_comments(x : str) -> str:
		if "#" in x:
			pos = x.index("#")
			return x[0:pos].replace(',', ' ')  # Quita el comentario y las comas.
		return x.replace(',', ' ')  # Si no hay comentarios, solo quita las comas.

    # Maneja instrucciones específicas que requieren un tratamiento especial en la tokenización.
	@staticmethod
	def handle_specific_instr(x : list) -> list:
        # Maneja casos como 'sw' y 'lw', que tienen un formato especial para los operandos.
		if len(x[0]) == 2 and (x[0] in S_instr or x[0] in I_instr):
			y = x[-1].split('('); y[1] = y[1].replace(')','')
			return x[0:-1] + y
		elif 'requires jump' == 5:
			...
		return x

    # Lee un archivo y devuelve una lista de líneas no vacías.
	@staticmethod
	def read_file(file : str) -> list:
		with open(file) as f:
			return [x.strip() for x in f.readlines() if x != '\n']

    # Convierte un arreglo de código de ensamblador en una lista de instrucciones interpretadas.
	@staticmethod
	def interpret_arr(code : list) -> list:
		int_code = []
		for line_num, line in enumerate(code):
			tokens = _Parser.tokenize(line, line_num, code)  # Tokeniza la línea.
			int_code += [_Parser.interpret(tokens) for _ in range(1) if len(tokens) != 0]  # Interpreta los tokens.
		return int_code

    # Divide una línea de ensamblador en tokens, incluyendo el número de línea y el código completo si se proporcionan.
	@staticmethod
	def tokenize(line : str, line_num: int = None, code : list = None) -> list:
		line = line.strip()
		if len(line) > 0 and _Parser.valid_line(line):
			tokens = _Parser.handle_inline_comments(line).split()
			tokens = _Parser.handle_specific_instr(tokens)
			return tokens + [line_num, code] if line_num != None and code != None else tokens
		return []

    # Determina el tipo de instrucción de los tokens y devuelve la función de análisis correspondiente.
	@staticmethod
	def interpret(tokens : list) -> str:
		f = _Parser.determine_type(tokens[0])
		return f(tokens)

	@staticmethod
	def determine_type(tk : str) -> function:
		instr_sets = [R_instr, I_instr, S_instr, SB_instr, U_instr, UJ_instr, pseudo_instr]
		parsers = [Rp, Ip, Sp, SBp, Up ,UJp, Psp]
		for i in range(len(instr_sets)):
			if tk in instr_sets[i]:
				return parsers[i]
		raise Exception("Instrucción errónea: " + tk + "!")

Parser = _Parser()