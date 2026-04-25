import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import tracemalloc
import sys
import os

# Ajuste de rutas para importar los módulos de algoritmos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importaciones
    from algoritmos.encriptacion.encriptacion import encriptar_cesar
    from algoritmos.encriptacion.encriptacionOpt import encriptar_cesar_optimizado
    from algoritmos.compresion.compresion import comprimir_origen
    from algoritmos.compresion.compresionOpt import comprimir_optimizado
    from algoritmos.grafos.grafos import recorrido_bfs
    from algoritmos.grafos.grafosOpt import recorrido_dfs
except ImportError as e:
    print(f"Error al importar módulos: {e}")

# Configuración visual de la interfaz
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BenchmarkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Software de Benchmarking - Lenguajes y Autómatas II")
        self.geometry("1150x850")

        self.archivo_contenido = ""
        self.tema_actual = ""

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="MENÚ TEMAS", font=("Arial", 20, "bold")).pack(pady=25)

        temas = ["Compresión de archivos", "Recorrido de grafos", "Tablas hash", 
                 "Rutas más cortas", "Encriptación", "Búsqueda binaria"]

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

        # Configurar títulos dependiendo del tema
        if self.tema_actual == "Encriptación":
            t1, t2 = "César (For)", "César (Join)"
        elif self.tema_actual == "Compresión de archivos":
            t1, t2 = "RLE (For)", "RLE (Itertools)"
        elif self.tema_actual == "Recorrido de grafos":
            t1, t2 = "BFS (Anchura - Cola)", "DFS (Profundidad - Pila)"
        else:
            t1, t2 = "Algoritmo Origen", "Algoritmo Optimizado"

        col1 = ctk.CTkFrame(frame_visual)
        col1.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(col1, text=t1, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_1 = ctk.CTkTextbox(col1, width=420, height=200)
        self.txt_1.pack(padx=10, pady=10)
        # AQUÍ ESTABA EL ERROR 1: Faltaba reinsertar la vista previa del archivo
        self.txt_1.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")

        col2 = ctk.CTkFrame(frame_visual)
        col2.grid(row=0, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(col2, text=t2, font=("Arial", 13, "bold")).pack(pady=5)
        self.txt_2 = ctk.CTkTextbox(col2, width=420, height=200)
        self.txt_2.pack(padx=10, pady=10)
        self.txt_2.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")

        self.btn_run = ctk.CTkButton(self.main_frame, text="⚡ EJECUTAR BENCHMARK", fg_color="#28a745", 
                                     font=("Arial", 16, "bold"), height=45, command=self.ejecutar_benchmark)
        self.btn_run.pack(pady=20)

        self.res_container = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")

    def generar_grafo_desde_texto(self, texto):
        """Convierte texto en lista de adyacencia para los grafos"""
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

        res_final = ""
        
        if self.tema_actual == "Encriptación":
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
            
        elif self.tema_actual == "Recorrido de grafos":
            grafo, inicio = self.generar_grafo_desde_texto(self.archivo_contenido)
            if not inicio: return
            
            tracemalloc.start()
            start_t = time.perf_counter()
            _ = recorrido_bfs(grafo, inicio)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory(); tracemalloc.stop()

            tracemalloc.start()
            start_t2 = time.perf_counter()
            recorrido = recorrido_dfs(grafo, inicio)
            res_final = " -> ".join(map(str, recorrido))  # Formatea el resultado con flechitas
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory(); tracemalloc.stop()
            
        else:
            messagebox.showinfo("Pendiente", "Módulo en construcción.")
            return

        # Cálculos finales
        t_origen = (end_t - start_t) * 1000
        t_opt = (end_t2 - start_t2) * 1000
        m_origen = mem_o / (1024 * 1024)
        m_opt = mem_p / (1024 * 1024)

        self.mostrar_resultados(t_origen, t_opt, m_origen, m_opt, res_final)

    # AQUÍ ESTABA EL ERROR 2: Restauramos tu función de resultados bonita
    def mostrar_resultados(self, t1, t2, m1, m2, texto_salida):
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

        ctk.CTkLabel(self.res_container, text="🔓 VISTA PREVIA DEL RESULTADO FINAL:", 
                     font=("Arial", 13, "bold")).pack()
        
        txt_res = ctk.CTkTextbox(self.res_container, height=80, width=850, fg_color="#000000")
        txt_res.pack(pady=15, padx=20)
        
        # Inyecta el resultado final (ya sea encriptado, comprimido o el recorrido con flechas)
        preview_final = str(texto_salida)[:500] + "\n\n[... Datos truncados por longitud ...]" if len(str(texto_salida)) > 500 else str(texto_salida)
        txt_res.insert("0.0", preview_final)
        txt_res.configure(state="disabled")

if __name__ == "__main__":
    app = BenchmarkingApp()
    app.mainloop()