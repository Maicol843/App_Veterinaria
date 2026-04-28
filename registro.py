import customtkinter as ctk
from tkinter import filedialog, messagebox
import sqlite3
import os
import shutil

class RegistroFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.ruta_foto = ""

        # Título Principal
        ctk.CTkLabel(self, text="REGISTRO CLÍNICO VETERINARIO", font=("Arial", 30, "bold")).pack(pady=20)

        # Contenedor Principal
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configuramos 2 columnas con el mismo peso y un espaciado entre ellas
        self.grid_container.columnconfigure((0, 1), weight=1, pad=30)

        # --- FILA 0: PARTE SUPERIOR ---
        # Columna 1: Datos Básicos de la Mascota
        col1 = self.crear_columna(self.grid_container, 0, 0, "DATOS DE LA MASCOTA")
        self.nombre = self.add_input(col1, "Nombre:")
        
        # Botón con ancho original
        self.btn_img = ctk.CTkButton(col1, text="Subir Imagen", fg_color="#20c997", hover_color="#19a179", command=self.subir_img)
        self.btn_img.pack(pady=10)
        
        self.especie = self.add_select(col1, "Especie:", ["Perro", "Gato"])
        self.raza = self.add_input(col1, "Raza:")
        self.sexo = self.add_select(col1, "Sexo:", ["Macho", "Hembra"])
        self.f_nac = self.add_input(col1, "Fecha Nacimiento (dd/mm/aaaa):")
        self.edad = self.add_input(col1, "Edad:")
        self.talla = self.add_select(col1, "Talla:", ["Chico", "Mediano", "Grande"])
        
        # Sección Dinámica: Vive con otros
        self.otros_anim = self.add_select(col1, "¿Vive con otros?", ["No", "Si"], command=lambda v: self.toggle_area(v, self.area_otros))
        
        # Contenedor para que "¿Cuáles?" aparezca inmediatamente debajo
        self.contenedor_otros = ctk.CTkFrame(col1, fg_color="transparent")
        self.contenedor_otros.pack(fill="x")
        self.area_otros = self.add_area(self.contenedor_otros, "Cuáles?", visible=False)

        # Columna 2: Historia Clínica y Constantes Fisiológicas (Sin título general)
        col2 = self.crear_columna(self.grid_container, 0, 1, "") # Título vacío
        
        # Historia Clínica al principio de la columna 2
        ctk.CTkLabel(col2, text="HISTORIA CLÍNICA", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(10, 10))
        self.castrado = self.add_input(col2, "Castrado:") 
        self.plan_vac = self.add_input(col2, "Plan de Vacunación:")
        self.plan_des = self.add_input(col2, "Plan de Desparacitación:")
        self.anamnesis = self.add_area(col2, "Anamnesis:")
        
        # Constantes Fisiológicas debajo de Historia Clínica
        ctk.CTkLabel(col2, text="CONSTANTES FISIOLÓGICAS", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(20, 10))
        self.peso = self.add_input(col2, "Peso (kg):")
        self.temp = self.add_input(col2, "Temperatura (°C):")
        self.llc = self.add_input(col2, "Llenado Capilar:")
        self.mucosas = self.add_input(col2, "Mucosas:")
        self.fc = self.add_input(col2, "Frecuencia Cardíaca:")
        self.fr = self.add_input(col2, "Frcuencia Respiratoria:")
        self.pulso = self.add_input(col2, "Pulso:")
        self.actitud = self.add_input(col2, "Actitud:")

        # --- FILA 1: PARTE INFERIOR ---
        # Columna 3: Examen Físico (Abajo Izquierda)
        col3 = self.crear_columna(self.grid_container, 1, 0, "EXAMEN FÍSICO")
        self.cc_piel = self.add_area(col3, "CC-Piel:")
        self.locomotor = self.add_area(col3, "Locomotor:")
        self.cardiaco = self.add_area(col3, "Cardíaco:")
        self.respiratorio = self.add_area(col3, "Respiratorio:")
        self.digestivo = self.add_area(col3, "Digestivo:")
        self.urinario = self.add_area(col3, "Urinario:")
        self.ganglios = self.add_area(col3, "Ganglios:")
        self.ojo_oido = self.add_area(col3, "Ojo-Oído:")
        self.nervioso = self.add_area(col3, "Nervioso:")

        # Columna 4: Seguimiento y Consulta (Abajo Derecha)
        col4 = self.crear_columna(self.grid_container, 1, 1, "SEGUIMIENTO")
        self.exam_comple = self.add_area(col4, "Exámenes Complementarios:")
        self.diag_presun = self.add_area(col4, "Diagnóstico Presuntivo:")
        self.trata = self.add_area(col4, "Tratamiento:")
        self.control = self.add_area(col4, "Control:")
        
        ctk.CTkLabel(col4, text="CONSULTA MÉDICA", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(25, 10))
        self.f_con = self.add_input(col4, "Fecha Consulta (dd/mm/aaaa):")
        self.motivo = self.add_select(col4, "Motivo:", ["Consulta general", "Dermatológico", "Neurológico", "Cardíaco", "Oncológico"])
        self.precio = self.add_input(col4, "Precio:")

        # Botón Registrar
        self.btn_reg = ctk.CTkButton(self, text="Registrar 🡆", height=45, fg_color="#20c997", 
                                     hover_color="#19a179", font=("Arial", 18, "bold"), command=self.guardar)
        self.btn_reg.pack(pady=50)

    # --- FUNCIONES AUXILIARES ---
    def crear_columna(self, master, r, c, titulo):
        f = ctk.CTkFrame(master)
        f.grid(row=r, column=c, padx=25, pady=20, sticky="nsew") 
        if titulo:
            ctk.CTkLabel(f, text=titulo, font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=15)
        return f

    def add_input(self, master, txt):
        ctk.CTkLabel(master, text=txt).pack(anchor="w", padx=30)
        e = ctk.CTkEntry(master, width=420)
        e.pack(pady=5, padx=30)
        return e

    def add_select(self, master, txt, vals, command=None):
        ctk.CTkLabel(master, text=txt).pack(anchor="w", padx=30)
        s = ctk.CTkComboBox(master, values=vals, width=420, command=command)
        s.pack(pady=5, padx=30)
        return s

    def add_area(self, master, txt, visible=True):
        lbl = ctk.CTkLabel(master, text=txt)
        if visible: lbl.pack(anchor="w", padx=30)
        t = ctk.CTkTextbox(master, width=420, height=85, border_width=2)
        if visible: t.pack(pady=5, padx=30)
        t.lbl_asociada = lbl
        return t

    def toggle_area(self, valor, area):
        if valor == "Si":
            area.lbl_asociada.pack(anchor="w", padx=30)
            area.pack(pady=5, padx=30)
        else:
            area.pack_forget()
            area.lbl_asociada.pack_forget()

    def subir_img(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.ruta_foto = ruta
            self.btn_img.configure(text="Imagen cargada ✅", fg_color="gray")

    def limpiar_formulario(self):
        entradas = [self.nombre, self.raza, self.f_nac, self.edad, self.castrado, self.plan_vac, self.plan_des, 
                    self.peso, self.temp, self.llc, self.mucosas, self.fc, self.fr, self.pulso, 
                    self.actitud, self.f_con, self.precio]
        for e in entradas:
            e.delete(0, 'end')

        areas = [self.area_otros, self.anamnesis, self.cc_piel, self.locomotor, self.cardiaco, 
                 self.respiratorio, self.digestivo, self.urinario, self.ganglios, self.ojo_oido, 
                 self.nervioso, self.exam_comple, self.diag_presun, self.trata, self.control]
        for a in areas:
            a.delete("1.0", "end")
            if hasattr(a, 'lbl_asociada') and a == self.area_otros:
                a.pack_forget()
                a.lbl_asociada.pack_forget()

        combos = [self.especie, self.sexo, self.talla, self.otros_anim, self.motivo]
        for c in combos:
            c.set(c.cget("values")[0])

        self.ruta_foto = ""
        self.btn_img.configure(text="Subir Imagen", fg_color="#20c997", hover_color="#19a179")

    def guardar(self):
        nombre_foto = "sin_foto.png"
        if self.ruta_foto:
            if not os.path.exists("img_Mascotas"): os.makedirs("img_Mascotas")
            nombre_foto = f"{self.nombre.get()}_{os.path.basename(self.ruta_foto)}"
            shutil.copy(self.ruta_foto, os.path.join("img_Mascotas", nombre_foto))

        try:
            conn = sqlite3.connect("veterinaria.db")
            c = conn.cursor()
            c.execute('''INSERT INTO mascotas (
                nombre_mascota, ruta_foto, especie, raza, sexo, fecha_nac, edad, talla, vive_otros, cuales_animales,
                castrado, plan_vacuna, plan_despar, anamnesis, peso, temperatura, llc, mucosas, fc, fr, pulso, actitud,
                cc_piel, locomotor, cardiaco, respiratorio, digestivo, urinario, ganglios, ojo_oido, nervioso,
                exam_comple, diag_presuntivo, tratamiento, control, fecha_consulta, motivo_consulta, precio
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                self.nombre.get(), nombre_foto, self.especie.get(), self.raza.get(), self.sexo.get(), self.f_nac.get(), self.edad.get(), self.talla.get(), self.otros_anim.get(), self.area_otros.get("1.0", "end-1c"),
                self.castrado.get(), self.plan_vac.get(), self.plan_des.get(), self.anamnesis.get("1.0", "end-1c"), self.peso.get(), self.temp.get(), self.llc.get(), self.mucosas.get(), self.fc.get(), self.fr.get(), self.pulso.get(), self.actitud.get(),
                self.cc_piel.get("1.0", "end-1c"), self.locomotor.get("1.0", "end-1c"), self.cardiaco.get("1.0", "end-1c"), self.respiratorio.get("1.0", "end-1c"), self.digestivo.get("1.0", "end-1c"), self.urinario.get("1.0", "end-1c"), self.ganglios.get("1.0", "end-1c"), self.ojo_oido.get("1.0", "end-1c"), self.nervioso.get("1.0", "end-1c"),
                self.exam_comple.get("1.0", "end-1c"), self.diag_presun.get("1.0", "end-1c"), self.trata.get("1.0", "end-1c"), self.control.get("1.0", "end-1c"), self.f_con.get(), self.motivo.get(), self.precio.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Se registró el paciente, correctamente")
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")