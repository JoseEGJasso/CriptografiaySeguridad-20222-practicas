import sympy
import random as rnd

"""
    Autores:
    - Jose Eduardo Gonzalez Jasso. 316093837
    - Diego Dozal Magnani. 316032708

    Clase que implementa el cifrado RSA. 
    Las funcionalidades de generacion de llaves, cifrado y 
    descifrado son independientes entre si
"""
class RSA:
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


    def __genera_primo(self):
        """
        Funcion que se encarga de generar numeros primos aleatorios entre
        1x10^99 y 1x10^99 + 267987

        input: None
        output:
            int. numero primo entre 1x10^99 y 1x10^99 + 267987
        """
        a = "1"
        b = "1"

        for _ in range(99):
            a += str(0)
            b += str(0)

        a = int(a)
        b = int(b) + 267987

        return sympy.randprime(a,b)


    def __toAscci(self,txt):
        """
        Funcion auxiliar que recibe una cadena y regresa una lista 
        con el codigo ASCCI de cada uno de sus caracteres.

        input:
            txt: str. Cadena de entrada
        output:
            txt_ascci: list. Lista con el codigo ASCCI de todos los caracteres 
                             de la cadena de entrada
        """
        txt_ascci = []

        for c in txt:
            txt_ascci.append(ord(c))

        return txt_ascci

    
    def generar_claves(self):
        """
        Funcion que genera la clave publica y clave privada para 
        el cifrado RSA.

        input: None
        output:
            ((n,e),(n,d)): tuple. Tupla con las dos claves.
                                El primer elemento es la clave publica
                                El segundo elemntos es la clave privada
        """

        # Generacion de primos aleatorios
        p = self.__genera_primo() 
        q = self.__genera_primo()

        n = q * p 

        euler_n = (p-1) * (q-1)
        euler_n = euler_n

        #Generacion de e 
        e = 0 
        while(True):
            e = rnd.randint(1,euler_n)
            if e % 2 != 0: 
                mcd,_,_ = self.__euclides(e,euler_n)
                if mcd == 1 : 
                    break 

        #Generacion de d
        d_info = self.__euclides(e,euler_n)
        d = d_info[1]
        
        if d_info[1]< 0 : 
            d = d_info[1] + euler_n
        
        #Regresamos la clave publica y privada
        return ((n,e),(n,d))


    def cifrar(self,tclaro,public_key):
        """
        Función de cifrado de RSA

        input:
            tclaro: str. Cadena de texto que se va a cifrar
            public_key: tuple. Clave pública generada
        output:
            t_cod: list. Lista con el cifrado de cada caracter del texto 
                         de entrada
        """
        n,e = public_key
        t_ascci = self.__toAscci(tclaro)
        t_cod = [int(pow(m,e,n)) for m in t_ascci]

        return t_cod

    
    def descifrar(self,m_cifrado,private_key): 
        """
        Función de descifrado de RSA

        input:
            m_cifrado: list. Lista con el cifrado de cada caracter de la
                             cadena cifrada
            private_key: tuple. Clave privada generada
        output:
            mensaje: str. Mensaje descifrado
        """
        n = private_key[0]
        d = private_key[1]
        
        mensaje = ''
        for c in m_cifrado : 
            #Codigo ascci descifrado
            ascci_num = pow(c,d,n)  
            mensaje = mensaje + chr(ascci_num)

        return mensaje  

if __name__ == '__main__':
    rsa = RSA()

    k_pub,k_priv = rsa.generar_claves()

    cifrado = rsa.cifrar("HOLA MUNDO",k_pub)
    claro = rsa.descifrar(cifrado,k_priv)

    print("Public Key : "+ str(k_pub))
    print("Private Key : " + str(k_priv))
    print("Texto descifrado:" + claro)