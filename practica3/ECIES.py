from utils import *
import random as rnd

"""
    Autores:
    - Jose Eduardo Gonzalez Jasso. 316093837
    - Diego Dozal Magnani. 316032708

    Clase que implementa el esquema de cifrado híbrido ECIES
    en su versión simplificada
"""
class ECIES():
    def __init__(self,curva,P,m,n,
                Q = None,
                abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        # P, Q y n son la llave publica 
        # m pertenece a Z_n \ {0} o Z_n * y m es la clave privada
        self.E = curva[0]
        self.a = curva[1]
        self.p = curva[2]
        self.P = P 
        self.m = m

        # si no se ingresó el punto Q, lo calculamos
        if Q == None:
            self.Q = self.producto_elipse(m,P)
        else:
            self.Q = Q

        self.n = n
        self.abc = abc


    def __suma_elipse(self,p,q):
        """
        Función auxiliar que suma dos puntos de una curva elíptica. 
        El infinito es representado como un None.

        input:
            p: tuple. Punto de la curva eliptica
            q: tuple. Punto de la curva eliptica
        output:
            (x3,y3): tuple. Suma de los puntos p y q
        """
        # Estos casos representan la suma P + infinito = P
        # para cualquier punto P de la curva
        if p == None and q != None:
            return q
        if p != None and q == None:
            return p

        x1,y1 = p
        x2,y2 = q
        
        if p == q and y1 != 0:
            num = 3 * int(pow(x1,2)) + self.a
            den = 2 * y1
        elif x1 != x2:
            num = y2 - y1
            den = x2 - x1
        # si no se entra a ninguno de los casos anteriores 
        # entonces P + Q = infinito
        else: 
            return None

        lam = num / den

        # si lam no es un entero, entonces despejamos y 
        # resolvemos la ecuacion
        if type(lam) == float:
            lam = resolver_ec(den,num,self.p)
        # en caso contrario solo calculamos el módulo
        else:
            lam = lam % self.p

        x3 = (int(pow(lam,2)) - x1 - x2) % self.p
        y3 = ((lam * (x1 - x3)) - y1) % self.p

        return (x3,y3)
        

    def producto_elipse(self,n,p):
        """
        Función que calcula el producto n por el punto p. Es decir,
        calcula n veces el punto p

        input:
            n: int. Entero por el que se va a multiplicar p
            p: tuple. Punto de la curva eliptica
        output:
            r: tuple. Producto de n*p
        """
        r = p

        for _ in range(n-1):
            r = self.__suma_elipse(r,p)

        return r
        

    def __punto_comprimido(self,p):
        """
        Función auxiliar que calcula el punto comprimido

        input:
            p: tuple. Punto de la curva elíptica
        output:
            tuple. Punto comprimido de p
        """
        return (p[0], p[1] % 2)


    def punto_descompresion(self, punto):
        """
        Función auxiliar que calcula el punto de descompresión

        input:
            punto: tuple. Punto comprimidao del a curva elíptica
        output:
            tuple. Punto descomprimido
        """
        z = self.E(punto[0])

        # si p cumple esta condición entonces usamos la forma rápida
        if (self.p - 3) % 4 == 0 and (es_residuo_cuadratico(z,self.p) or z == 0):
            y = int(pow(z,(self.p + 1)/4)) % self.p
        # si no, iteramos hasta encontrar la raiz
        else:
            y = raiz_congruente(z,self.p)

        if (y-punto[1]) % 2 == 0 : 
            return (punto[0], y)
        else : 
            return (punto[0], self.p -y)


    def cifrar(self, claro):
        """
        Función de cifrado ECIES simplificado

        input:
            claro: str. Texto claro a cifrar
        output:
            txt_cifrado: list. Lista con el cifrado de cada caracter 
                               del texto claro
        """
        # pasamos el texto claro a indices de acuerdo al abecedario
        # ingresado por el usuario
        txt_index = [a % self.p for a in strToIndex(claro,self.abc)]

        txt_cifrado = []

        #Se escoge una k secreta aleatoria en Z_n* 
        k = rnd.randint(1,self.n-1)

        # calculamos kP y kQ
        kP = self.producto_elipse(k,self.P)
        kQ = self.producto_elipse(k,self.Q) # = (x_0, y_0)

        # ciframos
        for x in txt_index: 
            y_1 = self.__punto_comprimido(kP)
            y_2 = x*kQ[0] % self.p 
            txt_cifrado.append((y_1, y_2))

        return txt_cifrado 


    def descifrar(self, cifrado):
        """
        Función de descifrado ECIES simplificado

        input:
            cifrado: list. Lista de tuplas con el texto cifrado
        output:
            des_claro: list. Lista con el texto descifrado
        """      
        claro = []

        # desciframos cada par (p,i)
        for p,i in cifrado: 
            y_1 = self.punto_descompresion(p)
            y_1_m = self.producto_elipse(self.m, y_1) # = (x_0,y_0)

            # calculamos el inverso de x_0
            _,x0_inv,_ = euclides(y_1_m[0], self.p)

            if x0_inv < 0:
                x0_inv += self.p
                
            # aplicamos la funcion d_k
            v = (i*x0_inv) % self.p
            claro.append(v % len(self.abc))

        des_claro = indexToStr(claro,self.abc)

        return des_claro


if __name__ == '__main__':

    #EJEMPLO 1
    cipher = [((17,0),17), ((25,0),4), ((12,1),5), ((22,0),6), 
              ((28,1),23), ((13,1),10), ((6,0),13), ((11,1),24), 
              ((19,1),13), ((24,1),28)] 

    f = lambda x: (int(pow(x,3)) + x + 1) % 29
    a = 1
    p = 29
    E = (f,a,p)
    P = (8,12)
    Q = (25,22)
    m = 4
    n = 29
    e = ECIES(E,P,m,n,Q)
    print("TEXTO DESCIFRADO:",e.descifrar(cipher))


    #EJEMPLO 2 
    cipher_2 = [((9, 1), 2), ((19, 0), 10),((29, 1), 24),((12, 1), 24),
                ((0, 1), 19),((24, 1), 13),((9, 1), 15), ((19, 0), 1),
                ((29, 1), 17),((24, 1), 20),((0, 1), 16),((27, 0), 4),
                ((0, 1), 29)]

    f_2 = lambda x: (int(pow(x,3)) + x + 14) % 31
    a_2 = 1
    p_2 = 31
    E_2 = (f_2,a_2,p_2)
    P_2 = (8,21)
    m_2 = 8
    n_2 = 31
    e_2 = ECIES(E_2,P_2,m_2,n_2,abc='-ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print("TEXTO DESCIFRADO:",e_2.descifrar(cipher_2))


    # EJEMPLO 3
    claro = "HOLAMUNDO"
    c = e.cifrar(claro)
    d = e.descifrar(c)
    print(f'TEXTO DESCIFRADO: {str(d)}')