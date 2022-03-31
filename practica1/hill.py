import math
import numpy as np

class Hill():
    def __init__(self,abc):
        self.abc = abc

    def __mcd(self,a,b):
        a = abs(a)
        b = abs(b)
        while(a % b != 0):
            a,b = b,a % b
        return b


    def __verifica_clave(self,raiz,clave):
        if raiz - int(raiz) > 0:
            raise ValueError("La clave no tiene una longitud valida")
        
        raiz = int(raiz)

        k_arr = [[0] * raiz] * raiz

        k = 0
        for i in range(0,raiz):
            for j in range(0,raiz):
                k_arr[i][j] = self.abc.index(clave[k])
                k += 1

        det = round(np.linalg.det(k_arr))

        if self.__mcd(det,len(self.abc)) != 1:
            raise ValueError("No es posible invertir la matriz crack")

        return k_arr


    def __mult_matrices(self, m_1, m_2):
        filas_m_1,filas_m_2 = len(m_1),len(m_2)
        columnas_m_1,columnas_m_2 = len(m_1[0]),len(m_2[0])

        if columnas_m_1 != filas_m_2:
            raise ValueError("Las matrices no se pueden multiplicar")

        producto = []

        for i in range(filas_m_2):
            producto.append([])
            for j in range(columnas_m_2):
                producto[i].append(None)

        for c in range(columnas_m_2):
            for i in range(filas_m_1):
                suma = 0
                for j in range(columnas_m_1):
                    suma += m_1[i][j]*m_2[j][c]
                producto[i][c] = suma

        return producto


    def cifrar(self,clave,texto):
        if len(texto) % len(clave) != 0:
            raise ValueError("La longitud del texto no es multiplo de la longitud de la clave")

        r = math.sqrt(len(clave))
        c_matriz = self.__verifica_clave(r,clave)

        print(c_matriz)

        vectores = []
        v = []
        s = 0
        for i in range(0,len(texto)):
            if s == r :
                vectores.append(v)
                s = 0
                v = []

            i_char = self.abc.index(texto[i])
            v.append([i_char])
            s += 1

            if i == len(texto) - 1:
                vectores.append(v)



        print(vectores)

        # vectores multiplicados por la matriz de cifrado
        v_cripto = [self.__mult_matrices(c_matriz,v) for v in vectores]

        cifrado = []

        # vectores modulo 27
        for vector in v_cripto:
            cifrado.append([int(i[0] % len(self.abc)) for i in vector])

        print(cifrado)

        criptotexto = []

        # obtenemos el caracter de cada valor de los vectores
        for vector in cifrado:
            criptotexto.append([self.abc[i] for i in vector])

        print(criptotexto)



    def descifrar(clave,cripg):
        pass


if __name__ == '__main__':
    print("HOLA MUNDO")
    a = [1,2,3,4]
    for i in a:
        i = 0
    h = Hill("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    h.cifrar("LIMONESAS","QWERTYUIOPASDFGHJK")
    