def encriptar_cesar(texto, desplazamiento=3):
    """
    ENFOQUE DE ORIGEN: Concatenación de strings tradicional.
    (Lento y consume más memoria en archivos grandes)
    """
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            ascii_base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - ascii_base + desplazamiento) % 26 + ascii_base)
        else:
            resultado += caracter
    return resultado