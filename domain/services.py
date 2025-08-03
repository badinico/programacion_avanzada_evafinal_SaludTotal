from typing import List, Optional
from datetime import datetime, timedelta
from .entities import Patient, Appointment, Treatment
from .value_objects import PatientId, Age, Gender, Contact, MedicalHistory
from .dto import PatientDTO, AppointmentDTO, TreatmentDTO, PatientSearchDTO, PatientReportDTO


class PatientService:
    """
    Servicio de dominio para la gestión de pacientes
    """
    
    @staticmethod
    def create_patient(
        name: str,
        age: int,
        gender: str,
        medical_history: str,
        contact: str
    ) -> Patient:
        """
        Crea un nuevo paciente con validación de dominio
        """
        try:
            age_vo = Age(age)
            gender_vo = Gender(gender)
            medical_history_vo = MedicalHistory(medical_history)
            contact_vo = Contact(contact)
            
            patient = Patient(
                id=None,
                name=name,
                age=age_vo,
                gender=gender_vo,
                medical_history=medical_history_vo,
                contact=contact_vo,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            if not patient.is_valid():
                raise ValueError("Los datos del paciente no son válidos")
                
            return patient
            
        except ValueError as e:
            raise ValueError(f"Error al crear paciente: {str(e)}")

    @staticmethod
    def update_patient_medical_history(patient: Patient, new_history: str) -> Patient:
        """
        Actualiza el historial médico del paciente
        """
        try:
            medical_history_vo = MedicalHistory(new_history)
            patient.medical_history = medical_history_vo
            patient.updated_at = datetime.now()
            return patient
        except ValueError as e:
            raise ValueError(f"Error al actualizar historial médico: {str(e)}")

    @staticmethod
    def update_patient_contact(patient: Patient, new_contact: str) -> Patient:
        """
        Actualiza la información de contacto del paciente
        """
        try:
            contact_vo = Contact(new_contact)
            patient.contact = contact_vo
            patient.updated_at = datetime.now()
            return patient
        except ValueError as e:
            raise ValueError(f"Error al actualizar contacto: {str(e)}")

    @staticmethod
    def validate_patient_data(patient: Patient) -> bool:
        """
        Valida que todos los datos del paciente sean correctos
        """
        return patient.is_valid()


class AppointmentService:
    """
    Servicio de dominio para la gestión de citas médicas
    """
    
    @staticmethod
    def create_appointment(
        patient_id: PatientId,
        date: datetime,
        doctor_name: str,
        reason: str,
        notes: Optional[str] = None
    ) -> Appointment:
        """
        Crea una nueva cita médica
        """
        if date < datetime.now():
            raise ValueError("No se puede crear una cita en el pasado")
            
        if not doctor_name or not reason:
            raise ValueError("El nombre del doctor y la razón son obligatorios")
            
        return Appointment(
            id=None,
            patient_id=patient_id,
            date=date,
            doctor_name=doctor_name,
            reason=reason,
            status='scheduled',
            notes=notes
        )

    @staticmethod
    def complete_appointment(appointment: Appointment) -> Appointment:
        """
        Marca una cita como completada
        """
        appointment.complete()
        return appointment

    @staticmethod
    def cancel_appointment(appointment: Appointment) -> Appointment:
        """
        Cancela una cita médica
        """
        appointment.cancel()
        return appointment

    @staticmethod
    def get_upcoming_appointments(appointments: List[Appointment], days: int = 7) -> List[Appointment]:
        """
        Obtiene las citas próximas en los próximos días especificados
        """
        cutoff_date = datetime.now() + timedelta(days=days)
        return [
            apt for apt in appointments 
            if apt.status == 'scheduled' and apt.date <= cutoff_date
        ]


class TreatmentService:
    """
    Servicio de dominio para la gestión de tratamientos médicos
    """
    
    @staticmethod
    def create_treatment(
        patient_id: PatientId,
        diagnosis: str,
        prescription: str,
        start_date: datetime = None
    ) -> Treatment:
        """
        Crea un nuevo tratamiento médico
        """
        if not diagnosis or not prescription:
            raise ValueError("El diagnóstico y la prescripción son obligatorios")
            
        if start_date is None:
            start_date = datetime.now()
            
        return Treatment(
            id=None,
            patient_id=patient_id,
            diagnosis=diagnosis,
            prescription=prescription,
            start_date=start_date,
            status='active'
        )

    @staticmethod
    def complete_treatment(treatment: Treatment) -> Treatment:
        """
        Marca un tratamiento como completado
        """
        treatment.complete()
        return treatment

    @staticmethod
    def discontinue_treatment(treatment: Treatment) -> Treatment:
        """
        Discontinúa un tratamiento
        """
        treatment.discontinue()
        return treatment

    @staticmethod
    def get_active_treatments(treatments: List[Treatment]) -> List[Treatment]:
        """
        Obtiene todos los tratamientos activos
        """
        return [trt for trt in treatments if trt.status == 'active']


class ReportService:
    """
    Servicio de dominio para la generación de reportes
    """
    
    @staticmethod
    def generate_patient_report(
        patients: List[Patient],
        appointments: List[Appointment],
        treatments: List[Treatment]
    ) -> PatientReportDTO:
        """
        Genera un reporte completo de pacientes
        """
        # Estadísticas por género
        patients_by_gender = {}
        for patient in patients:
            gender = patient.gender.value
            patients_by_gender[gender] = patients_by_gender.get(gender, 0) + 1

        # Estadísticas por rango de edad
        patients_by_age_range = {
            '0-18': 0,
            '19-30': 0,
            '31-50': 0,
            '51-70': 0,
            '71+': 0
        }
        
        for patient in patients:
            age = patient.age.value
            if age <= 18:
                patients_by_age_range['0-18'] += 1
            elif age <= 30:
                patients_by_age_range['19-30'] += 1
            elif age <= 50:
                patients_by_age_range['31-50'] += 1
            elif age <= 70:
                patients_by_age_range['51-70'] += 1
            else:
                patients_by_age_range['71+'] += 1

        # Pacientes recientes (últimos 30 días)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_patients = [
            PatientDTO.from_entity(p) for p in patients 
            if p.created_at >= thirty_days_ago
        ]

        # Tratamientos activos
        active_treatments = len([t for t in treatments if t.status == 'active'])

        # Citas próximas
        upcoming_appointments = len([
            a for a in appointments 
            if a.status == 'scheduled' and a.date > datetime.now()
        ])

        return PatientReportDTO(
            total_patients=len(patients),
            patients_by_gender=patients_by_gender,
            patients_by_age_range=patients_by_age_range,
            recent_patients=recent_patients,
            active_treatments=active_treatments,
            upcoming_appointments=upcoming_appointments
        )
