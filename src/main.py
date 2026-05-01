import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import tracemalloc
import sys
import os

# Ajuste de rutas para importar los módulos de algoritmos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from algoritmos.encriptacion.encriptacion import encriptar_cesar
    from algoritmos.encriptacion.encriptacionOpt import encriptar_cesar_optimizado
    from algoritmos.compresion.compresion import comprimir_origen
    from algoritmos.compresion.compresionOpt import comprimir_optimizado
    from algoritmos.grafos.grafos import recorrido_bfs
    from algoritmos.grafos.grafosOpt import recorrido_dfs
    
    from algoritmos.busqueda.arbol_binario import ArbolBinarioBusqueda
    from algoritmos.busqueda.arbol_avl import ArbolAVL
    from algoritmos.busqueda_listas.secuencial import busqueda_secuencial
    from algoritmos.busqueda_listas.binaria import busqueda_binaria
except ImportError as e:
    print(f"Error al importar módulos: {e}")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BenchmarkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Software de Benchmarking - Lenguajes y Autómatas II")
        self.geometry("1150x850")

        self.archivo_contenido = ""
        self.tema_actual = ""
        
        # [NUEVO] Guardamos ambos resultados por separado
        self.ultimo_resultado_origen = "" 
        self.ultimo_resultado_opt = ""

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="MENÚ TEMAS", font=("Arial", 20, "bold")).pack(pady=25)

        temas = ["Compresión de archivos", "Recorrido de grafos", "Encriptación", 
                 "Árboles (BST vs AVL)", "Búsqueda en Listas"]

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

    def seleccionar_tema(self, tema):
        self.tema_actual = tema
        self.lbl_titulo.configure(text=f"Módulo: {tema}")
        self.lbl_subtitulo.configure(text="Cargue un archivo .txt para realizar la comparación")
        
        for widget in self.main_frame.winfo_children():
            if widget not in [self.lbl_titulo, self.lbl_subtitulo]:
                widget.destroy()

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
        frame_visual = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_visual.pack(fill="both", expand=True, padx=10)

        if self.tema_actual == "Encriptación":
            t1, t2 = "César (Básico)", "César (Optimizado)"
        elif self.tema_actual == "Compresión de archivos":
            t1, t2 = "RLE (Básico)", "RLE (Optimizado)"
        elif self.tema_actual == "Recorrido de grafos":
            t1, t2 = "BFS (Anchura - Cola)", "DFS (Profundidad - Pila)"
        elif self.tema_actual == "Árboles (BST vs AVL)":
            t1, t2 = "Árbol Binario (BST)", "Árbol AVL (Balanceado)"
        elif self.tema_actual == "Búsqueda en Listas":
            t1, t2 = "Secuencial (Normal O(n))", "Binaria (Optimizada O(log n))"
        else:
            t1, t2 = "Algoritmo Origen", "Algoritmo Optimizado"

        # --- PANEL IZQUIERDO (ORIGEN) ---
        col1 = ctk.CTkFrame(frame_visual)
        col1.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(col1, text=t1, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_1 = ctk.CTkTextbox(col1, width=420, height=180)
        self.txt_1.pack(padx=10, pady=10)
        self.txt_1.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")
        # Botón izquierdo (Inicia desactivado)
        self.btn_ver_origen = ctk.CTkButton(col1, text="🔍 Ver Resultado", font=("Arial", 12, "bold"), 
                                            state="disabled", fg_color="#1f538d",
                                            command=lambda: self.abrir_ventana_resultado(t1, self.ultimo_resultado_origen))
        self.btn_ver_origen.pack(pady=10)

        # --- PANEL DERECHO (OPTIMIZADO) ---
        col2 = ctk.CTkFrame(frame_visual)
        col2.grid(row=0, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(col2, text=t2, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_2 = ctk.CTkTextbox(col2, width=420, height=180)
        self.txt_2.pack(padx=10, pady=10)
        self.txt_2.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")
        # Botón derecho (Inicia desactivado)
        self.btn_ver_opt = ctk.CTkButton(col2, text="🔍 Ver Resultado", font=("Arial", 12, "bold"), 
                                         state="disabled", fg_color="#1f538d",
                                         command=lambda: self.abrir_ventana_resultado(t2, self.ultimo_resultado_opt))
        self.btn_ver_opt.pack(pady=10)

        # --- BOTÓN CENTRAL EJECUTAR ---
        self.btn_run = ctk.CTkButton(self.main_frame, text="⚡ EJECUTAR BENCHMARK", fg_color="#28a745", 
                                     font=("Arial", 16, "bold"), height=45, command=self.ejecutar_benchmark)
        self.btn_run.pack(pady=20)

        self.res_container = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")

    def generar_grafo_desde_texto(self, texto):
        lineas = [l for l in texto.split() if l]
        grafo = {}
        for i, palabra in enumerate(lineas):
            if i < 5000:
                vecinos = set()
                if i + 1 < len(lineas): vecinos.add(lineas[i+1])
                if i + 2 < len(lineas): vecinos.add(lineas[i+2])
                grafo[palabra] = vecinos
        return grafo, lineas[0] if lineas else None

    def ejecutar_benchmark(self):
        if not self.archivo_contenido:
            messagebox.showwarning("Advertencia", "No hay datos para procesar.")
            return

        res_origen = ""
        res_opt = ""
        
        if self.tema_actual == "Árboles (BST vs AVL)":
            datos = [15, 9, 20, 6, 14, 17, 64, 13, 26, 72]
            objetivo = 13 
            tracemalloc.start(); start_t = time.perf_counter(); bst = ArbolBinarioBusqueda()
            for p in datos: bst.insertar(p)
            _ = bst.buscar(objetivo); mapa_bst = bst.generar_mapa_visual(); end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start(); start_t2 = time.perf_counter(); avl = ArbolAVL()
            for p in datos: avl.insertar(p)
            encontrado = avl.buscar(objetivo); mapa_avl = avl.generar_mapa_visual(); end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
            self.txt_1.delete("0.0", "end"); self.txt_1.insert("0.0", f"Estructura BST:\n{mapa_bst}")
            self.txt_2.delete("0.0", "end"); self.txt_2.insert("0.0", f"Estructura AVL:\n{mapa_avl}")
            
            res_origen = f"Dibujo Estructura BST:\n{mapa_bst}\n\nObjetivo: {objetivo} -> {'Encontrado' if _ else 'No encontrado'}"
            res_opt = f"Dibujo Estructura AVL:\n{mapa_avl}\n\nObjetivo: {objetivo} -> {'Encontrado' if encontrado else 'No encontrado'}"

        elif self.tema_actual == "Búsqueda en Listas":
            datos = self.archivo_contenido.split()
            if not datos: return
            datos.sort()
            objetivo = "Z_OBJETIVO_FINAL"
            tracemalloc.start(); start_t = time.perf_counter(); i_o = busqueda_secuencial(datos, objetivo); end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start(); start_t2 = time.perf_counter(); i_p = busqueda_binaria(datos, objetivo); end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
            res_origen = f"Análisis Secuencial (O(n)) completado.\nElementos: {len(datos)}\nObjetivo: '{objetivo}'\nResultado: {'No encontrado' if i_o == -1 else f'En índice {i_o}'}"
            res_opt = f"Análisis Binario (O(log n)) completado.\nElementos: {len(datos)}\nObjetivo: '{objetivo}'\nResultado: {'No encontrado' if i_p == -1 else f'En índice {i_p}'}"

        elif self.tema_actual == "Encriptación":
            tracemalloc.start(); start_t = time.perf_counter(); res_origen = encriptar_cesar(self.archivo_contenido); end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start(); start_t2 = time.perf_counter(); res_opt = encriptar_cesar_optimizado(self.archivo_contenido); end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()

        elif self.tema_actual == "Compresión de archivos":
            tracemalloc.start(); start_t = time.perf_counter(); res_origen = comprimir_origen(self.archivo_contenido); end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start(); start_t2 = time.perf_counter(); res_opt = comprimir_optimizado(self.archivo_contenido); end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
        elif self.tema_actual == "Recorrido de grafos":
            grafo, inicio = self.generar_grafo_desde_texto(self.archivo_contenido)
            if not inicio: return
            tracemalloc.start(); start_t = time.perf_counter(); reco_o = recorrido_bfs(grafo, inicio); end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start(); start_t2 = time.perf_counter(); reco_p = recorrido_dfs(grafo, inicio); end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
            res_origen = " -> ".join(map(str, reco_o))
            res_opt = " -> ".join(map(str, reco_p))
            
        else:
            return

        t_origen = (end_t - start_t) * 1000
        t_opt = (end_t2 - start_t2) * 1000
        m_origen = mem_o / (1024 * 1024)
        m_opt = mem_p / (1024 * 1024)

        # Actualizamos la memoria de la aplicación con los dos resultados
        self.ultimo_resultado_origen = res_origen
        self.ultimo_resultado_opt = res_opt

        # Activamos los botones de los paneles
        self.btn_ver_origen.configure(state="normal", fg_color="#007bff")
        self.btn_ver_opt.configure(state="normal", fg_color="#007bff")

        self.mostrar_resultados(t_origen, t_opt, m_origen, m_opt)

    def mostrar_resultados(self, t1, t2, m1, m2):
        self.res_container.pack(fill="x", padx=30, pady=10)
        
        for widget in self.res_container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.res_container, text="📊 RESULTADOS DE HARDWARE", 
                     font=("Arial", 18, "bold"), text_color="yellow").pack(pady=10)

        texto_stats = (
            f"⏱️ Tiempo de CPU (Origen): {t1:.4f} ms\n"
            f"⏱️ Tiempo de CPU (Optimizado): {t2:.4f} ms\n\n"
            f"💾 Uso de RAM (Origen): {m1:.6f} MB\n"
            f"💾 Uso de RAM (Optimizado): {m2:.6f} MB"
        )
        
        lbl_stats = ctk.CTkLabel(self.res_container, text=texto_stats, font=("Consolas", 14), justify="left")
        lbl_stats.pack(pady=10)

        # Dejamos un mensaje limpio indicando dónde ver los datos
        ctk.CTkLabel(self.res_container, text="🔓 ESTADO DEL ANÁLISIS:", font=("Arial", 13, "bold")).pack()
        txt_res = ctk.CTkTextbox(self.res_container, height=40, width=850, fg_color="#000000")
        txt_res.pack(pady=5, padx=20)
        txt_res.insert("0.0", "¡Análisis completado exitosamente! Usa los botones 🔍 en cada panel superior para inspeccionar los datos procesados.")
        txt_res.configure(state="disabled")

    def abrir_ventana_resultado(self, tipo_algoritmo, contenido):
        # Creamos una ventana secundaria
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Resultado - {tipo_algoritmo}")
        ventana.geometry("850x650")
        ventana.attributes("-topmost", True) 

        lbl_titulo = ctk.CTkLabel(ventana, text=f"📄 Resultado: {tipo_algoritmo}", font=("Arial", 20, "bold"), text_color="cyan")
        lbl_titulo.pack(pady=15)

        # Caja de texto grande para todo el resultado
        txt_completo = ctk.CTkTextbox(ventana, width=800, height=550, font=("Consolas", 14))
        txt_completo.pack(padx=20, pady=10, fill="both", expand=True)
        
        txt_completo.insert("0.0", str(contenido))
        txt_completo.configure(state="disabled")

if __name__ == "__main__":
    app = BenchmarkingApp()
    app.mainloop()