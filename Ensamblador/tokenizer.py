from dataclasses import dataclass
import copy
from rich import print


import re

# ANALISIS LEXICO
@dataclass
class Token:
	'''
	Representacion de un token
	'''
	type  : str
	value : float or str
	lineno: int = 1

class Tokenizer:

	tokens = [
		(r'\s+', None),
		(r'//.*\n', None),		#Comentarios Ignorados
		(r'addi',	 lambda s,tok:Token('ADD_I',tok)),
		(r'xori',	 lambda s,tok:Token('XOR_I',tok)),
		(r'ori',	 lambda s,tok:Token('OR_I',tok)),
		(r'andi',	 lambda s,tok:Token('AND_I',tok)),
		(r'slli',	 lambda s,tok:Token('SLL_I',tok)),
		(r'srli',	 lambda s,tok:Token('SRL_I',tok)),
		(r'srai',	 lambda s,tok:Token('SRA_I',tok)),
		(r'sltiu', lambda s,tok:Token('SLTIU',tok)),
		(r'slti',	 lambda s,tok:Token('SLT_I',tok)),
		(r'add',	 lambda s,tok:Token('ADD',tok)),
		(r'sub',	 lambda s,tok:Token('SUB',tok)),
		(r'xor',	 lambda s,tok:Token('XOR',tok)),
		(r'or',	   lambda s,tok:Token('OR',tok)),
		(r'and',	 lambda s,tok:Token('AND',tok)),
		(r'sll',	 lambda s,tok:Token('SLL',tok)),
		(r'srl',	 lambda s,tok:Token('SRL',tok)),
		(r'sra',	 lambda s,tok:Token('SRA',tok)),
		(r'sltu',	 lambda s,tok:Token('SLTU',tok)),
		(r'slt',	 lambda s,tok:Token('SLT',tok)),
		(r'lbu',	 lambda s,tok:Token('LBU',tok)),
		(r'lb',	   lambda s,tok:Token('LB',tok)),
		(r'lhu',	 lambda s,tok:Token('LHU',tok)),
		(r'lh',	   lambda s,tok:Token('LH',tok)),
		(r'lw',	   lambda s,tok:Token('LW',tok)),
		(r'sb',	   lambda s,tok:Token('SB',tok)),
		(r'sh',	   lambda s,tok:Token('SH',tok)),
		(r'sw',	   lambda s,tok:Token('SW',tok)),
		(r'beq',	 lambda s,tok:Token('BEQ',tok)),
		(r'bne',	 lambda s,tok:Token('BNE',tok)),
		(r'bltu',	 lambda s,tok:Token('BLTU',tok)),
		(r'blt',	 lambda s,tok:Token('BLT',tok)),
		(r'bgeu',	 lambda s,tok:Token('BGEU',tok)),
		(r'bge',	 lambda s,tok:Token('BGE',tok)),
		(r'jalr',	 lambda s,tok:Token('JALR',tok)),
		(r'jal',	 lambda s,tok:Token('JAL',tok)),
    (r'lui',     lambda s,tok:Token('LUI',tok)),
    (r'auipc',     lambda s,tok:Token('AUIPC',tok)),
    (r'ecall',     lambda s,tok:Token('ECALL',tok)),
    (r'ebreak',     lambda s,tok:Token('EBREAK',tok)),
		(r'-?[0-9]+',lambda s,tok:Token('IMM',tok)),
		(r'x(3[0-1]|0|[1-2]?[0-9])|zero|ra|sp|gp|tp|t0|t1|t2|s0|s1|a0|a1|a2|a3|a4|a5|a6|a7|s2|s3|s4|s5|s6|s7|s8|s9|s10|s11|t3|t4|t5|t6',	 lambda s,tok:Token('REG',tok)),
		(r'[a-zA-Z_][a-zA-Z0-9_]*:?', lambda s, tok: Token('LABEL', tok)),
		(r',',                       lambda s,tok:Token(',',tok)),
		(r'.',                       lambda s,tok:print("Error: caracter ilegal '%s'" % tok))]

	def tokenizer(self, text):
		scanner = re.Scanner(self.tokens)
		results, remainder = scanner.scan(text)
		return iter(results)