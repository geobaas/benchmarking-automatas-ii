import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import tracemalloc
import sys
import os

# Ajuste de rutas para importar los módulos de algoritmos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importaciones de Encriptación
    from algoritmos.encriptacion.encriptacion import encriptar_cesar
    from algoritmos.encriptacion.encriptacionOpt import encriptar_cesar_optimizado
    
    # Importaciones de Compresión
    from algoritmos.compresion.compresion import comprimir_origen
    from algoritmos.compresion.compresionOpt import comprimir_optimizado
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

        # Layout: Sidebar (izquierda) y Contenedor Principal (derecha)
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

        self.lbl_subtitulo = ctk.CTkLabel(self.main_frame, text="Seleccione un módulo del menú lateral para comenzar", font=("Arial", 16))
        self.lbl_subtitulo.pack(pady=5)

    def seleccionar_tema(self, tema):
        self.tema_actual = tema
        self.lbl_titulo.configure(text=f"Módulo: {tema}")
        self.lbl_subtitulo.configure(text="Cargue un archivo .txt para realizar la comparación de algoritmos")
        
        # Limpiar área de trabajo al cambiar de tema
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
        # Panel para ver códigos/entrada
        frame_visual = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_visual.pack(fill="both", expand=True, padx=10)

        # Nombres dinámicos según el tema
        if self.tema_actual == "Encriptación":
            t1, t2 = "César (Sustitución Tradicional)", "César (Optimizado Join)"
        elif self.tema_actual == "Compresión de archivos":
            t1, t2 = "RLE (Concatenación Tradicional)", "RLE (Optimizado Itertools)"
        else:
            t1, t2 = "Algoritmo Origen", "Algoritmo Optimizado"

        # Columna Izquierda (Origen)
        col1 = ctk.CTkFrame(frame_visual)
        col1.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(col1, text=t1, font=("Arial", 13, "bold"), text_color="#3b8ed0").pack(pady=5)
        self.txt_preview_1 = ctk.CTkTextbox(col1, width=420, height=200)
        self.txt_preview_1.pack(padx=10, pady=10)
        self.txt_preview_1.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")

        # Columna Derecha (Optimizado)
        col2 = ctk.CTkFrame(frame_visual)
        col2.grid(row=0, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(col2, text=t2, font=("Arial", 13, "bold"), text_color="#1f6aa5").pack(pady=5)
        self.txt_preview_2 = ctk.CTkTextbox(col2, width=420, height=200)
        self.txt_preview_2.pack(padx=10, pady=10)
        self.txt_preview_2.insert("0.0", f"--- Entrada Lista ---\n{self.archivo_contenido[:300]}...")

        # Botón para ejecutar el proceso
        self.btn_run = ctk.CTkButton(self.main_frame, text="⚡ EJECUTAR PRUEBA DE RENDIMIENTO", 
                                     fg_color="#28a745", hover_color="#218838",
                                     font=("Arial", 16, "bold"), height=45,
                                     command=self.ejecutar_benchmark)
        self.btn_run.pack(pady=20)

        # Contenedor para resultados (se llena al ejecutar)
        self.res_container = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e", border_width=1)

    def ejecutar_benchmark(self):
        if not self.archivo_contenido:
            messagebox.showwarning("Advertencia", "No hay datos para procesar.")
            return

        res_final = ""
        
        # --- LOGICA DE BENCHMARKING ---
        if self.tema_actual == "Encriptación":
            # Medición Origen
            tracemalloc.start()
            start_t = time.perf_counter()
            _ = encriptar_cesar(self.archivo_contenido)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Medición Optimizado
            tracemalloc.start()
            start_t2 = time.perf_counter()
            res_final = encriptar_cesar_optimizado(self.archivo_contenido)
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        elif self.tema_actual == "Compresión de archivos":
            # Medición Origen
            tracemalloc.start()
            start_t = time.perf_counter()
            _ = comprimir_origen(self.archivo_contenido)
            end_t = time.perf_counter()
            _, mem_o = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Medición Optimizado
            tracemalloc.start()
            start_t2 = time.perf_counter()
            res_final = comprimir_optimizado(self.archivo_contenido)
            end_t2 = time.perf_counter()
            _, mem_p = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        else:
            messagebox.showinfo("Pendiente", "Módulo en construcción.")
            return

        # Cálculos
        t_origen = (end_t - start_t) * 1000
        t_opt = (end_t2 - start_t2) * 1000
        m_origen = mem_o / (1024 * 1024)
        m_opt = mem_p / (1024 * 1024)

        self.mostrar_resultados(t_origen, t_opt, m_origen, m_opt, res_final)

    def mostrar_resultados(self, t1, t2, m1, m2, texto_salida):
        self.res_container.pack(fill="x", padx=30, pady=10)
        
        for widget in self.res_container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.res_container, text="📊 RESULTADOS DE HARDWARE", 
                     font=("Arial", 18, "bold"), text_color="yellow").pack(pady=10)

        # Formato de métricas según tu rúbrica
        texto_stats = (
            f"⏱️ Tiempo de CPU (Origen): {t1:.4f} ms\n"
            f"⏱️ Tiempo de CPU (Optimizado): {t2:.4f} ms\n\n"
            f"💾 Uso de RAM (Origen): {m1:.6f} MB\n"
            f"💾 Uso de RAM (Optimizado): {m2:.6f} MB"
        )
        
        lbl_stats = ctk.CTkLabel(self.res_container, text=texto_stats, font=("Consolas", 14), justify="left")
        lbl_stats.pack(pady=10)

        # Sección de Vista Previa del Mensaje Incriptado/Comprimido
        ctk.CTkLabel(self.res_container, text="🔓 VISTA PREVIA DEL RESULTADO FINAL:", 
                     font=("Arial", 13, "bold")).pack()
        
        txt_res = ctk.CTkTextbox(self.res_container, height=80, width=850, fg_color="#000000")
        txt_res.pack(pady=15, padx=20)
        
        # Limitar vista previa para no saturar la UI
        preview_final = texto_salida[:500] + "\n\n[... Datos truncados por longitud ...]" if len(texto_salida) > 500 else texto_salida
        txt_res.insert("0.0", preview_final)
        txt_res.configure(state="disabled")

if __name__ == "__main__":
    app = BenchmarkingApp()
    app.mainloop()