class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

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

        # 2. Actualizamos la altura
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))

        # 3. Obtenemos el factor de balance
        balance = self._obtener_balance(nodo)

        # 4. Rotaciones para auto-balancear
        if balance > 1 and valor < nodo.izquierda.valor:
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor > nodo.derecha.valor:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and valor > nodo.izquierda.valor:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor < nodo.derecha.valor:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        return nodo

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

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None or nodo_actual.valor == valor:
            return nodo_actual
        if nodo_actual.valor < valor:
            return self._buscar_recursivo(nodo_actual.derecha, valor)
        return self._buscar_recursivo(nodo_actual.izquierda, valor)

    def generar_mapa_visual(self):
        """Genera un dibujo en texto del árbol para la interfaz gráfica"""
        lineas = []
        def _recorrer(nodo, prefijo="", es_izquierdo=True):
            if nodo is not None:
                # Recorremos primero la derecha
                if nodo.derecha:
                    _recorrer(nodo.derecha, prefijo + ("│   " if es_izquierdo else "    "), False)
                
                # Nodo actual
                lineas.append(prefijo + ("└── " if es_izquierdo else "┌── ") + str(nodo.valor))
                
                # Recorremos la izquierda
                if nodo.izquierda:
                    _recorrer(nodo.izquierda, prefijo + ("    " if es_izquierdo else "│   "), True)
                    
        _recorrer(self.raiz, "", True)
        return "\n".join(lineas)