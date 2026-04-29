import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class MascotasFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Título
        ctk.CTkLabel(self, text="LISTA DE PACIENTES", font=("Arial", 30, "bold")).pack(pady=20)

        # --- BUSCADOR Y BOTONES ---
        tool_bar = ctk.CTkFrame(self, fg_color="transparent")
        tool_bar.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(tool_bar, placeholder_text="Buscar por mascota, dueño o email...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Restauración de todos los botones con sus colores originales
        ctk.CTkButton(tool_bar, text="Descargar", fg_color="#198754", width=100, command=self.exportar_pdf).pack(side="right", padx=5)
        ctk.CTkButton(tool_bar, text="Restablecer", fg_color="#dc3545", width=100, command=self.restablecer_todo).pack(side="right", padx=5)
        ctk.CTkButton(tool_bar, text="Eliminar", fg_color="#c52434", width=100, command=self.eliminar_registro).pack(side="right", padx=5)
        ctk.CTkButton(tool_bar, text="Ver Ficha", fg_color="#0d6efd", width=100, command=self.ver_ficha).pack(side="right", padx=5)

        style = ttk.Style()
        style.theme_use("default")

        # Configuración de los Datos (Cuerpo de la tabla)
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=40,          
                        font=("Arial", 14),    # Tamaño 14
                        borderwidth=0)
        
        # Configuración de los Encabezados (Header)
        style.configure("Treeview.Heading", 
                        background="#1f1f1f", 
                        foreground="white", 
                        relief="flat",
                        font=("Arial", 14, "bold")) # Tamaño 14 y Negrita para resaltar

        style.map("Treeview", background=[('selected', '#19a179')])

        # --- TABLA ---
        columnas = ("num", "nombre", "dueno", "direccion", "telefono", "email")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", style="Treeview")
        
        headers = ["Nro.", "Mascota", "Dueño", "Dirección", "Teléfono", "Correo"]
        anchos = [60, 150, 180, 180, 130, 200] # Anchos ligeramente ajustados para letra más grande
        
        for col, h, w in zip(columnas, headers, anchos):
            self.tabla.heading(col, text=h)
            self.tabla.column(col, anchor="center", width=w)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)
        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        val = f"%{self.search_entry.get()}%"
        conn = sqlite3.connect("veterinaria.db")
        cursor = conn.cursor()
        
        query = """SELECT id, nombre_mascota, nombre_dueno, apellido_dueno, direccion, telefono, email 
                   FROM mascotas WHERE nombre_mascota LIKE ? OR nombre_dueno LIKE ? OR email LIKE ?"""
        cursor.execute(query, (val, val, val))
        
        for i, row in enumerate(cursor.fetchall(), 1):
            id_db, mascota, n_dueno, a_dueno, direccion, tel, mail = row
            self.tabla.insert("", "end", iid=id_db, values=(i, mascota, f"{n_dueno} {a_dueno}", direccion, tel, mail))
        conn.close()

    def exportar_pdf(self):
        ruta_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not ruta_pdf: return

        try:
            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            titulo = Paragraph("<b>LISTA DE PACIENTES</b>", styles['Title'])
            elementos.append(titulo)
            elementos.append(Spacer(1, 20))

            # Encabezado con letra más grande (tamaño 12)
            data = [["Nro.", "Imagen", "Mascota", "Dueño", "Teléfono"]]
            
            conn = sqlite3.connect("veterinaria.db")
            cursor = conn.cursor()
            # Obtenemos ruta_foto para incluirla en el PDF
            cursor.execute("SELECT ruta_foto, nombre_mascota, nombre_dueno, apellido_dueno, telefono FROM mascotas")
            
            for idx, row in enumerate(cursor.fetchall(), 1):
                r_foto, mascota, n_dueno, a_dueno, tel = row
                
                # Procesar imagen para el PDF
                img_widget = "Sin foto"
                if r_foto:
                    ruta_img = os.path.join("img_Mascotas", r_foto)
                    if os.path.exists(ruta_img):
                        try:
                            img_widget = RLImage(ruta_img, width=40, height=40)
                        except:
                            img_widget = "Error"

                data.append([idx, img_widget, mascota, f"{n_dueno} {a_dueno}", tel])
            
            conn.close()

            # Configuración de tabla PDF: ColWidths ajustados e incremento de FONTSIZE
            tabla_pdf = Table(data, colWidths=[30, 60, 120, 160, 100])
            tabla_pdf.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.cadetblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('FONTSIZE', (0,0), (0,-1), 11),    # Tamaño de letra de los datos
                ('FONTSIZE', (0,0), (-1,0), 13),    # Tamaño de letra del encabezado
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 10),
            ]))

            elementos.append(tabla_pdf)
            doc.build(elementos)
            messagebox.showinfo("Éxito", "PDF generado con imágenes y letra ampliada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {e}")

    def ver_ficha(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un paciente de la lista.")
            return
        messagebox.showinfo("Ficha Técnica", f"Abriendo detalles del ID: {sel[0]}")

    def restablecer_todo(self):
        if messagebox.askyesno("Confirmar", "¿Desea vaciar TODA la base de datos de pacientes?"):
            conn = sqlite3.connect("veterinaria.db")
            conn.cursor().execute("DELETE FROM mascotas")
            conn.commit()
            conn.close()
            self.cargar_datos()

    def eliminar_registro(self):
        sel = self.tabla.selection()
        if not sel: return
        if messagebox.askyesno("Eliminar", "¿Eliminar este registro?"):
            conn = sqlite3.connect("veterinaria.db")
            conn.cursor().execute("DELETE FROM mascotas WHERE id=?", (sel[0],))
            conn.commit()
            conn.close()
            self.cargar_datos()