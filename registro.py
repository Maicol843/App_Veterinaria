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
        ctk.CTkLabel(self, text="REGISTRO DE MASCOTA", font=("Arial", 30, "bold")).pack(pady=20)

        # Contenedor Principal para las Columnas
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True, padx=10)
        self.grid_container.columnconfigure((0, 1), weight=1)

        # --- COLUMNA 1: DATOS DE LA MASCOTA ---
        col1 = self.crear_columna(self.grid_container, 0, 0, "DATOS DE LA MASCOTA")
        self.nombre = self.add_input(col1, "Nombre:")
        self.btn_img = ctk.CTkButton(col1, text="Subir Imagen", command=self.subir_img)
        self.btn_img = ctk.CTkButton(col1, text="Subir Imagen", 
        fg_color="#20c997", 
        hover_color="#19a179", 
        command=self.subir_img)
        self.btn_img.pack(pady=5)
        self.especie = self.add_select(col1, "Especie:", ["Perro", "Gato"])
        self.raza = self.add_input(col1, "Raza:")
        self.sexo = self.add_select(col1, "Sexo:", ["Macho", "Hembra"])
        self.f_nac = self.add_input(col1, "Fecha Nacimiento (dd/mm/aaaa):")
        self.edad = self.add_input(col1, "Edad:")
        self.peso = self.add_input(col1, "Peso:")
        self.talla = self.add_select(col1, "Talla:", ["Chico", "Mediano", "Grande"])
        self.otros_anim = self.add_select(col1, "¿Vive con otros?", ["No", "Si"], 
                                         command=lambda v: self.toggle_area(v, self.area_otros))
        self.area_otros = self.add_area(col1, "Cuáles?", visible=False)

        # --- COLUMNA 2: DUEÑO Y CONSULTA ---
        col2 = self.crear_columna(self.grid_container, 0, 1, "DATOS DEL DUEÑO")
        self.dueno = self.add_input(col2, "Nombre y Apellido:")
        self.dir = self.add_input(col2, "Dirección:")
        self.tel = self.add_input(col2, "Teléfono:")
        self.mail = self.add_input(col2, "Correo:")
        ctk.CTkLabel(col2, text="CONSULTA MÉDICA", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(20, 10))
        self.f_con = self.add_input(col2, "Fecha Consulta (dd/mm/aaaa):")
        self.motivo = self.add_area(col2, "Motivo:")
        self.diag = self.add_area(col2, "Diagnóstico:")
        self.precio = self.add_input(col2, "Precio:")

        # --- COLUMNA 3: VACUNAS, DESPAR. Y CASTRACIÓN ---
        col3 = self.crear_columna(self.grid_container, 1, 0, "PLAN DE VACUNAS")
        self.f_vac = self.add_input(col3, "Fecha Vacunación:")
        self.f_prox_vac = self.add_input(col3, "Próxima Vacunación:")
        self.nom_vac = self.add_input(col3, "Vacuna (Nombre):")
        ctk.CTkLabel(col3, text="DESPARACITACIÓN", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(20, 10))
        self.f_des = self.add_input(col3, "Fecha Desparacitación:")
        self.prod_des = self.add_input(col3, "Producto:")
        ctk.CTkLabel(col3, text="CASTRACIÓN", font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=(20, 10))
        self.esteril = self.add_select(col3, "Esterilizado:", ["No", "Si"])
        self.partos = self.add_input(col3, "N° de Partos:")

        # --- COLUMNA 4: SÍNTOMAS Y CIRUGÍAS ---
        col4 = self.crear_columna(self.grid_container, 1, 1, "SINTOMAS, CIRUGÍAS Y TRATAMIENTOS")
        self.rabia = self.add_select(col4, "Rabia:", ["No", "Si"], command=lambda v: self.toggle_area(v, self.area_rabia))
        self.area_rabia = self.add_area(col4, "Cuáles?", visible=False)
        self.alergia = self.add_select(col4, "Alergia:", ["No", "Si"], command=lambda v: self.toggle_area(v, self.area_alergia))
        self.area_alergia = self.add_area(col4, "Cual/es?", visible=False)
        self.enfermedades = self.add_area(col4, "Enfermedades padecidas:")
        self.cirugias = self.add_select(col4, "Cirugías previas:", ["No", "Si"], command=lambda v: self.toggle_area(v, self.area_cirugias))
        self.area_cirugias = self.add_area(col4, "Cual/es?", visible=False)
        self.trata = self.add_area(col4, "Tratamientos:")
        self.medica = self.add_area(col4, "Medicación:")

        # Botón Registrar
        self.btn_reg = ctk.CTkButton(self, text="Registrar 🡆", height=45, fg_color="#20c997", 
                                     hover_color="#19a179", font=("Arial", 18, "bold"), command=self.guardar)
        self.btn_reg.pack(pady=40)

    # --- FUNCIONES AUXILIARES ---
    def crear_columna(self, master, r, c, titulo):
        f = ctk.CTkFrame(master)
        f.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(f, text=titulo, font=("Arial", 16, "bold"), text_color="#20c997").pack(pady=10)
        return f

    def add_input(self, master, txt):
        ctk.CTkLabel(master, text=txt).pack(anchor="w", padx=20)
        e = ctk.CTkEntry(master, width=300)
        e.pack(pady=2, padx=20)
        return e

    def add_select(self, master, txt, vals, command=None):
        ctk.CTkLabel(master, text=txt).pack(anchor="w", padx=20)
        s = ctk.CTkComboBox(master, values=vals, width=300, command=command)
        s.pack(pady=2, padx=20)
        return s

    def add_area(self, master, txt, visible=True):
        lbl = ctk.CTkLabel(master, text=txt)
        if visible: lbl.pack(anchor="w", padx=20)
        t = ctk.CTkTextbox(master, width=300, height=60, border_width=2)
        if visible: t.pack(pady=2, padx=20)
        t.lbl_asociada = lbl
        return t

    def toggle_area(self, valor, area):
        if valor == "Si":
            area.lbl_asociada.pack(anchor="w", padx=20)
            area.pack(pady=2, padx=20)
        else:
            area.pack_forget()
            area.lbl_asociada.pack_forget()

    def subir_img(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.ruta_foto = ruta
            self.btn_img.configure(text="Imagen cargada ✅", fg_color="gray")

    def limpiar_formulario(self):
        """Restablece todos los campos después de guardar"""
        # Limpiar Entries
        entradas = [self.nombre, self.raza, self.f_nac, self.edad, self.peso, self.dueno, 
                    self.dir, self.tel, self.mail, self.f_con, self.precio, self.f_vac, 
                    self.f_prox_vac, self.nom_vac, self.f_des, self.prod_des, self.partos]
        for e in entradas:
            e.delete(0, 'end')

        # Limpiar Textboxes y ocultar dinámicos
        areas = [self.area_otros, self.motivo, self.diag, self.area_rabia, self.area_alergia, 
                 self.enfermedades, self.area_cirugias, self.trata, self.medica]
        for a in areas:
            a.delete("1.0", "end")
            if hasattr(a, 'lbl_asociada'):
                a.pack_forget()
                a.lbl_asociada.pack_forget()

        # Restablecer ComboBoxes
        combos = [self.especie, self.sexo, self.talla, self.otros_anim, self.esteril, 
                  self.rabia, self.alergia, self.cirugias]
        for c in combos:
            c.set(c.cget("values")[0])

        # Reset Foto
        self.ruta_foto = ""
        self.btn_img.configure(text="Subir Imagen", fg_color=["#20c997", "#19a179"])

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
                nombre_mascota, ruta_foto, especie, raza, sexo, fecha_nac, edad, peso, talla, vive_otros, cuales_animales,
                nombre_dueno, direccion, telefono, email, fecha_consulta, motivo_consulta, diagnostico, precio_consulta,
                fecha_vacuna, proxima_vacuna, nombre_vacuna, fecha_despar, producto_despar, esterilizado, num_partos,
                rabia, rabia_detalles, alergia, alergia_detalles, enfermedades, cirugias_previas, cirugias_detalles, tratamientos, medicacion
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                self.nombre.get(), nombre_foto, self.especie.get(), self.raza.get(), self.sexo.get(), self.f_nac.get(), self.edad.get(), self.peso.get(), self.talla.get(), self.otros_anim.get(), self.area_otros.get("1.0", "end-1c"),
                self.dueno.get(), self.dir.get(), self.tel.get(), self.mail.get(), self.f_con.get(), self.motivo.get("1.0", "end-1c"), self.diag.get("1.0", "end-1c"), self.precio.get(),
                self.f_vac.get(), self.f_prox_vac.get(), self.nom_vac.get(), self.f_des.get(), self.prod_des.get(), self.esteril.get(), self.partos.get(),
                self.rabia.get(), self.area_rabia.get("1.0", "end-1c"), self.alergia.get(), self.area_alergia.get("1.0", "end-1c"), self.enfermedades.get("1.0", "end-1c"), self.cirugias.get(), self.area_cirugias.get("1.0", "end-1c"), self.trata.get("1.0", "end-1c"), self.medica.get("1.0", "end-1c")
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Mascota registrada correctamente")
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")