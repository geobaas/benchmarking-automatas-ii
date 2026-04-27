class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # Método para insertar datos (Ideal para preparar el benchmarking)
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecha, valor)

    # Método de Búsqueda (Este es el que mediremos con psutil)
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        # Caso base: la raíz es nula o el valor está en la raíz
        if nodo_actual is None or nodo_actual.valor == valor:
            return nodo_actual
        
        # El valor es mayor que el valor de la raíz
        if nodo_actual.valor < valor:
            return self._buscar_recursivo(nodo_actual.derecha, valor)
        
        # El valor es menor que el valor de la raíz
        return self._buscar_recursivo(nodo_actual.izquierda, valor)