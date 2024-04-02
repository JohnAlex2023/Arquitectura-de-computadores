from instr_arr import *
from parse import *
from os.path import exists

__all__ = ['ConversorEnsamblador']

class ConversorEnsamblador:
    # Constructor: Inicializa los modos de salida, nibble y hexadecimal.
    def __init__(self, modo_salida: str = 'a', modo_nibble: bool = False, modo_hex: bool = False) -> None:
        self.__modo_salida = self.__verificar_modo_salida(modo_salida)
        self.__modo_nibble = self.__verificar_modo_nibble(modo_nibble)
        self.__modo_hex = self.__verificar_modo_hex(modo_hex)

    # Representación en cadena de la configuración actual del conversor.
    def __str__(self):
        return "Salida: {modo_salida}, Nibble: {modo_nibble}, Hex: {modo_hex}".format(
            modo_salida=self.__modo_salida,
            modo_nibble=self.__modo_nibble,
            modo_hex=self.__modo_hex
        )

    # Representación formal de la configuración actual del conversor.
    def __repr__(self):
        return "Salida: {modo_salida}, Nibble: {modo_nibble}, Hex: {modo_hex}".format(
            modo_salida=self.__modo_salida,
            modo_nibble=self.__modo_nibble,
            modo_hex=self.__modo_hex
        )

    # Crea un clon de esta instancia de ConversorEnsamblador.
    def clone(self):
        return ConversorEnsamblador(
            modo_salida=self.__modo_salida,
            modo_nibble=self.__modo_nibble,
            modo_hex=self.__modo_hex
        )

    # Función llamable para convertir el código ensamblador usando la configuración actual.
    def __call__(self, *args):
        return self.convertir(*args)

    # Verifica que el modo de salida sea válido.
    def __verificar_modo_salida(self, x) -> str:
        mod = ''.join(sorted(x.split()))
        assert mod in ['a', 'f', 'p', None], "El modo de salida debe ser uno de a(rreglo), f(ichero), p(imprimir), o None."
        return x

    # Verifica que el modo nibble sea un booleano.
    def __verificar_modo_nibble(self, x) -> bool:
        assert type(x) == bool, "El modo nibble debe ser un booleano."
        return x

    # Verifica que el modo hexadecimal sea un booleano.
    def __verificar_modo_hex(self, x) -> bool:
        assert type(x) == bool, "El modo hexadecimal debe ser un booleano."
        return x

    # Propiedad: manera de outputear el código de máquina.
    @property
    def modo_salida(self) -> str:
        return self.__modo_salida

    @modo_salida.setter
    def modo_salida(self, x: str) -> None:
        self.__modo_salida = x

    # Propiedad: si se imprime en nibbles o no (solo aplica para texto o imprimir).
    @property
    def modo_nibble(self) -> bool:
        return self.__modo_nibble

    @modo_nibble.setter
    def modo_nibble(self, x: bool) -> None:
        self.__modo_nibble = x

    # Propiedad: si se retorna en hexadecimal o no.
    @property
    def modo_hex(self) -> bool:
        return self.__modo_hex

    @modo_hex.setter
    def modo_hex(self, x: bool) -> None:
        self.__modo_hex = x

    # Convierte el código ensamblador al formato deseado según la configuración actual.
    def convertir(self, entrada: str, fichero: str = None):
        salida = Parser(entrada)
        assert len(salida) > 0, "La entrada proporcionada no produjo ningún resultado del analizador. Verifique la entrada."
        salida = self.mod(salida)  # aplicar modo nibble, modo hex

        if self.__modo_salida == 'a':
            return salida
        elif self.__modo_salida == 'f':
            directorio_prov = '/'.join(fichero.split('/')[:-1])
            assert fichero is not None, "Para el modo de salida a fichero, se necesita proporcionar un nombre de fichero."
            assert exists(directorio_prov if directorio_prov != '' else '.'), "El directorio del nombre de fichero proporcionado no existe."

            if self.__modo_hex and fichero[-4:] == '.bin':
                # cambiar a binario
                print('Advertencia: modo hexadecimal anulado para poder outputear a fichero binario.')
                salida = [format(int(elem, 16), '032b') for elem in salida]
            ConversorEnsamblador.escribir_a_fichero(salida, fichero)
            return
        elif self.__modo_salida == 'p':
            print('\n'.join(salida))
            return

        raise NotImplementedError()

    # Escribe la salida a un fichero, eligiendo el formato adecuado basado en la extensión del fichero.
    @staticmethod
    def escribir_a_fichero(salida: list, fichero: str) -> None:
        extension = fichero[-4:]

        if extension == '.bin':
            with open(fichero, 'wb') as f:
                for instr in salida:
                    arreglo_bytes = [instr[i:i+8] for i in range(0, len(instr), 8)]
                    lista_bytes = [int(b, 2) for b in arreglo_bytes]
                    f.write(bytearray(lista_bytes))
            return

        elif extension == '.txt':
            with open(fichero, 'w') as f:
                for instr in salida:
                    f.write(instr + "\n")

            return

        elif extension == '.csv':
            raise NotImplementedError()

        elif extension == '.dat':
            raise NotImplementedError()

        raise NotImplementedError()

    # Modifica la salida aplicando el modo nibble o hexadecimal si está activado.
    def mod(self, salida: list) -> list:
        if self.__modo_nibble:
            salida = ConversorEnsamblador.aplicar_nibble(salida)
        elif self.__modo_hex:
            salida = ConversorEnsamblador.aplicar_hex(salida)
        return salida

    # Aplica el modo nibble a la salida.
    @staticmethod
    def aplicar_nibble(salida: list) -> list:
        return ['\t'.join([elem[i:i+4] for i in range(0, len(elem), 4)]) for elem in salida]

    # Aplica el modo hexadecimal a la salida.
    @staticmethod
    def aplicar_hex(salida: list) -> list:
        return ['0x' + '{:08X}'.format(int(elem, 2)).lower() for elem in salida]
