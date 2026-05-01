class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

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