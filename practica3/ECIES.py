import fractions as f

class ECIES():

    def __suma_elipse(self,p,q):
        x1,y1 = p
        x2,y2 = q

        x3,y3 = 0


        if p == q:
            pass
        else:
            pass

        return (x3,y3)
        

    def __producto_elipse(self,n,p):
        r = p

        for _ in range(n):
            r = self.__suma_elipse(r,p)

        return r
            

    def __punto_comprimido(self,n):
        pass

    def cifrado(self):
        pass

    def descifrado(self):
        pass