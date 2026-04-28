import customtkinter as ctk
from registro import RegistroFrame

class AppVeterinaria(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión Veterinaria")
        self.geometry("900x600")

        # Configuración de cuadrícula (Layout)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- BARRA LATERAL (Navegación) ---
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="MENU", 
                                                   font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Estilo común para los botones
        btn_color = "#20c997"
        btn_hover = "#19a179" # Un tono un poco más oscuro para el efecto visual

        # Botones del Menú
        self.btn_inicio = ctk.CTkButton(self.navigation_frame, text="Inicio", 
                                        fg_color=btn_color, hover_color=btn_hover, command=self.show_inicio)
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        self.btn_registro = ctk.CTkButton(self.navigation_frame, text="Registro", 
                                          fg_color=btn_color, hover_color=btn_hover, command=self.show_registro)
        self.btn_registro.grid(row=2, column=0, padx=20, pady=10)

        self.btn_mascotas = ctk.CTkButton(self.navigation_frame, text="Mascotas", 
                                          fg_color=btn_color, hover_color=btn_hover, command=self.show_mascotas)
        self.btn_mascotas.grid(row=3, column=0, padx=20, pady=10)

        self.btn_agenda = ctk.CTkButton(self.navigation_frame, text="Agenda", 
                                        fg_color=btn_color, hover_color=btn_hover, command=self.show_agenda)
        self.btn_agenda.grid(row=4, column=0, padx=20, pady=10)

        self.btn_ingresos = ctk.CTkButton(self.navigation_frame, text="Ingresos", 
                                          fg_color=btn_color, hover_color=btn_hover, command=self.show_ingresos)
        self.btn_ingresos.grid(row=5, column=0, padx=20, pady=10)

        self.btn_egresos = ctk.CTkButton(self.navigation_frame, text="Egresos", 
                                         fg_color=btn_color, hover_color=btn_hover, command=self.show_egresos)
        self.btn_egresos.grid(row=6, column=0, padx=20, pady=10)

        self.btn_config = ctk.CTkButton(self.navigation_frame, text="Configuración", 
                                        fg_color=btn_color, hover_color=btn_hover, command=self.show_config)
        self.btn_config.grid(row=7, column=0, padx=20, pady=10)

        # --- CONTENEDOR PRINCIPAL (Donde cambia el contenido) ---
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        
        # Label de bienvenida por defecto
        self.label_welcome = ctk.CTkLabel(self.main_container, text="Bienvenido al Sistema Veterinaria", font=("Arial", 24))
        self.label_welcome.pack(pady=100)

    # Funciones de navegación
    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_inicio(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Panel de Inicio / Dashboard", font=("Arial", 20)).pack(pady=20)

    def show_registro(self):
        self.clear_main_container()
        # Frame de registro 
        self.frame_registro = RegistroFrame(self.main_container, fg_color="transparent")
        self.frame_registro.pack(fill="both", expand=True)

    def show_mascotas(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Listado de Pacientes (Mascotas)", font=("Arial", 20)).pack(pady=20)

    def show_agenda(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Calendario de Citas Médicas", font=("Arial", 20)).pack(pady=20)

    def show_ingresos(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Control de Ventas e Ingresos", font=("Arial", 20)).pack(pady=20)

    def show_egresos(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Gastos y Compras", font=("Arial", 20)).pack(pady=20)

    def show_config(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="Configuración del Sistema", font=("Arial", 20)).pack(pady=20)

if __name__ == "__main__":
    app = AppVeterinaria()
    app.mainloop()