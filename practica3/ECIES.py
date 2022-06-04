from utils import *
import math
import random as rnd 

class ECIES():
    def __init__(self,curva,P,m,Q,n):
        # P, Q y n son la llave publica 
        # m pertenece a Z_n \ {0} o Z_n * y m es la clave privada
        self.E = curva[0]
        self.a = curva[1]
        self.p = curva[2]
        self.P = P 
        self.m = m
        #Realmente Q = mP entonces se debe quitar Q de los argumentos y ser 
        #self.Q = self.__producto_elipse(m,self.P)
        self.Q = Q
        self.n = n

    # x=1/2 mod n 
    # 2x = 1 mod n
    # lamda x: x^3 + 2x + 5 

    def suma_elipse(self,p,q):
        x1,y1 = p
        x2,y2 = q

        if p == q:
            lam = (3 * pow(x1,2) + self.a) / 2 * y1
        else:
            lam = (y2 - y1) / (x2 - x1) 

        x3 = pow(lam,2) - x1 - x2
        y3 = lam * (x1 - x3) - y1

        if type(x3) == float:
            x3 = resolver_ec(1,x3,self.p)

        if type(y3) == float:
            y3 = resolver_ec(1,y3,self.p)

        return (x3,y3)
        

    def __producto_elipse(self,n,p):
        r = p

        for _ in range(n):
            r = self.__suma_elipse(r,p)

        return r
    
    def __es_residuo_cuadratico(self, x, mod): 
        
        return True  


    #El punto de comprension (P) de un punto P de E es :
    #  Sea P = (x,y) in E -> (P) = (x, y mod 2)
    def __punto_comprimido(self,P):
        return (P[0], P[1] % 2)

    def __punto_descompresion(self, punto):
        z = self.E(punto[0])
        if self.__es_residuo_cuadratico(z,self.p): 
            y = math.sqrt(z) % self.p # Revisar esta parte 
            # checar si y es congruente con i modulo 2
            mcd_y_i = euclides(y,2)[0]
            if mcd_y_i % punto[1] == 0 : 
                return (punto[0], y)
            else : 
                return (punto[0], self.p -y)
        else: 
            try:
                raise Exception('__punto_descompresion: __es_residuo_cuadratico')
            except Exception as error:
                print(f'{z} no es residuo cuadratico')

    #El texto claro sera una lista del estilo ((x, y mod 2), z)
    def cifrado(self, claro):

        cifrado = []
        #Se escoge una k secreta aleatoria en Z_n * 
        #Se escoge una x en Z_p * (esta x aun no me queda claro si es la llave privada u otr cosa)
        k = rnd.randint(1,self.n-1)
        x = rnd.randint(1,self.p-1)
        kP = self.__producto_elipse(k,self.P)
        kQ = self.__producto_elipse(k,self.Q) # = (x_0, y_0)
        for e in claro : 
            y_1 = self.__punto_comprimido(kP)
            y_2 = x*kQ[0] % self.p 
            cifrado.append((y_1, y_2))
        #En el ejemplo, para y_1 , cuando definimos k=7 el profe usa despues k=9, por que? 
        #y_1 = self.__punto_comprimido(x,k) = (x, k mod 2)
        #y_2 = x * x_0 (kQ[0]) mod P 
        #El texto cifrado es la tupla (y_1, y_2)
        return cifrado 

    def descifrado(self, cifrado):

        #Se recibe la tupla (y_1, y_2)
        #Calculamos self.__punto_descompresion(y_1) = P_0 
        #Calculamos self.__producto_elipse(self.m, P_0) = (x_0, x_1)     NOTA : Revisar que x_0 NO SEA el x_0 de kQ en cifrado 
        #luego calculamos el inverso de x_0 en mod self.p , sea x_0^-1
        #despues hacemos dk = y_2 * x_0^-1 mod self.p
        # Se supone que dk es el mensaje desifrado 
        pass