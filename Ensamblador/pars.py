import copy
from tokenizer import Tokenizer, Token

class RecursiveDescentParser(object):
    current_line = -4
    etiquetas={}
    def Inicio(self):
      InstR = ['ADD','SUB','XOR','OR','AND','SLL','SRL','SRA','SLT','SLTU']
      InstI = ['ADD_I','XOR_I','OR_I','AND_I','SLL_I','SRL_I','SRA_I','SLT_I','SLTIU','LB','LH','LW','LBU','LHU','JALR','ECALL','EBREAK']
      InstS = ['SB','SH','SW']
      InstB = ['BEQ','BNE','BLT','BGE','BLTU','BGEU']
      InstJ = ['JAL']
      InstU = ['LUI','AUIPC']
      tok_inicio = copy.copy(self.tok)
      nexttok_inicio= copy.copy(self.nexttok)
      tokens_inicio = copy.copy(self.tokens)

      while self.nexttok != None:
        if self._accept('LABEL'):
          if ":" in self.tok.value:
            self.current_line += 4
            self.etiquetas[self.tok.value.replace(":", "")] = self.current_line
            self.current_line -= 4
        else:
          if self.nexttok.type in InstR or self.nexttok.type in InstI or  self.nexttok.type in InstS or  self.nexttok.type in InstB or self.nexttok.type in InstJ or self.nexttok.type in InstU:
            self.current_line += 4
          self._advance()

      self.tok=tok_inicio
      self.nexttok=nexttok_inicio
      self.tokens=tokens_inicio
      return self.Inst()

    def Inst(self):
      '''
          Inst ::= InstR | InstI | InstS | InstB | InstJ | InstU
        '''
      InstR = ['ADD','SUB','XOR','OR','AND','SLL','SRL','SRA','SLT','SLTU']
      InstI = ['ADD_I','XOR_I','OR_I','AND_I','SLL_I','SRL_I','SRA_I','SLT_I','SLTIU','LB','LH','LW','LBU','LHU','JALR','ECALL','EBREAK']
      InstS = ['SB','SH','SW']
      InstB = ['BEQ','BNE','BLT','BGE','BLTU','BGEU']
      InstJ = ['JAL']
      InstU = ['LUI','AUIPC']
      Instrucicones=""
      self.current_line = -4
      while self.nexttok != None:
          self.current_line += 4
          if self.nexttok.type in InstR:
              Instrucicones=Instrucicones+self.InstR()+"\n"
          elif self.nexttok.type in InstI:
              Instrucicones=Instrucicones+self.InstI()+"\n"
          elif self.nexttok.type in InstS:
              Instrucicones=Instrucicones+self.InstS()+"\n"
          elif self.nexttok.type in InstB:
              Instrucicones=Instrucicones+self.InstB()+"\n"
          elif self.nexttok.type in InstJ:
              Instrucicones=Instrucicones+self.InstJ()+"\n"
          elif self.nexttok.type in InstU:
              Instrucicones=Instrucicones+self.InstU()+"\n"
          elif self.nexttok.type == 'LABEL':
            self._accept('LABEL')
            self.current_line+=-4
          else:
            raise SyntaxError('Caracter ilegal')
      return Instrucicones

    def InstR(self):
      '''
      InstR :: add rd, rs1, rs2
                  |sub rd, rs1, rs2
          |xor rd, rs1, rs2
          |or rd, rs1, rs2
          |and rd, rs1, rs2
          |sll rd, rs1, rs2
          |srl rd, rs1, rs2
          |sra rd, rs1, rs2
          |slt rd, rs1, rs2
          |sltu rd, rs1, rs2
      '''
      opcode="0110011"
      funct7="0000000"
      if self._accept('ADD'):
        funct3="000"
      elif self._accept('SUB'):
        funct7="0100000"
        funct3="000"
      elif self._accept('XOR'):
        funct3="100"
      elif self._accept('OR'):
        funct3="110"
      elif self._accept('AND'):
        funct3="111"
      elif self._accept('SLL'):
        funct3="001"
      elif self._accept('SRL'):
        funct3="101"
      elif self._accept('SRA'):
        funct7="0100000"
        funct3="101"
      elif self._accept('SLT'):
        funct3="010"
      elif self._accept('SLTU'):
        funct3="011"
      else:
        raise SyntaxError('Esperando un Inst tipo R')

      rd=self.Register()
      self._expect(',')
      rs1=self.Register()
      self._expect(',')
      rs2=self.Register()
      inst=funct7+rs2+rs1+funct3+rd+opcode
      return inst

    def InstI(self):
      '''
      InstI :: addi rd, rs1, imm
          |xori rd, rs1, imm
          |ori rd, rs1, imm
          |andi rd, rs1, imm
          |slli rd, rs1, imm[0:4]
          |srli rd, rs1, imm[0:4]
          |srai rd, rs1, imm[0:4]
          |slti rd, rs1, imm
          |sltiu rd, rs1, imm
          |jalr rd, rs1, imm
          |ecall
          |ebreak
      '''
      opcode="0010011"
      if self._accept('ADD_I'):
        funct3="000"
      elif self._accept('XOR_I'):
        funct3="100"
      elif self._accept('OR_I'):
        funct3="110"
      elif self._accept('AND_I'):
        funct3="111"
      elif self._accept('SLL_I'):
        funct3="001"
        funct7="0000000"
      elif self._accept('SRL_I'):
        funct3="101"
        funct7="0000000"
      elif self._accept('SRA_I'):
        funct3="101"
        funct7="0100000"
      elif self._accept('SLT_I'):
        funct3="010"
      elif self._accept('SLTIU'):
        funct3="011"
      elif self._accept('JALR'):
        opcode="1100111"
        funct3="000"
      else:
        opcode = "0000011"
        if self._accept('LB'):
            funct3 = "000"
        elif self._accept('LH'):
            funct3 = "001"
        elif self._accept('LW'):
            funct3 = "010"
        elif self._accept('LBU'):
            funct3 = "100"
        elif self._accept('LHU'):
            funct3 = "101"
        else:
            opcode = "1110011"
            if self._accept('ECALL'):
                funct3 = "000"
                funct7 = "0000000"
            elif self._accept('EBREAK'):
                funct3 = "000"
                funct7 = "0000001"
            else:
                raise SyntaxError('Esperando un Inst tipo I')

      if(self.tok.type in ['LB','LH','LW','LBU','LHU']):
          rd=self.Register()
          self._expect(',')
          self._accept('IMM')

          valor_imm=int(self.tok.value)

          if valor_imm > 2047 or valor_imm < -2048:
            raise SystemError('El inmediato ingresado no puede ser mayor a 11 bits (2047 0 -2048) ')
          bits=12
          if valor_imm >= 0:
            imm=bin(valor_imm)[2:].zfill(bits)
          else:
            numero_positivo = -valor_imm
            bin_positivo = bin(numero_positivo)[2:].zfill(bits)
            bin_complemento_1 = ''.join('1' if bit == '0' else '0' for bit in bin_positivo)
            bin_complemento_1 = bin_complemento_1[-bits:]
            bin_complemento_2 = bin(int(bin_complemento_1, 2) + 1)[2:].zfill(bits)
            imm=bin_complemento_2

          self._expect(',')
          rs1=self.Register()
          inst=imm+rs1+funct3+rd+opcode
          return inst

      else:
          if(self.tok.type in ['ECALL','EBREAK']):
              bits = 12
              imm = funct7+"00000"
              rs1 = "00000"
              rd = "00000"
              inst=imm+rs1+funct3+rd+opcode
              return inst
          else:
              rd=self.Register()
              self._expect(',')
              rs1=self.Register()
              self._expect(',')
              if self._accept('IMM'):
                valor_imm=int(self.tok.value)
              elif self._accept('LABEL'):
                if self.tok.value not in self.etiquetas:
                  raise SystemError('Ingreso un label que no está')
                valor_imm=self.etiquetas[self.tok.value]
              else:
                raise SystemError('Se esperaba un inmediato o un label')

              if (self.tok.type not in ['SLL_I','SRL_I','SRA_I'] ):
                if valor_imm > 2047 or valor_imm < -2048:
                  raise SystemError('El inmediato ingresado no puede ser mayor a 11 bits (2047 0 -2048) ')
                bits=12
                if valor_imm >= 0:
                  imm=bin(valor_imm)[2:].zfill(bits)
                else:
                  numero_positivo = -valor_imm
                  bin_positivo = bin(numero_positivo)[2:].zfill(bits)
                  bin_complemento_1 = ''.join('1' if bit == '0' else '0' for bit in bin_positivo)
                  bin_complemento_1 = bin_complemento_1[-bits:]
                  bin_complemento_2 = bin(int(bin_complemento_1, 2) + 1)[2:].zfill(bits)
                  imm=bin_complemento_2
              else:
                if valor_imm > 31 or valor_imm<0:
                  imm=funct7+bin(valor_imm)[2:]
                else:
                  raise SystemError('El inmediato ingresado no puede ser mayor a 5 bits (31)')

          inst=imm+rs1+funct3+rd+opcode
          return inst

    def InstS(self):
      '''
      InstS :: sb rs2, imm, rs1
          |sh rs2, imm, rs1
          |sw rs2, imm, rs1
      '''

      opcode = "0100011"
      if self._accept('SB'):
        funct3="000"
      elif self._accept('SH'):
        funct3="001"
      elif self._accept('SW'):
        funct3="010"
      else:
        raise SyntaxError('Esperando un Inst tipo S')

      rs2=self.Register()
      self._expect(',')
      self._accept('IMM')

      valor_imm=int(self.tok.value)

      if valor_imm > 2047 or valor_imm < -2048:
        raise SystemError('El inmediato ingresado no puede ser mayor a 11 bits (2047 0 -2048) ')
      bits=12
      if valor_imm >= 0:
        imm=bin(valor_imm)[2:].zfill(bits)
      else:
        numero_positivo = -valor_imm
        bin_positivo = bin(numero_positivo)[2:].zfill(bits)
        bin_complemento_1 = ''.join('1' if bit == '0' else '0' for bit in bin_positivo)
        bin_complemento_1 = bin_complemento_1[-bits:]
        bin_complemento_2 = bin(int(bin_complemento_1, 2) + 1)[2:].zfill(bits)
        imm=bin_complemento_2

      self._expect(',')
      rs1=self.Register()

      inst=imm[0:7]+rs2+rs1+funct3+imm[7:12]+opcode
      return inst

    def InstB(self):
      '''
      InstB :: beq rs1, rs2, imm
          |bne rs1, rs2, imm
          |blt rs1, rs2, imm
          |bge rs1, rs2, imm
          |bltu rs1, rs2, imm
          |bgeu rs1, rs2, imm
      '''

      opcode = "1100011"
      if self._accept('BEQ'):
        funct3="000"
      elif self._accept('BNE'):
        funct3="001"
      elif self._accept('BLT'):
        funct3="100"
      elif self._accept('BGE'):
        funct3="101"
      elif self._accept('BLTU'):
        funct3="110"
      elif self._accept('BGEU'):
        funct3="111"
      else:
        raise SyntaxError('Esperando un Inst tipo B')

      rs1=self.Register()
      self._expect(',')
      rs2=self.Register()
      self._expect(',')
      if self._accept('IMM'):
        valor_imm=int(self.tok.value)
      elif self._accept('LABEL'):
        if self.tok.value not in self.etiquetas:
          raise SystemError('Ingreso un label que no está')
        label_linea=self.etiquetas[self.tok.value]
        valor_imm=label_linea-self.current_line
        print(valor_imm)
      else:
        raise SystemError('Se esperaba un inmediato o un label')

      if valor_imm > 4095 or valor_imm < -4096:
        raise SystemError('El inmediato ingresado no puede ser mayor a 13 bits (4095 0 -4096) ')
      bits=13
      if valor_imm >= 0:
        imm=bin(valor_imm)[2:].zfill(bits)
        print(imm)
      else:
        numero_positivo = -valor_imm
        bin_positivo = bin(numero_positivo)[2:].zfill(bits)
        bin_complemento_1 = ''.join('1' if bit == '0' else '0' for bit in bin_positivo)
        bin_complemento_1 = bin_complemento_1[-bits:]
        bin_complemento_2 = bin(int(bin_complemento_1, 2) + 1)[2:].zfill(bits)
        imm=bin_complemento_2
      inst=imm[0]+imm[2:8]+rs2+rs1+funct3+imm[8:12]+imm[1]+opcode
      return inst

    def InstJ(self):
      '''
      InstJ :: jal (rd,)? (imm|label)
      '''
      opcode = "1101111"
      if self._accept('JAL'):
          pass #No tiene functs
      else:
          raise SyntaxError('Esperando un Inst tipo J')

      if self.nexttok.type == 'REG':
        rd=self.Register()
        self._expect(',')
      else:
        rd="00001" #ra

      if self._accept('IMM'):
        valor_imm=int(self.tok.value)
      elif self._accept('LABEL'):
        if self.tok.value not in self.etiquetas:
          raise SystemError('Ingreso un label que no está')
        label_linea=self.etiquetas[self.tok.value]
        valor_imm=label_linea-self.current_line
      else:
        raise SystemError('Se esperaba un inmediato o un label')

      if valor_imm > 1048575 or valor_imm < -1048576:
          raise SystemError('El inmediato ingresado no puede ser mayor a 21 bits (1048575 0 -1048576) ')
      bits=21
      if valor_imm >= 0:
        imm=bin(valor_imm)[2:].zfill(bits)
      else:
        numero_positivo = -valor_imm
        bin_positivo = bin(numero_positivo)[2:].zfill(bits)
        bin_complemento_1 = ''.join('1' if bit == '0' else '0' for bit in bin_positivo)
        bin_complemento_1 = bin_complemento_1[-bits:]
        bin_complemento_2 = bin(int(bin_complemento_1, 2) + 1)[2:].zfill(bits)
        imm=bin_complemento_2

      inst=imm[1]+imm[11:21]+imm[10]+imm[2:10]+rd+opcode
      return inst

    def InstU(self):
      '''
      InstU :: lui rd imm | auipc rd imm
      '''

      opcode = "0110111"
      if self._accept('LUI'):
        pass #No tiene functs
      elif self._accept('AUIPC'):
        opcode = "0010111"
      else:
        raise SystemError('Esperando Inst tipo U')

      rd=self.Register()
      self._expect(',')
      self._accept('IMM')

      valor_imm=int(self.tok.value)
      if valor_imm > 9979356512255 or valor_imm < -8899172237312:
          raise SystemError('El inmediato ingresado no puede ser mayor a 20 bits (9979356512255) o negativo')
      bits=20
      imm=bin(valor_imm)[2:].zfill(bits)

      inst=imm[0:20]+rd+opcode
      return inst

    def Register(self):
      if self._accept('REG'):
        reg=self.tok.value
        registros = {
                  "zero": "00000",
                  "ra": "00001",
                  "sp": "00010",
                  "gp": "00011",
                  "tp": "00100",
                  "t0": "00101",
                  "t1": "00110",
                  "t2": "00111",
                  "s0": "01000",
                  "s1": "01001",
                  "a0": "01010",
                  "a1": "01011",
                  "a2": "01100",
                  "a3": "01101",
                  "a4": "01110",
                  "a5": "01111",
                  "a6": "10000",
                  "a7": "10001",
                  "s2": "10010",
                  "s3": "10011",
                  "s4": "10100",
                  "s5": "10101",
                  "s6": "10110",
                  "s7": "10111",
                  "s8": "11000",
                  "s9": "11001",
                  "s10": "11010",
                  "s11": "11011",
                  "t3": "11100",
                  "t4": "11101",
                  "t5": "11110",
                  "t6": "11111",
              }
        #Se agrega la equivalencia de x0 hasta x31
        for i in range(32):
          registros[f'x{i}'] = format(i, '05b')
        if reg in registros:
          return registros[reg]


    def _advance(self):
      'Advanced the tokenizer by one symbol'
      self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self,toktype):
      'Consume the next token if it matches an expected type'
      if self.nexttok and self.nexttok.type == toktype:
        self._advance()
        return True
      else:
        return False

    def _expect(self,toktype):
      'Consume and discard the next token or raise SyntaxError'
      if not self._accept(toktype):
        raise SyntaxError("Expected %s" % toktype)

    def start(self):
      'Entry point to parsing'
      self._advance()              # Load first lookahead token
      return self.Inicio()

    def parse(self,tokens):
      'Entry point to parsing'
      self.tok = None         
      self.nexttok = None     
      self.tokens = tokens
      return self.start()
