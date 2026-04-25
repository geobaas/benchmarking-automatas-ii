def encriptar_cesar_optimizado(texto, desplazamiento=3):
    """
    ENFOQUE OPTIMIZADO: List Comprehension y método .join()
    (Mucho más rápido y eficiente en uso de CPU y RAM)
    """
    def procesar_char(c):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            return chr((ord(c) - base + desplazamiento) % 26 + base)
        return c
        
    return "".join(procesar_char(c) for c in texto)