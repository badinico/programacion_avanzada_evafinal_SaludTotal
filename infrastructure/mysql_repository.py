import mysql.connector
from typing import List, Optional
from datetime import datetime
from domain.entities import Patient, Appointment, Treatment
from domain.value_objects import PatientId, Age, Gender, Contact, MedicalHistory
from domain.dto import PatientSearchDTO
from config import DATABASE_CONFIG


class MySQLRepository:
    """
    Clase base para repositorios MySQL
    """
    
    def __init__(self):
        self.config = DATABASE_CONFIG
        self._create_tables()

    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return mysql.connector.connect(**self.config)

    def _create_tables(self):
        """Crea las tablas necesarias si no existen"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        # Tabla de pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pacientes (
                ID VARCHAR(36) PRIMARY KEY,
                Nombre VARCHAR(100) NOT NULL,
                Edad INT NOT NULL,
                Genero VARCHAR(10) NOT NULL,
                HistorialMedico TEXT,
                Contacto VARCHAR(100) NOT NULL,
                CreatedAt DATETIME NOT NULL,
                UpdatedAt DATETIME NOT NULL
            )
        """)
        
        # Tabla de citas médicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Citas (
                ID VARCHAR(50) PRIMARY KEY,
                PatientID VARCHAR(36) NOT NULL,
                Fecha DATETIME NOT NULL,
                Doctor VARCHAR(100) NOT NULL,
                Razon VARCHAR(200) NOT NULL,
                Estado VARCHAR(20) NOT NULL,
                Notas TEXT,
                FOREIGN KEY (PatientID) REFERENCES Pacientes(ID)
            )
        """)
        
        # Tabla de tratamientos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tratamientos (
                ID VARCHAR(50) PRIMARY KEY,
                PatientID VARCHAR(36) NOT NULL,
                Diagnostico VARCHAR(200) NOT NULL,
                Prescripcion TEXT NOT NULL,
                FechaInicio DATETIME NOT NULL,
                FechaFin DATETIME,
                Estado VARCHAR(20) NOT NULL,
                FOREIGN KEY (PatientID) REFERENCES Pacientes(ID)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()


class MySQLPatientRepository(MySQLRepository):
    """
    Repositorio MySQL para la gestión de pacientes
    """
    
    def save(self, patient: Patient) -> Patient:
        """Guarda o actualiza un paciente en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            if patient.id and self._exists(patient.id):
                # Actualizar paciente existente
                cursor.execute("""
                    UPDATE Pacientes 
                    SET Nombre = %s, Edad = %s, Genero = %s, HistorialMedico = %s, 
                        Contacto = %s, UpdatedAt = %s
                    WHERE ID = %s
                """, (
                    patient.name,
                    patient.age.value,
                    patient.gender.value,
                    patient.medical_history.value,
                    patient.contact.value,
                    patient.updated_at,
                    str(patient.id)
                ))
            else:
                # Insertar nuevo paciente
                cursor.execute("""
                    INSERT INTO Pacientes (ID, Nombre, Edad, Genero, HistorialMedico, 
                                         Contacto, CreatedAt, UpdatedAt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(patient.id),
                    patient.name,
                    patient.age.value,
                    patient.gender.value,
                    patient.medical_history.value,
                    patient.contact.value,
                    patient.created_at,
                    patient.updated_at
                ))
            
            connection.commit()
            return patient
            
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, patient_id: PatientId) -> Optional[Patient]:
        """Busca un paciente por su ID"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Pacientes WHERE ID = %s
            """, (str(patient_id),))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_patient(row)
            return None
            
        finally:
            cursor.close()
            connection.close()

    def find_all(self) -> List[Patient]:
        """Obtiene todos los pacientes"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM Pacientes ORDER BY Nombre")
            rows = cursor.fetchall()
            return [self._row_to_patient(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def search(self, search_dto: PatientSearchDTO) -> List[Patient]:
        """Busca pacientes según criterios específicos"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM Pacientes WHERE 1=1"
            params = []
            
            if search_dto.name:
                query += " AND Nombre LIKE %s"
                params.append(f"%{search_dto.name}%")
            
            if search_dto.age_min is not None:
                query += " AND Edad >= %s"
                params.append(search_dto.age_min)
            
            if search_dto.age_max is not None:
                query += " AND Edad <= %s"
                params.append(search_dto.age_max)
            
            if search_dto.gender:
                query += " AND Genero = %s"
                params.append(search_dto.gender)
            
            if search_dto.contact:
                query += " AND Contacto LIKE %s"
                params.append(f"%{search_dto.contact}%")
            
            query += " ORDER BY Nombre"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_patient(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def delete(self, patient_id: PatientId) -> bool:
        """Elimina un paciente de la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM Pacientes WHERE ID = %s", (str(patient_id),))
            connection.commit()
            return cursor.rowcount > 0
            
        finally:
            cursor.close()
            connection.close()

    def _exists(self, patient_id: PatientId) -> bool:
        """Verifica si un paciente existe en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM Pacientes WHERE ID = %s", (str(patient_id),))
            count = cursor.fetchone()[0]
            return count > 0
            
        finally:
            cursor.close()
            connection.close()

    def _row_to_patient(self, row: dict) -> Patient:
        """Convierte una fila de la base de datos a una entidad Patient"""
        return Patient(
            id=PatientId.from_string(row['ID']),
            name=row['Nombre'],
            age=Age(row['Edad']),
            gender=Gender(row['Genero']),
            medical_history=MedicalHistory(row['HistorialMedico']),
            contact=Contact(row['Contacto']),
            created_at=row['CreatedAt'],
            updated_at=row['UpdatedAt']
        )


class MySQLAppointmentRepository(MySQLRepository):
    """
    Repositorio MySQL para la gestión de citas médicas
    """
    
    def save(self, appointment: Appointment) -> Appointment:
        """Guarda o actualiza una cita en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            if appointment.id and self._exists(appointment.id):
                # Actualizar cita existente
                cursor.execute("""
                    UPDATE Citas 
                    SET PatientID = %s, Fecha = %s, Doctor = %s, Razon = %s, 
                        Estado = %s, Notas = %s
                    WHERE ID = %s
                """, (
                    str(appointment.patient_id),
                    appointment.date,
                    appointment.doctor_name,
                    appointment.reason,
                    appointment.status,
                    appointment.notes,
                    appointment.id
                ))
            else:
                # Insertar nueva cita
                cursor.execute("""
                    INSERT INTO Citas (ID, PatientID, Fecha, Doctor, Razon, Estado, Notas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    appointment.id,
                    str(appointment.patient_id),
                    appointment.date,
                    appointment.doctor_name,
                    appointment.reason,
                    appointment.status,
                    appointment.notes
                ))
            
            connection.commit()
            return appointment
            
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Busca una cita por su ID"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Citas WHERE ID = %s
            """, (appointment_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_appointment(row)
            return None
            
        finally:
            cursor.close()
            connection.close()

    def find_all(self) -> List[Appointment]:
        """Obtiene todas las citas"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM Citas ORDER BY Fecha")
            rows = cursor.fetchall()
            return [self._row_to_appointment(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def find_by_patient_id(self, patient_id: PatientId) -> List[Appointment]:
        """Obtiene todas las citas de un paciente específico"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Citas WHERE PatientID = %s ORDER BY Fecha
            """, (str(patient_id),))
            
            rows = cursor.fetchall()
            return [self._row_to_appointment(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def _exists(self, appointment_id: str) -> bool:
        """Verifica si una cita existe en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM Citas WHERE ID = %s", (appointment_id,))
            count = cursor.fetchone()[0]
            return count > 0
            
        finally:
            cursor.close()
            connection.close()

    def _row_to_appointment(self, row: dict) -> Appointment:
        """Convierte una fila de la base de datos a una entidad Appointment"""
        return Appointment(
            id=row['ID'],
            patient_id=PatientId.from_string(row['PatientID']),
            date=row['Fecha'],
            doctor_name=row['Doctor'],
            reason=row['Razon'],
            status=row['Estado'],
            notes=row['Notas']
        )


class MySQLTreatmentRepository(MySQLRepository):
    """
    Repositorio MySQL para la gestión de tratamientos médicos
    """
    
    def save(self, treatment: Treatment) -> Treatment:
        """Guarda o actualiza un tratamiento en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            if treatment.id and self._exists(treatment.id):
                # Actualizar tratamiento existente
                cursor.execute("""
                    UPDATE Tratamientos 
                    SET PatientID = %s, Diagnostico = %s, Prescripcion = %s, 
                        FechaInicio = %s, FechaFin = %s, Estado = %s
                    WHERE ID = %s
                """, (
                    str(treatment.patient_id),
                    treatment.diagnosis,
                    treatment.prescription,
                    treatment.start_date,
                    treatment.end_date,
                    treatment.status,
                    treatment.id
                ))
            else:
                # Insertar nuevo tratamiento
                cursor.execute("""
                    INSERT INTO Tratamientos (ID, PatientID, Diagnostico, Prescripcion, 
                                            FechaInicio, FechaFin, Estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    treatment.id,
                    str(treatment.patient_id),
                    treatment.diagnosis,
                    treatment.prescription,
                    treatment.start_date,
                    treatment.end_date,
                    treatment.status
                ))
            
            connection.commit()
            return treatment
            
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, treatment_id: str) -> Optional[Treatment]:
        """Busca un tratamiento por su ID"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Tratamientos WHERE ID = %s
            """, (treatment_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_treatment(row)
            return None
            
        finally:
            cursor.close()
            connection.close()

    def find_all(self) -> List[Treatment]:
        """Obtiene todos los tratamientos"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM Tratamientos ORDER BY FechaInicio DESC")
            rows = cursor.fetchall()
            return [self._row_to_treatment(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def find_by_patient_id(self, patient_id: PatientId) -> List[Treatment]:
        """Obtiene todos los tratamientos de un paciente específico"""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Tratamientos WHERE PatientID = %s ORDER BY FechaInicio DESC
            """, (str(patient_id),))
            
            rows = cursor.fetchall()
            return [self._row_to_treatment(row) for row in rows]
            
        finally:
            cursor.close()
            connection.close()

    def _exists(self, treatment_id: str) -> bool:
        """Verifica si un tratamiento existe en la base de datos"""
        connection = self._get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM Tratamientos WHERE ID = %s", (treatment_id,))
            count = cursor.fetchone()[0]
            return count > 0
            
        finally:
            cursor.close()
            connection.close()

    def _row_to_treatment(self, row: dict) -> Treatment:
        """Convierte una fila de la base de datos a una entidad Treatment"""
        return Treatment(
            id=row['ID'],
            patient_id=PatientId.from_string(row['PatientID']),
            diagnosis=row['Diagnostico'],
            prescription=row['Prescripcion'],
            start_date=row['FechaInicio'],
            end_date=row['FechaFin'],
            status=row['Estado']
        )
