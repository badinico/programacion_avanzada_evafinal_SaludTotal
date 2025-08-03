from typing import List, Optional
from datetime import datetime
from domain.entities import Patient, Appointment, Treatment
from domain.value_objects import PatientId, Age, Gender, Contact, MedicalHistory
from domain.dto import PatientDTO, AppointmentDTO, TreatmentDTO, PatientSearchDTO, PatientReportDTO
from domain.services import PatientService, AppointmentService, TreatmentService, ReportService


class PatientUseCase:
    """
    Casos de uso para la gestión de pacientes
    """
    
    def __init__(self, patient_repository):
        self.patient_repository = patient_repository
        self.patient_service = PatientService()

    def create_patient(
        self,
        name: str,
        age: int,
        gender: str,
        medical_history: str,
        contact: str
    ) -> PatientDTO:
        """
        Crea un nuevo paciente en el sistema
        """
        try:
            patient = self.patient_service.create_patient(
                name=name,
                age=age,
                gender=gender,
                medical_history=medical_history,
                contact=contact
            )
            
            saved_patient = self.patient_repository.save(patient)
            return PatientDTO.from_entity(saved_patient)
            
        except Exception as e:
            raise Exception(f"Error al crear paciente: {str(e)}")

    def get_all_patients(self) -> List[PatientDTO]:
        """
        Obtiene todos los pacientes del sistema
        """
        try:
            patients = self.patient_repository.find_all()
            return [PatientDTO.from_entity(patient) for patient in patients]
        except Exception as e:
            raise Exception(f"Error al obtener pacientes: {str(e)}")

    def get_patient_by_id(self, patient_id: str) -> Optional[PatientDTO]:
        """
        Obtiene un paciente por su ID
        """
        try:
            patient = self.patient_repository.find_by_id(PatientId.from_string(patient_id))
            if patient:
                return PatientDTO.from_entity(patient)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener paciente: {str(e)}")

    def update_patient_medical_history(self, patient_id: str, new_history: str) -> PatientDTO:
        """
        Actualiza el historial médico de un paciente
        """
        try:
            patient = self.patient_repository.find_by_id(PatientId.from_string(patient_id))
            if not patient:
                raise ValueError("Paciente no encontrado")
                
            updated_patient = self.patient_service.update_patient_medical_history(patient, new_history)
            saved_patient = self.patient_repository.save(updated_patient)
            return PatientDTO.from_entity(saved_patient)
            
        except Exception as e:
            raise Exception(f"Error al actualizar historial médico: {str(e)}")

    def update_patient_contact(self, patient_id: str, new_contact: str) -> PatientDTO:
        """
        Actualiza la información de contacto de un paciente
        """
        try:
            patient = self.patient_repository.find_by_id(PatientId.from_string(patient_id))
            if not patient:
                raise ValueError("Paciente no encontrado")
                
            updated_patient = self.patient_service.update_patient_contact(patient, new_contact)
            saved_patient = self.patient_repository.save(updated_patient)
            return PatientDTO.from_entity(saved_patient)
            
        except Exception as e:
            raise Exception(f"Error al actualizar contacto: {str(e)}")

    def search_patients(self, search_dto: PatientSearchDTO) -> List[PatientDTO]:
        """
        Busca pacientes según criterios específicos
        """
        try:
            patients = self.patient_repository.search(search_dto)
            return [PatientDTO.from_entity(patient) for patient in patients]
        except Exception as e:
            raise Exception(f"Error al buscar pacientes: {str(e)}")

    def delete_patient(self, patient_id: str) -> bool:
        """
        Elimina un paciente del sistema
        """
        try:
            return self.patient_repository.delete(PatientId.from_string(patient_id))
        except Exception as e:
            raise Exception(f"Error al eliminar paciente: {str(e)}")


class AppointmentUseCase:
    """
    Casos de uso para la gestión de citas médicas
    """
    
    def __init__(self, appointment_repository, patient_repository):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.appointment_service = AppointmentService()

    def create_appointment(
        self,
        patient_id: str,
        date: datetime,
        doctor_name: str,
        reason: str,
        notes: Optional[str] = None
    ) -> AppointmentDTO:
        """
        Crea una nueva cita médica
        """
        try:
            patient = self.patient_repository.find_by_id(PatientId.from_string(patient_id))
            if not patient:
                raise ValueError("Paciente no encontrado")
                
            appointment = self.appointment_service.create_appointment(
                patient_id=patient.id,
                date=date,
                doctor_name=doctor_name,
                reason=reason,
                notes=notes
            )
            
            saved_appointment = self.appointment_repository.save(appointment)
            return AppointmentDTO.from_entity(saved_appointment)
            
        except Exception as e:
            raise Exception(f"Error al crear cita: {str(e)}")

    def get_all_appointments(self) -> List[AppointmentDTO]:
        """
        Obtiene todas las citas del sistema
        """
        try:
            appointments = self.appointment_repository.find_all()
            return [AppointmentDTO.from_entity(appointment) for appointment in appointments]
        except Exception as e:
            raise Exception(f"Error al obtener citas: {str(e)}")

    def get_appointments_by_patient(self, patient_id: str) -> List[AppointmentDTO]:
        """
        Obtiene todas las citas de un paciente específico
        """
        try:
            appointments = self.appointment_repository.find_by_patient_id(PatientId.from_string(patient_id))
            return [AppointmentDTO.from_entity(appointment) for appointment in appointments]
        except Exception as e:
            raise Exception(f"Error al obtener citas del paciente: {str(e)}")

    def complete_appointment(self, appointment_id: str) -> AppointmentDTO:
        """
        Marca una cita como completada
        """
        try:
            appointment = self.appointment_repository.find_by_id(appointment_id)
            if not appointment:
                raise ValueError("Cita no encontrada")
                
            updated_appointment = self.appointment_service.complete_appointment(appointment)
            saved_appointment = self.appointment_repository.save(updated_appointment)
            return AppointmentDTO.from_entity(saved_appointment)
            
        except Exception as e:
            raise Exception(f"Error al completar cita: {str(e)}")

    def cancel_appointment(self, appointment_id: str) -> AppointmentDTO:
        """
        Cancela una cita médica
        """
        try:
            appointment = self.appointment_repository.find_by_id(appointment_id)
            if not appointment:
                raise ValueError("Cita no encontrada")
                
            updated_appointment = self.appointment_service.cancel_appointment(appointment)
            saved_appointment = self.appointment_repository.save(updated_appointment)
            return AppointmentDTO.from_entity(saved_appointment)
            
        except Exception as e:
            raise Exception(f"Error al cancelar cita: {str(e)}")

    def get_upcoming_appointments(self, days: int = 7) -> List[AppointmentDTO]:
        """
        Obtiene las citas próximas
        """
        try:
            all_appointments = self.appointment_repository.find_all()
            upcoming_appointments = self.appointment_service.get_upcoming_appointments(all_appointments, days)
            return [AppointmentDTO.from_entity(appointment) for appointment in upcoming_appointments]
        except Exception as e:
            raise Exception(f"Error al obtener citas próximas: {str(e)}")


class TreatmentUseCase:
    """
    Casos de uso para la gestión de tratamientos médicos
    """
    
    def __init__(self, treatment_repository, patient_repository):
        self.treatment_repository = treatment_repository
        self.patient_repository = patient_repository
        self.treatment_service = TreatmentService()

    def create_treatment(
        self,
        patient_id: str,
        diagnosis: str,
        prescription: str,
        start_date: datetime = None
    ) -> TreatmentDTO:
        """
        Crea un nuevo tratamiento médico
        """
        try:
            patient = self.patient_repository.find_by_id(PatientId.from_string(patient_id))
            if not patient:
                raise ValueError("Paciente no encontrado")
                
            treatment = self.treatment_service.create_treatment(
                patient_id=patient.id,
                diagnosis=diagnosis,
                prescription=prescription,
                start_date=start_date
            )
            
            saved_treatment = self.treatment_repository.save(treatment)
            return TreatmentDTO.from_entity(saved_treatment)
            
        except Exception as e:
            raise Exception(f"Error al crear tratamiento: {str(e)}")

    def get_all_treatments(self) -> List[TreatmentDTO]:
        """
        Obtiene todos los tratamientos del sistema
        """
        try:
            treatments = self.treatment_repository.find_all()
            return [TreatmentDTO.from_entity(treatment) for treatment in treatments]
        except Exception as e:
            raise Exception(f"Error al obtener tratamientos: {str(e)}")

    def get_treatments_by_patient(self, patient_id: str) -> List[TreatmentDTO]:
        """
        Obtiene todos los tratamientos de un paciente específico
        """
        try:
            treatments = self.treatment_repository.find_by_patient_id(PatientId.from_string(patient_id))
            return [TreatmentDTO.from_entity(treatment) for treatment in treatments]
        except Exception as e:
            raise Exception(f"Error al obtener tratamientos del paciente: {str(e)}")

    def complete_treatment(self, treatment_id: str) -> TreatmentDTO:
        """
        Marca un tratamiento como completado
        """
        try:
            treatment = self.treatment_repository.find_by_id(treatment_id)
            if not treatment:
                raise ValueError("Tratamiento no encontrado")
                
            updated_treatment = self.treatment_service.complete_treatment(treatment)
            saved_treatment = self.treatment_repository.save(updated_treatment)
            return TreatmentDTO.from_entity(saved_treatment)
            
        except Exception as e:
            raise Exception(f"Error al completar tratamiento: {str(e)}")

    def discontinue_treatment(self, treatment_id: str) -> TreatmentDTO:
        """
        Discontinúa un tratamiento
        """
        try:
            treatment = self.treatment_repository.find_by_id(treatment_id)
            if not treatment:
                raise ValueError("Tratamiento no encontrado")
                
            updated_treatment = self.treatment_service.discontinue_treatment(treatment)
            saved_treatment = self.treatment_repository.save(updated_treatment)
            return TreatmentDTO.from_entity(saved_treatment)
            
        except Exception as e:
            raise Exception(f"Error al discontinuar tratamiento: {str(e)}")

    def get_active_treatments(self) -> List[TreatmentDTO]:
        """
        Obtiene todos los tratamientos activos
        """
        try:
            all_treatments = self.treatment_repository.find_all()
            active_treatments = self.treatment_service.get_active_treatments(all_treatments)
            return [TreatmentDTO.from_entity(treatment) for treatment in active_treatments]
        except Exception as e:
            raise Exception(f"Error al obtener tratamientos activos: {str(e)}")


class ReportUseCase:
    """
    Casos de uso para la generación de reportes
    """
    
    def __init__(self, patient_repository, appointment_repository, treatment_repository):
        self.patient_repository = patient_repository
        self.appointment_repository = appointment_repository
        self.treatment_repository = treatment_repository
        self.report_service = ReportService()

    def generate_patient_report(self) -> PatientReportDTO:
        """
        Genera un reporte completo de pacientes
        """
        try:
            patients = self.patient_repository.find_all()
            appointments = self.appointment_repository.find_all()
            treatments = self.treatment_repository.find_all()
            
            return self.report_service.generate_patient_report(patients, appointments, treatments)
            
        except Exception as e:
            raise Exception(f"Error al generar reporte: {str(e)}")
