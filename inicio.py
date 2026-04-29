import customtkinter as ctk
from registro import RegistroFrame
from mascotas import MascotasFrame 

class AppVeterinaria(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Veterinario Pro")
        self.geometry("1200x800")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Colores solicitados
        self.btn_color = "#20c997"
        self.btn_hover = "#19a179"

        # Navegador Lateral
        self.nav = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.nav.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.nav, text="MENÚ", font=("Arial", 20, "bold")).pack(pady=20)

        # Botones Navegación con colores corregidos
        ctk.CTkButton(self.nav, text="Inicio", fg_color=self.btn_color, hover_color=self.btn_hover, command=self.show_inicio).pack(pady=10, padx=20)
        ctk.CTkButton(self.nav, text="Registrar", fg_color=self.btn_color, hover_color=self.btn_hover, command=self.show_registro).pack(pady=10, padx=20)
        ctk.CTkButton(self.nav, text="Pacientes", fg_color=self.btn_color, hover_color=self.btn_hover, command=self.show_mascotas).pack(pady=10, padx=20)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_inicio()

    def show_inicio(self):
        for w in self.container.winfo_children(): w.destroy()
        ctk.CTkLabel(self.container, text="Bienvenido al Sistema", font=("Arial", 25)).pack(pady=100)

    def show_registro(self):
        for w in self.container.winfo_children(): w.destroy()
        RegistroFrame(self.container).pack(fill="both", expand=True)

    def show_mascotas(self):
        for w in self.container.winfo_children(): w.destroy()
        MascotasFrame(self.container).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppVeterinaria()
    app.mainloop()