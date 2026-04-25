def recorrido_dfs(grafo, inicio, visitados=None):
    """
    ENFOQUE OPTIMIZADO: Búsqueda en Profundidad (DFS) Recursivo.
    Explora lo más lejos posible a lo largo de cada rama antes de retroceder.
    """
    if visitados is None:
        visitados = set()
    
    visitados.add(inicio)
    resultado = [inicio]

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            resultado.extend(recorrido_dfs(grafo, vecino, visitados))
    return resultado