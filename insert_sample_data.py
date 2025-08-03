import mysql.connector
from datetime import datetime, timedelta
from config import DATABASE_CONFIG


def create_sample_data():
    """
    Crea datos de ejemplo para la clínica SaludTotal
    """
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        print("Insertando datos de ejemplo...")
        
        # Insertar pacientes de ejemplo
        patients_data = [
            ('Juan Pérez', 35, 'Masculino', 'Hipertensión arterial, diabetes tipo 2', 'juan.perez@email.com'),
            ('María López', 45, 'Femenino', 'Diabetes mellitus, obesidad', 'maria.lopez@email.com'),
            ('Pedro García', 28, 'Masculino', 'Asma bronquial, alergias estacionales', 'pedro.garcia@email.com'),
            ('Ana Rodríguez', 52, 'Femenino', 'Artritis reumatoide, osteoporosis', 'ana.rodriguez@email.com'),
            ('Carlos Martínez', 38, 'Masculino', 'Hipertensión, colesterol alto', 'carlos.martinez@email.com'),
            ('Laura Sánchez', 29, 'Femenino', 'Migraña crónica, ansiedad', 'laura.sanchez@email.com'),
            ('Roberto Torres', 41, 'Masculino', 'Diabetes tipo 1, retinopatía', 'roberto.torres@email.com'),
            ('Carmen Vega', 47, 'Femenino', 'Fibromialgia, depresión', 'carmen.vega@email.com'),
            ('Miguel Ruiz', 33, 'Masculino', 'Síndrome del intestino irritable', 'miguel.ruiz@email.com'),
            ('Isabel Moreno', 39, 'Femenino', 'Endometriosis, infertilidad', 'isabel.moreno@email.com')
        ]
        
        for i, (name, age, gender, history, contact) in enumerate(patients_data, 1):
            patient_id = f"patient_{i:03d}"
            created_at = datetime.now() - timedelta(days=i*10)
            updated_at = datetime.now()
            
            cursor.execute("""
                INSERT INTO Pacientes (ID, Nombre, Edad, Genero, HistorialMedico, Contacto, CreatedAt, UpdatedAt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, name, age, gender, history, contact, created_at, updated_at))
        
        print(f"Insertados {len(patients_data)} pacientes de ejemplo")
        
        # Insertar citas de ejemplo
        appointments_data = [
            ('apt_001', 'patient_001', datetime.now() + timedelta(days=2), 'Dr. García', 'Control de hipertensión', 'scheduled', 'Paciente estable'),
            ('apt_002', 'patient_002', datetime.now() + timedelta(days=5), 'Dra. Martínez', 'Control de diabetes', 'scheduled', 'Revisar glucemia'),
            ('apt_003', 'patient_003', datetime.now() - timedelta(days=1), 'Dr. López', 'Consulta por asma', 'completed', 'Tratamiento efectivo'),
            ('apt_004', 'patient_004', datetime.now() + timedelta(days=7), 'Dra. Rodríguez', 'Control de artritis', 'scheduled', 'Evaluar dolor'),
            ('apt_005', 'patient_005', datetime.now() + timedelta(days=3), 'Dr. Sánchez', 'Control de colesterol', 'scheduled', 'Paciente mejorando'),
            ('apt_006', 'patient_006', datetime.now() - timedelta(days=2), 'Dra. Torres', 'Consulta por migraña', 'completed', 'Síntomas controlados'),
            ('apt_007', 'patient_007', datetime.now() + timedelta(days=4), 'Dr. Vega', 'Control de diabetes', 'scheduled', 'Revisar retinopatía'),
            ('apt_008', 'patient_008', datetime.now() + timedelta(days=6), 'Dra. Ruiz', 'Control de fibromialgia', 'scheduled', 'Evaluar tratamiento'),
            ('apt_009', 'patient_009', datetime.now() - timedelta(days=3), 'Dr. Moreno', 'Consulta digestiva', 'completed', 'Dieta recomendada'),
            ('apt_010', 'patient_010', datetime.now() + timedelta(days=1), 'Dra. Pérez', 'Control ginecológico', 'scheduled', 'Revisión anual')
        ]
        
        for appointment_id, patient_id, date, doctor, reason, status, notes in appointments_data:
            cursor.execute("""
                INSERT INTO Citas (ID, PatientID, Fecha, Doctor, Razon, Estado, Notas)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (appointment_id, patient_id, date, doctor, reason, status, notes))
        
        print(f"Insertadas {len(appointments_data)} citas de ejemplo")
        
        # Insertar tratamientos de ejemplo
        treatments_data = [
            ('trt_001', 'patient_001', 'Hipertensión arterial', 'Losartán 50mg 1 tableta diaria, dieta baja en sodio, ejercicio moderado', datetime.now() - timedelta(days=30), None, 'active'),
            ('trt_002', 'patient_002', 'Diabetes mellitus tipo 2', 'Metformina 500mg 2 tabletas diarias, insulina NPH 20 unidades nocturnas, control de glucemia', datetime.now() - timedelta(days=45), None, 'active'),
            ('trt_003', 'patient_003', 'Asma bronquial', 'Salbutamol inhalador según necesidad, Budesonida 200mcg 2 inhalaciones diarias', datetime.now() - timedelta(days=20), None, 'active'),
            ('trt_004', 'patient_004', 'Artritis reumatoide', 'Methotrexate 15mg semanal, Ácido fólico 5mg diario, fisioterapia', datetime.now() - timedelta(days=60), None, 'active'),
            ('trt_005', 'patient_005', 'Hipercolesterolemia', 'Atorvastatina 20mg 1 tableta nocturna, dieta baja en grasas, ejercicio cardiovascular', datetime.now() - timedelta(days=25), None, 'active'),
            ('trt_006', 'patient_006', 'Migraña crónica', 'Sumatriptán 50mg según necesidad, Propranolol 40mg 2 tabletas diarias, evitar desencadenantes', datetime.now() - timedelta(days=15), None, 'active'),
            ('trt_007', 'patient_007', 'Diabetes tipo 1', 'Insulina regular 10 unidades antes de cada comida, Insulina NPH 25 unidades nocturnas, control estricto de glucemia', datetime.now() - timedelta(days=90), None, 'active'),
            ('trt_008', 'patient_008', 'Fibromialgia', 'Amitriptilina 25mg nocturna, ejercicio de bajo impacto, terapia cognitivo-conductual', datetime.now() - timedelta(days=40), None, 'active'),
            ('trt_009', 'patient_009', 'Síndrome del intestino irritable', 'Dieta FODMAP, probióticos diarios, manejo del estrés, ejercicio regular', datetime.now() - timedelta(days=35), None, 'active'),
            ('trt_010', 'patient_010', 'Endometriosis', 'Anticonceptivos orales combinados, analgésicos según necesidad, seguimiento ginecológico', datetime.now() - timedelta(days=50), None, 'active')
        ]
        
        for treatment_id, patient_id, diagnosis, prescription, start_date, end_date, status in treatments_data:
            cursor.execute("""
                INSERT INTO Tratamientos (ID, PatientID, Diagnostico, Prescripcion, FechaInicio, FechaFin, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (treatment_id, patient_id, diagnosis, prescription, start_date, end_date, status))
        
        print(f"Insertados {len(treatments_data)} tratamientos de ejemplo")
        
        # Confirmar cambios
        connection.commit()
        print("Datos de ejemplo insertados correctamente")
        
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada")


if __name__ == "__main__":
    create_sample_data() 