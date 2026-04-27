import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import tracemalloc
import sys
import os

# Ajuste de rutas para importar los módulos de algoritmos en Linux/Windows
# Esto asegura que Fedora encuentre la carpeta 'algoritmos' correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # --- IMPORTACIONES DE TUS MÓDULOS ---
    from algoritmos.encriptacion.encriptacion import encriptar_cesar
    from algoritmos.encriptacion.encriptacionOpt import encriptar_cesar_optimizado
    
    from algoritmos.compresion.compresion import comprimir_origen
    from algoritmos.compresion.compresionOpt import comprimir_optimizado
    
    from algoritmos.grafos.grafos import recorrido_bfs
    from algoritmos.grafos.grafosOpt import recorrido_dfs
    
    # Módulos de Árboles (Búsqueda Binaria)
    from algoritmos.busqueda.arbol_binario import ArbolBinarioBusqueda
    from algoritmos.busqueda.arbol_avl import ArbolAVL
    
except ImportError as e:
    print(f"Error al importar módulos: {e}")

# Configuración visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BenchmarkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Software de Benchmarking - Lenguajes y Autómatas II")
        self.geometry("1150x850")

        self.archivo_contenido = ""
        self.tema_actual = ""

        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Menú lateral) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="MENÚ TEMAS", font=("Arial", 20, "bold")).pack(pady=25)

        # Aquí están los botones que activan cada módulo
        temas = ["Compresión de archivos", "Recorrido de grafos", "Encriptación", "Búsqueda binaria"]

        for tema in temas:
            btn = ctk.CTkButton(self.sidebar, text=tema, command=lambda t=tema: self.seleccionar_tema(t))
            btn.pack(pady=8, padx=15, fill="x")

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.lbl_titulo = ctk.CTkLabel(self.main_frame, text="Software de Benchmarking", font=("Arial", 28, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.lbl_subtitulo = ctk.CTkLabel(self.main_frame, text="Seleccione un módulo lateral", font=("Arial", 16))
        self.lbl_subtitulo.pack(pady=5)

        self.res_container = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")

    def seleccionar_tema(self, tema):
        """ Se activa al presionar cualquier botón del menú lateral """
        self.tema_actual = tema
        self.lbl_titulo.configure(text=f"Módulo: {tema}")
        self.lbl_subtitulo.configure(text="Cargue un archivo .txt para realizar la comparación")
        
        # Limpiar interfaz previa
        for widget in self.main_frame.winfo_children():
            if widget not in [self.lbl_titulo, self.lbl_subtitulo, self.res_container]:
                widget.destroy()
        self.res_container.pack_forget()

        self.btn_load = ctk.CTkButton(self.main_frame, text="📁 Cargar archivo .txt", 
                                     font=("Arial", 14), command=self.cargar_archivo)
        self.btn_load.pack(pady=20)

    def cargar_archivo(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.archivo_contenido = f.read()
                self.btn_load.configure(text=f"📄 {os.path.basename(path)} cargado", state="disabled")
                self.preparar_interfaz_benchmark()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def preparar_interfaz_benchmark(self):
        """ Configura los cuadros de texto y el botón de ejecución """
        frame_visual = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_visual.pack(fill="both", expand=True, padx=10)

        # Títulos dinámicos según el tema seleccionado
        if self.tema_actual == "Encriptación":
            t1, t2 = "César (Básico)", "César (Optimizado)"
        elif self.tema_actual == "Compresión de archivos":
            t1, t2 = "RLE (Básico)", "RLE (Optimizado)"
        elif self.tema_actual == "Recorrido de grafos":
            t1, t2 = "BFS (Cola)", "DFS (Pila)"
        elif self.tema_actual == "Búsqueda binaria":
            t1, t2 = "Árbol Binario (BST)", "Árbol AVL (Balanceado)"
        else:
            t1, t2 = "Algoritmo A", "Algoritmo B"

        # Columna 1
        col1 = ctk.CTkFrame(frame_visual)
        col1.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(col1, text=t1, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_1 = ctk.CTkTextbox(col1, width=420, height=180)
        self.txt_1.pack(padx=10, pady=10)
        self.txt_1.insert("0.0", f"--- Datos de Entrada ---\n{self.archivo_contenido[:200]}...")

        # Columna 2
        col2 = ctk.CTkFrame(frame_visual)
        col2.grid(row=0, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(col2, text=t2, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_2 = ctk.CTkTextbox(col2, width=420, height=180)
        self.txt_2.pack(padx=10, pady=10)
        self.txt_2.insert("0.0", f"--- Datos de Entrada ---\n{self.archivo_contenido[:200]}...")

        # El botón que dispara el proceso
        self.btn_run = ctk.CTkButton(self.main_frame, text="⚡ EJECUTAR BENCHMARK", fg_color="#28a745", 
                                     font=("Arial", 16, "bold"), height=45, command=self.ejecutar_benchmark)
        self.btn_run.pack(pady=20)

    def ejecutar_benchmark(self):
        """ Lógica central que mide tiempo y memoria al presionar el botón verde """
        if not self.archivo_contenido:
            return

        res_final = ""
        
        # --- LÓGICA DE BÚSQUEDA BINARIA (ÁRBOLES) ---
        if self.tema_actual == "Búsqueda binaria":
            datos = self.archivo_contenido.split()[:5000] # Limite para evitar recursión infinita en BST
            objetivo = datos[-1] # Buscamos la última palabra para forzar el recorrido completo

            # Test Árbol BST (Origen)
            tracemalloc.start()
            start_t = time.perf_counter()
            bst = ArbolBinarioBusqueda()
            for p in datos: bst.insertar(p)
            _ = bst.buscar(objetivo)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            # Test Árbol AVL (Optimizado)
            tracemalloc.start()
            start_t2 = time.perf_counter()
            avl = ArbolAVL()
            for p in datos: avl.insertar(p)
            encontrado = avl.buscar(objetivo)
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
            res_final = f"Búsqueda finalizada.\nObjetivo: {objetivo}\nResultado: {'Encontrado' if encontrado else 'No encontrado'}"

        # --- LÓGICA DE ENCRIPTACIÓN ---
        elif self.tema_actual == "Encriptación":
            tracemalloc.start()
            start_t = time.perf_counter()
            _ = encriptar_cesar(self.archivo_contenido)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start()
            start_t2 = time.perf_counter()
            res_final = encriptar_cesar_optimizado(self.archivo_contenido)
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()

        # --- LÓGICA DE GRAFOS ---
        elif self.tema_actual == "Recorrido de grafos":
            lineas = self.archivo_contenido.split()
            grafo = {p: set(lineas[i+1:i+3]) for i, p in enumerate(lineas) if i < 3000}
            inicio = lineas[0]

            tracemalloc.start()
            start_t = time.perf_counter()
            _ = recorrido_bfs(grafo, inicio)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start()
            start_t2 = time.perf_counter()
            recorrido = recorrido_dfs(grafo, inicio)
            res_final = " -> ".join(recorrido[:50]) + "..."
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()

        # --- LÓGICA DE COMPRESIÓN ---
        elif self.tema_actual == "Compresión de archivos":
            tracemalloc.start()
            start_t = time.perf_counter()
            _ = comprimir_origen(self.archivo_contenido)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start()
            start_t2 = time.perf_counter()
            res_final = comprimir_optimizado(self.archivo_contenido)
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()

        # Cálculos de resultados
        t_o = (end_t - start_t) * 1000
        t_p = (end_t2 - start_t2) * 1000
        m_o = mem_o / (1024 * 1024)
        m_p = mem_p / (1024 * 1024)

        self.mostrar_resultados(t_o, t_p, m_o, m_p, res_final)

    def mostrar_resultados(self, t1, t2, m1, m2, res_final):
        self.res_container.pack(fill="x", padx=30, pady=10)
        for widget in self.res_container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.res_container, text="📊 MÉTRICAS DE RENDIMIENTO", 
                     font=("Arial", 16, "bold"), text_color="cyan").pack(pady=5)

        stats = (f"Tiempo CPU Origen: {t1:.4f} ms | Optimizado: {t2:.4f} ms\n"
                 f"Uso RAM Origen: {m1:.4f} MB | Optimizado: {m2:.4f} MB")
        
        ctk.CTkLabel(self.res_container, text=stats, font=("Consolas", 12)).pack(pady=5)
        
        txt_output = ctk.CTkTextbox(self.res_container, height=60, width=800)
        txt_output.pack(pady=10)
        txt_output.insert("0.0", f"Resultado: {res_final}")
        txt_output.configure(state="disabled")

if __name__ == "__main__":
    app = BenchmarkingApp()
    app.mainloop()