import time
import tracemalloc
import psutil
import os

def medir_rendimiento(nombre_algoritmo, funcion_algoritmo, *args):
    print(f"\n--- Ejecutando: {nombre_algoritmo} ---")
    
    # Iniciar medición de memoria RAM
    tracemalloc.start()
    
    # Medir tiempo de inicio
    tiempo_inicio = time.perf_counter()
    
    #  AQUI SE EJECUTA EL ALGORITMO 
    resultado = funcion_algoritmo(*args)
    
    # Medir tiempo de fin
    tiempo_fin = time.perf_counter()
    
    # Obtener memoria usada (pico máximo durante la ejecución)
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Obtener uso de CPU del proceso actual
    proceso = psutil.Process(os.getpid())
    uso_cpu = proceso.cpu_percent(interval=None)
    
    # Cálculos
    tiempo_total = (tiempo_fin - tiempo_inicio) * 1000 # Convertir a milisegundos
    memoria_mb = memoria_pico / (1024 * 1024) # Convertir a Megabytes
    
    print(f"⏱️ Tiempo: {tiempo_total:.4f} ms")
    print(f"💾 Memoria RAM Pico: {memoria_mb:.6f} MB")
    print(f"⚙️ Uso de CPU del proceso: {uso_cpu}%")
    
    return tiempo_total, memoria_mb