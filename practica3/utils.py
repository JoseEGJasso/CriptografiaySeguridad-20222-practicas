from fractions import Fraction

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

# cx = b (mod m) - mcd(c,m) | b
def resolver_ec(c,b,m):
    if type(b) == float:
        f = Fraction(b)
        c = c * f.denominator
        b = f.numerator

    mcd,_,_ = euclides(c,m)

    c,b,m = c/mcd,b/mcd,m/mcd

    n = 0

    while((b+n) % c != 0):
        n += m

    return int((b+n)/c)

def residuo_cuadratico(a,p):
    return (pow(a,p-1/2) - 1) % p