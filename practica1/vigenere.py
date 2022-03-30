""" Clase que implementa el cifrado y descifrado de Vigenere"""
class Vigenere():
    def __init__(self,abc):
        self.abc = abc
        self.table = self.__generar_tabla(abc)


    def __get_caesar(text,des): 
        """
        Funcion que obtiene el cifrado caesar dado un texto y un entero
        que representa el recorrido del crifrado
        
        input:
            text: string. Texto a cifrar
            des: string. Recorrido del crifrado caesar
        output:
            c: string. Texto crifado
        """
        c = ''
        for i in range(0,len(text)):
            c = c + text[(i+des)%len(text)]

        return c 


    def __generar_tabla(self):
        """
        Funcion que genera la tabla de Vigenere donde cada renglon
        es el cifrado de caesar con el recorrido del indice de cada 
        letra del abecedario

        input: None
        ouput: 
            table: list. Matriz con la tabla para el cifrado de Vigenere
        """
        table=[]
        table.append(self.abc)
        for i in range(1,len(self.abc)):
            table.append(self.__get_caesar(self.abc,i))

        return table


    def cifrar(self, texto, clave):
        """
        Funcion que cifra utilizando el cifrado de Vigenere

        input:
            texto: string. Texto a cifrar
            clave: string. Clave con la que se va a cifrar
        output:
            cifrado: string. Texto cifrado
        """
        cifrado = ''
        j = 0
        for i in range(0,len(texto)): 
            if texto[i] in self.abc: 
                reng_index = self.abc.index(clave[j%len(clave)]) 
                colum_index = self.abc.index(texto[i]) 

                ## Primero accedemos al renglon y luego la columna 
                cifrado = cifrado + self.table[reng_index][colum_index]

                j += 1
            else : 
                cifrado = cifrado + texto[i]
        
        return cifrado


    def descifrar(self, criptograma, clave): 
        """
        Funcion que descifra un criptograma utilizando 
        el cifrado de Vigenere

        input:
            criptograma: string. Texto a descifrar
            clave: string. Clave con la que se va a cifrar
        output:
            mensaje: string. Texto descifrado
        """
        mensaje = ''
        j = 0
        for i in range(0, len(criptograma)): 
            if criptograma[i] in self.abc: 

                # buscamos el renglon correspondiente a la letra de la palabra clave
                reng_index = self.abc.index(clave[j%len(clave)])

                # en el renglon anterior buscamos el indice de la letra del criptograma
                colum_index = self.table[reng_index].index(criptograma[i])

                mensaje = mensaje + self.abc[colum_index]

                j += 1
            else : 
                mensaje = mensaje + criptograma[i]
        
        return mensaje


if __name__ == '__main__':

    v = Vigenere('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ')

    cripto = v.cifrar('ATACAR AL ANOCHECER', 'LIMON')
    print(cripto)
    mensaje = v.descifrar(cripto,'LIMON')
    print(mensaje)
    