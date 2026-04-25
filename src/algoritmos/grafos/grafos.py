from collections import deque

def recorrido_bfs(grafo, inicio):
    """
    ENFOQUE ORIGEN: Búsqueda en Anchura (BFS).
    Utiliza una cola (FIFO) para recorrer nivel por nivel.
    """
    visitados = set()
    cola = deque([inicio])
    resultado = []

    while cola:
        vertice = cola.popleft()
        if vertice not in visitados:
            visitados.add(vertice)
            resultado.append(vertice)
            # Agrega vecinos no visitados
            cola.extend(grafo[vertice] - visitados)
    return resultado