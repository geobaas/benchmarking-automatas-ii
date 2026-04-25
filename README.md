# Proyecto: Desarrollo de un Software de Benchmarking 

**Ingeniería en Sistemas Computacionales | 6o. Semestre**

Este repositorio contiene la implementación de un software de Benchmarking desarrollado para realizar pruebas de rendimiento entre algoritmos que resuelven la misma tarea. El objetivo principal es analizar y comparar su comportamiento midiendo el tiempo de CPU y el uso de memoria bajo las mismas entradas de datos.

## Datos de la Asignatura

* **Nombre de la asignatura:** Lenguajes y Autómatas II
* **Actividad:** Rúbrica Programa Informático Tema 3
* **Nombre del docente:** José Leonel Pech May
* **Nombre del alumno:** Geovanny Francisco Baas Chale
* **Valor de la prueba:** 40 pts
* **Grupo:** 6A / 6B / 6C *(Borra los que no correspondan)*

## Objetivo General

Desarrollar un software que permita realizar pruebas de benchmarking seleccionando al menos dos algoritmos que realicen la misma tarea con diferentes enfoques. El sistema ejecutará ambos algoritmos con los mismos datos de entrada para identificar cuellos de botella y proponer mejoras.

## Algoritmos Evaluados

Se han implementado y comparado pares de algoritmos para las siguientes 6 áreas de estudio:

1. **Compresión de archivos:** (Ej. Algoritmo 1 vs Algoritmo 2)
2. **Recorrido de grafos:** (Ej. BFS vs DFS)
3. **Tablas hash:** (Ej. Resolución por encadenamiento vs Direccionamiento abierto)
4. **Rutas más cortas:** (Ej. Dijkstra vs Bellman-Ford)
5. **Encriptación:** (Ej. AES vs RSA)
6. **Búsqueda binaria en árboles:** (Ej. Árboles AVL vs Árboles Rojo-Negro)

## Características del Benchmarking

Para garantizar una evaluación justa y precisa, el software cumple con los siguientes parámetros:
* **Entradas de Datos:** Se utilizan los mismos conjuntos de datos variados (tamaños pequeños, medianos y grandes) para todos los algoritmos evaluados.
* **Métricas Registradas:**
  *  Tiempo de ejecución (Uso de CPU).
  *  Uso de memoria.
* **Análisis:** Salida de resultados de forma clara, numérica y gráfica para la interpretación de rendimiento.

## Tecnologías y Requisitos

* **Lenguaje de Programación:** Python 3.12
* **Módulos Nativos (Standard Library):**
  * `time`: Uso de `time.perf_counter()` para la medición de alta precisión del tiempo de ejecución (CPU).
  * `tracemalloc`: Para el rastreo detallado y la medición del pico de uso de memoria RAM durante la ejecución de cada algoritmo.
* **Dependencias Externas (Opcionales):**
  * `matplotlib` (Para representación gráfica de los resultados).

## 📖 Instrucciones de Uso (Manual de Usuario)

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/GbReptech/benchmarking-automatas-ii.git](https://github.com/GbReptech/benchmarking-automatas-ii.git)
   cd benchmarking-automatas-ii