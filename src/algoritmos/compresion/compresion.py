# src/algoritmos/compresion/compresion.py

def comprimir_origen(texto):
    """
    ENFOQUE DE ORIGEN: Compresión RLE con ciclo For y concatenación.
    Construye el string comprimido paso a paso, lo cual es costoso en RAM.
    """
    if not texto:
        return ""

    resultado = ""
    contador = 1
    caracter_actual = texto[0]

    for i in range(1, len(texto)):
        if texto[i] == caracter_actual:
            contador += 1
        else:
            # Concatenamos el carácter y la cantidad de veces que apareció
            resultado += caracter_actual + str(contador)
            caracter_actual = texto[i]
            contador = 1
            
    # Agregar el último grupo que quedó pendiente en el ciclo
    resultado += caracter_actual + str(contador)
    return resultado