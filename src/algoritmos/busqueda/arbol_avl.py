class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # Llevamos un registro de la altura para calcular el balance

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        # 1. Inserción normal tipo Árbol Binario
        if not nodo:
            return NodoAVL(valor)
        elif valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)

        # 2. Actualizamos la altura del nodo actual
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))

        # 3. Obtenemos el factor de balance para ver si se enchuecó
        balance = self._obtener_balance(nodo)

        # 4. Si el nodo se desbalancea, aplicamos las 4 posibles rotaciones
        # Caso Izquierda-Izquierda (Rotación Derecha)
        if balance > 1 and valor < nodo.izquierda.valor:
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Derecha (Rotación Izquierda)
        if balance < -1 and valor > nodo.derecha.valor:
            return self._rotacion_izquierda(nodo)
        
        # Caso Izquierda-Derecha (Rotación Doble)
        if balance > 1 and valor > nodo.izquierda.valor:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Izquierda (Rotación Doble)
        if balance < -1 and valor < nodo.derecha.valor:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        return nodo

    # --- Funciones matemáticas para balancear el árbol ---
    def _rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def _rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def _obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)

    # --- Método de Búsqueda (Idéntico al original para que la competencia sea justa) ---
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None or nodo_actual.valor == valor:
            return nodo_actual
        if nodo_actual.valor < valor:
            return self._buscar_recursivo(nodo_actual.derecha, valor)
        return self._buscar_recursivo(nodo_actual.izquierda, valor)