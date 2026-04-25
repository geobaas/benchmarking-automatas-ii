# src/algoritmos/compresion/compresionOpt.py
import itertools

def comprimir_optimizado(texto):
    """
    ENFOQUE OPTIMIZADO: Compresión RLE usando itertools.groupby y join().
    itertools opera a nivel de C, minimizando el uso de CPU y RAM.
    """
    if not texto:
        return ""
    
    # groupby agrupa automáticamente los caracteres consecutivos idénticos.
    # Usamos comprensión de generadores para armar el formato Letra+Numero y unimos con join.
    return "".join(f"{caracter}{sum(1 for _ in grupo)}" for caracter, grupo in itertools.groupby(texto))