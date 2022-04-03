import math

"""
    Autores:
    - Jose Eduardo Gonzalez Jasso. 316093837
    - Diego Dozal Magnani. 316032708

    Clase que implementa el cifrado y decifrado de Hill
    para matrices de 2x2 y 3x3
"""
class Hill():
    def __init__(self,abc):
        """ Constructor que recibe el alfabeto sobre el que se
            va a trabajar
            
            input:
                abc: string. alfabeto de entrada"""
        self.abc = abc


    def __mcd(self,a,b):
        """ 
        Funcion auxiliar que calcula el minimo comun divisor 
        de dos numeros
            
        input:
            a: int. primer numero
            b: int. segundo numero
        output:
            b: int. maximo comun divisor de a y b
        """

        a = abs(a)
        b = abs(b)

        while(a % b != 0):
            a,b = b,a % b
        return b


    def __euclides(self,a,b):
        """
        Funcion que realiza el algoritmo de euclides dados dos numeros
        Esta version se basa en el pseudocodigo mostrado en:
        https://es.wikipedia.org/wiki/Algoritmo_de_Euclides

        input:
            a: int. primer numero
            b: int. segundo numero
        output:
            (mcd,s,t): tuple. tupla que contiene los coeficientes de la siguiente 
                              combinacion lineal mcd(a,b) = sa + tb
        """
        a = abs(a)
        b = abs(b)

        if b == 0:
            return (a,1,0)
        else:
            d,s,t = self.__euclides(b,a % b)
            return (d,t,s - (a // b)*t)        


    def __mult_matrices(self, m_1, m_2):
        """ 
        Funcion que calcula el producto de dos matrices

        input:
            m_1: list of list. matriz 1
            m_2: list of list. matriz 2
        output:
            m_r: list of list. matriz del producto
        exceptions:
            ValueError. Si las matrices no se pueden multiplicar
        
        """
        filas_m_1,filas_m_2 = len(m_1),len(m_2)
        columnas_m_1,columnas_m_2 = len(m_1[0]),len(m_2[0])

        if columnas_m_1 != filas_m_2:
            raise ValueError("Las matrices no se pueden multiplicar")

        # matriz resultante
        m_r = []

        # creamos matriz resultante
        for i in range(filas_m_2):
            m_r.append([-1]*columnas_m_2)

        # llenamos matriz resultante
        for c in range(columnas_m_2):
            for i in range(filas_m_1):
                suma = 0
                for j in range(columnas_m_1):
                    suma += m_1[i][j]*m_2[j][c]
                m_r[i][c] = suma

        return m_r


    def __det(self,m):
        """
        Funcion que calcula el determinante de una matriz
        de 2x2 o 3x3

        input:
            m: list of list. matriz
        output:
            int. determinante de la matriz m
        exceptions:
            ValueError. Si la matriz no es de 2x2 o 3x3
        """
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        elif len(m) == 3:
            d1 = m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[1][0]*m[2][1]
            d2 = m[2][0]*m[1][1]*m[0][2] + m[2][1]*m[1][2]*m[0][0] + m[2][2]*m[1][0]*m[0][1]
            return d1 - d2
        else:
            raise ValueError(
                f'Imposible calcular el determinante de una matriz de tamaño {len(m)}')


    def __inversa(self,m):
        """
        Funcion que calcula la inversa de una matriz de 2x2 o 3x3

        input:
            m: list of list. matriz a invertir
        output:
            l: list of list. matriz inversa de m

        """
        l = [0] * len(m)

        for i in range(0,len(m)):
            l[i] = [0]*len(m)

        if len(m) == 2:
            # intercambiamos la entrada 0,0 con la 1,1
            l[0][0], l[1][1]= m[1][1],m[0][0]

            # multiplicamos por -1 las entradas 0,1 y 1,0
            l[0][1] *= -1
            l[1][0] *= -1

            return l

        elif len(m) == 3:
            cp_m = m.copy()
            n = len(l)

            b = 1

            for i in range(0,n):
                for j in range(0,n):
                    p1 = cp_m[(j+1)%n][(i+1)%n] * cp_m[(j+2)%n][(i+2)%n]
                    p2 = cp_m[(j+1)%n][(i+2)%n] * cp_m[(j+2)%n][(i+1)%n]

                    l[i][j] =  p1 - p2
                    5
                    b += 1
            
            return l

        else:
            raise ValueError("Solo es posible calcular la inversa de una matriz 2x2 o 3x3")



    def __verifica_clave(self,clave):
        """
        Funcion que verifica que la clave sea valida para el
        cifrado de Hill y genera su forma de matriz

        input:
            clave: string. clave de cifrado
        output:
            k_arr: list of list. matriz de la clave de cifrado
        exceptions:
            ValueError. Si la clave no es de longitud 4 o 9
                        Si la matriz de la clave no es invertible
        """
        raiz = int(math.sqrt(len(clave)))

        if not raiz in [2,3]:
            raise ValueError(
                "La clave no tiene una longitud valida (tiene que ser de longitud 4 o 9)")

        # matriz de la clave
        k_arr = [0]*raiz

        # llenamos matriz de la clave
        k = 0
        for i in range(0,raiz):
            fila = []

            for j in range(0,raiz):
                fila.append(self.abc.index(clave[k]))
                k += 1

            k_arr[i] = fila

        # calculamos determinante
        det = round(self.__det(k_arr))

        # verificamos si es invertible sobre mod longitud del alfabeto
        if self.__mcd(det,len(self.abc)) != 1:
            raise ValueError("No es posible invertir la matriz de la clave")

        return k_arr


    def cifrar(self,clave,texto):
        """ 
        Funcion que cifra un texto dada una clave utilizando
        el cifrado de Hill
        
        input:
            clave: string. clave de cifrado
            texto: string. texto a cifrar
        output:
            criptotexto: string. texto cifrado
        exceptions:
            ValueError. Si la longitud del texto no es multilplo de 
                        la longitud de la clave
        
        """
        if len(texto) % len(clave) != 0:
            raise ValueError(
                "La longitud del texto no es multiplo de la longitud de la clave")

        c_matriz = self.__verifica_clave(clave)
        r = math.sqrt(len(clave))

        # calculamos el indice correspondiente de cada caracter del texto
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

        # vectores multiplicados por la matriz de cifrado
        v_cripto = [self.__mult_matrices(c_matriz,v) for v in vectores]

        cifrado = []

        # vectores modulo longitud del alfabeto
        for vector in v_cripto:
            cifrado.append([int(k[0] % len(self.abc)) for k in vector])

        criptotexto = ""

        # obtenemos el caracter de cada valor de los vectores
        for vector in cifrado:
            for ch in [self.abc[i] for i in vector]:
                criptotexto += ch

        return criptotexto


    def descifrar(self,clave,criptograma):
        """
        Funcion que descifra un criptograma dada una clave
        utilizando el criptosistema de Hill

        input:
            clave: string. clave para descifrar
            criptograma: string. texto cifrado
        output:
            txt_claro. string
        """
        d_matriz = self.__verifica_clave(clave)
        inv = self.__inversa(d_matriz)

        r = int(math.sqrt(len(clave)))

        # calculamos el indice correspondiente de cada letra del criptograma
        vectores = []
        v = []
        s = 0
        for i in range(0,len(criptograma)):
            if s == r :
                vectores.append(v)
                s = 0
                v = []

            i_char = self.abc.index(criptograma[i])
            v.append([i_char])
            s += 1

            if i == len(criptograma) - 1:
                vectores.append(v)

        # calculamos el inverso del determinante
        det = round(self.__det(d_matriz)) % len(self.abc)
        _,det_inv,_ = self.__euclides(det,len(self.abc))

        if det_inv < 0:
            det_inv += len(self.abc)

        # calculamos la matriz inversa modulo longitud del abecedario de entrada
        inv_mod = []

        for fila in inv:
            inv_mod.append([(k * det_inv) % len(self.abc) for k in fila])

        # multiplicamos por la matriz de descifrado
        descifrado = [self.__mult_matrices(inv_mod,v) for v in vectores]

        # vectores modulo longitud del alfabeto de entrada
        desc_mod = []

        for vector in descifrado:
            desc_mod.append([int(k[0] % len(self.abc)) for k in vector])

        # obtenemos el caracter de cada valor de los vectores
        txt_claro = ""

        for vector in desc_mod:
            for ch in [self.abc[k] for k in vector]:
                txt_claro += ch

        return txt_claro


if __name__ == '__main__':
    h = Hill("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

    try:
        c = h.cifrar("LIMONESAS","QWERTYUIOPASDFGHJK")
        print("TEXTO CIFRADO: ",c)
        d = h.descifrar("LIMONESAS",c)
        print("TEXTO DESCIFRADO: ",d)
    except ValueError as e:
        print(e)
    