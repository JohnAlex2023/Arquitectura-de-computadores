# main.py
import re


def ensamblar_programa(archivo_asm, archivo_salida, reg_map, instr_map):
    direccion_memoria = 0
    etiquetas = {}
    instrucciones_con_etiquetas = []
    
    with open(archivo_asm, 'r') as f_asm:
        for line in f_asm:
            line = line.split('#')[0].strip()
            if not line:
                continue
            if ':' in line:
                # Esta es una etiqueta
                etiqueta, instruccion = line.split(':')
                etiquetas[etiqueta.strip()] = direccion_memoria
                line = instruccion.strip()
                if not line:  # Si no hay instrucción después de la etiqueta, continuamos
                    continue
            tokens = re.split(r'[\s,]+', line)
            instrucciones_con_etiquetas.append((tokens, direccion_memoria))
            direccion_memoria += 4  # Incrementamos la dirección de memoria

    # Segunda pasada para resolver las etiquetas y convertir a código máquina
    with open(archivo_salida, 'w') as f_out:
        for tokens, addr in instrucciones_con_etiquetas:
            instruccion = tokens[0]
            if instruccion in etiquetas:  # Si la instrucción es realmente una etiqueta
                addr_etiqueta = etiquetas[instruccion]
                offset = (addr_etiqueta - addr) // 4
                tokens[-1] = str(offset)  # Reemplazamos la etiqueta por el offset calculado
            codigo_maquina = convertir_instruccion(tokens, reg_map, instr_map)
            if codigo_maquina:
                hex_instruccion = format(int(codigo_maquina, 2), '08x')
                f_out.write(f"{addr:04x}: {hex_instruccion}\n")


# Cargar el mapeo de registros desde un archivo
def cargar_registro_mapa(archivo):
    reg_map = {}
    with open(archivo, "r") as f:
        for line in f:
            (key, val) = line.split()
            reg_map[key] = format(int(val[1:]), '05b') if val[1:].isdigit() else None
    return reg_map

# Cargar el mapeo de instrucciones desde un archivo
def cargar_instruccion_mapa(archivo):
    instr_map = {}
    with open(archivo, "r") as f:
        for line in f:
            parts = line.split()
            instr_map[parts[0]] = parts[1:]
    return instr_map

# Convertir la instrucción dada a código máquina
def convertir_instruccion(tokens, reg_map, instr_map):
    instr = tokens[0]
    if instr not in instr_map:
        print(f"Instrucción no reconocida: {instr}")
        return None

    # Información de la instrucción
    instr_info = instr_map[instr]
    instr_type = instr_info[0]

    if instr_type == "R":
        rd, rs1, rs2 = reg_map[tokens[1]], reg_map[tokens[2]], reg_map[tokens[3]]
        opcode, funct3, funct7 = instr_info[1], instr_info[2], instr_info[3]
        return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"

    elif instr_type == "I":
        rd, rs1 = reg_map[tokens[1]], reg_map[tokens[2]]
        imm = format(int(tokens[3]) & ((1 << 12) - 1), '012b')
        opcode, funct3 = instr_info[1], instr_info[2]
        return f"{imm}{rs1}{funct3}{rd}{opcode}"

    elif instr_type == "S":
        rs1, rs2 = reg_map[tokens[2]], reg_map[tokens[1]]
        imm = format(int(tokens[3]) & ((1 << 12) - 1), '012b')
        opcode, funct3 = instr_info[1], instr_info[2]
        return f"{imm[0:7]}{rs2}{rs1}{funct3}{imm[7:12]}{opcode}"

    elif instr_type == "B":
        rs1, rs2 = reg_map[tokens[1]], reg_map[tokens[2]]
        imm = format(int(tokens[3]) & ((1 << 13) - 1), '013b')
        opcode, funct3 = instr_info[1], instr_info[2]
        # El inmediato para instrucciones B está disperso
        imm = f"{imm[12]}{imm[10:5]}{imm[4:1]}{imm[11]}"
        return f"{imm}{rs2}{rs1}{funct3}{opcode}"

    elif instr_type == "U":
        rd = reg_map[tokens[1]]
        imm = format(int(tokens[2]) >> 12 & ((1 << 20) - 1), '020b')
        opcode = instr_info[1]
        return f"{imm}{rd}{opcode}"

    elif instr_type == "J":
        rd = reg_map[tokens[1]]
        imm = format(int(tokens[2]) & ((1 << 21) - 1), '021b')
        opcode = instr_info[1]
        # El inmediato para instrucciones J está disperso
        imm = f"{imm[20]}{imm[10:1]}{imm[11]}{imm[19:12]}"
        return f"{imm}{rd}{opcode}"

    # Agregar casos para otros tipos de instrucciones si es necesario

    return None


# Leer el programa ensamblador y convertirlo a código máquina
def ensamblar_programa(archivo_asm, archivo_salida, reg_map, instr_map):
    with open(archivo_asm, 'r') as f_asm, open(archivo_salida, 'w') as f_out:
        for line in f_asm:
            # Eliminar comentarios y separar los tokens
            line = line.split('#')[0].strip()
            tokens = re.split(r'[\s,]+', line) if line else []
            if tokens:
                codigo_maquina = convertir_instruccion(tokens, reg_map, instr_map)
                if codigo_maquina:
                    # Escribir el código máquina al archivo de salida
                    f_out.write(codigo_maquina + '\n')

# Rutas de los archivos de datos
ruta_instr_data = 'instr_data.dat'
ruta_reg_map = 'reg_map.dat'

# Cargar los mapeos
reg_map = cargar_registro_mapa(ruta_reg_map)
instr_map = cargar_instruccion_mapa(ruta_instr_data)

# Ruta del programa de ensamblador y archivo de salida
ruta_programa_asm = 'C:/Users/jdavi/Desktop/Registros/mi_programa.asm'
ruta_archivo_salida = 'C:/Users/jdavi/Desktop/Registros/mi_programa_salida.bin'

# Ensamblar el programa
ensamblar_programa(ruta_programa_asm, ruta_archivo_salida, reg_map, instr_map)
