import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("veterinaria.db")
    cursor = conexion.cursor()

    # Eliminamos la tabla anterior si existe para aplicar los nuevos cambios
    cursor.execute('DROP TABLE IF EXISTS mascotas')

    cursor.execute('''
        CREATE TABLE mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_mascota TEXT, ruta_foto TEXT, especie TEXT, raza TEXT, 
            sexo TEXT, fecha_nac TEXT, edad TEXT, talla TEXT, 
            vive_otros TEXT, cuales_animales TEXT,
            castrado TEXT, plan_vacuna TEXT, plan_despar TEXT, anamnesis TEXT,
            peso TEXT, temperatura TEXT, llc TEXT, mucosas TEXT, 
            fc TEXT, fr TEXT, pulso TEXT, actitud TEXT,
            cc_piel TEXT, locomotor TEXT, cardiaco TEXT, respiratorio TEXT, 
            digestivo TEXT, urinario TEXT, ganglios TEXT, ojo_oido TEXT, nervioso TEXT,
            exam_comple TEXT, diag_presuntivo TEXT, tratamiento TEXT, control TEXT,
            fecha_consulta TEXT, motivo_consulta TEXT, precio TEXT
        )
    ''')
    conexion.commit()
    conexion.close()
    print("Base de datos actualizada con éxito.")

if __name__ == "__main__":
    crear_base_datos()