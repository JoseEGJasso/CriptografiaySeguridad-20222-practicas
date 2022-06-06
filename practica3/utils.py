import math

"""
    Autores:
    - Jose Eduardo Gonzalez Jasso. 316093837
    - Diego Dozal Magnani. 316032708

    Modulo de funciones útiles para la implementación de
    un sistema de cifrado
"""

def euclides(a,b):
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
        d,s,t = euclides(b,a % b)
        return (d,t,s - (a // b)*t)  


def resolver_ec(c,b,m):
    """
    Función que resuelve congruencias lineales de la forma
    cx ≡ b (mod m)

    input:
        c: int. Coeficiente que multiplica a x en la ecuación
        b: int. Coeficiente b
        m: int. Módulo de la ecuación
    output:
        int. Solución de la ecuación
    """
    if type(c) == float or type(b) == float:
        raise TypeError("No se aceptan numeros decimales!!!")

    mcd,_,_ = euclides(c,m)

    c,b,m = c/mcd,b/mcd,m/mcd

    n = 0

    while((b+n) % c != 0):
        n += m

    return int((b+n)/c)


def es_residuo_cuadratico(a,p):
    """
    Función que verifica si un entero a es residuo cuadrático (RC) módulo p

    input:
        a: int. Entero a verificar si es RC
        p: int. Módulo del residuo cuadrático
    output:
        boolean. True si es RC
                 False en caso contrario
    """
    return ((int(pow(a,(p-1)/2)) - 1) % p) == 0


def raiz_congruente(b,p):
    """
    Función que resuelve congruencias de la forma x^2 ≡ b (mod p)

    input:
        b: int. Coeficiente b en la ecuación
        p: int. Módulo de la ecuación
    output:
        int. Solucion a la ecuacion
    """
    raiz = math.sqrt(b)

    while(raiz - int(raiz) > 0):
        b += p
        raiz = math.sqrt(b)

    return int(raiz) % p


def strToIndex(s,abc):
    """
    Función que trasnforma un string en una lista con 
    índices que corresponden a la posición del caracter
    en el abecedario de entrada

    input:
        s: str. Cadena a transformar
        abc: str. Abecedario de entrada
    output:
        list. Lista de índices
    """
    return [ abc.index(c) for c in s]


def indexToStr(l,abc):
    """
    Función que transforma una lista de enteros en una lista de 
    caracteres de acuerdo al caracter correspondiente de cada
    entero en el abecedario de entrada

    input:
        l: list. Lista de índices
        abc: str. Abecedario de entrada
    output:
        list. Lista de caracteres
    """
    return  [ abc[i % len(abc)] for i in l ]