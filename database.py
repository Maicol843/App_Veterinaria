import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("veterinaria.db")
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_mascota TEXT, ruta_foto TEXT, especie TEXT, raza TEXT, 
            sexo TEXT, fecha_nac TEXT, edad TEXT, peso TEXT, talla TEXT, 
            vive_otros TEXT, cuales_animales TEXT,
            nombre_dueno TEXT, direccion TEXT, telefono TEXT, email TEXT,
            fecha_consulta TEXT, motivo_consulta TEXT, diagnostico TEXT, precio_consulta TEXT,
            fecha_vacuna TEXT, proxima_vacuna TEXT, nombre_vacuna TEXT,
            fecha_despar TEXT, producto_despar TEXT,
            esterilizado TEXT, num_partos TEXT,
            rabia TEXT, rabia_detalles TEXT, alergia TEXT, alergia_detalles TEXT,
            enfermedades TEXT, cirugias_previas TEXT, cirugias_detalles TEXT,
            tratamientos TEXT, medicacion TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_base_datos()