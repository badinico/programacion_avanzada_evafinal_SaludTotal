from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class PatientDTO:
    """
    DTO para transferir datos de pacientes entre capas
    """
    id: Optional[str]
    name: str
    age: int
    gender: str
    medical_history: str
    contact: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, patient):
        """Crea un DTO desde una entidad Patient"""
        return cls(
            id=str(patient.id) if patient.id else None,
            name=patient.name,
            age=patient.age.value,
            gender=patient.gender.value,
            medical_history=patient.medical_history.value,
            contact=patient.contact.value,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )

    def to_dict(self):
        """Convierte el DTO a un diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'medical_history': self.medical_history,
            'contact': self.contact,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class AppointmentDTO:
    """
    DTO para transferir datos de citas médicas entre capas
    """
    id: Optional[str]
    patient_id: str
    date: datetime
    doctor_name: str
    reason: str
    status: str
    notes: Optional[str] = None

    @classmethod
    def from_entity(cls, appointment):
        """Crea un DTO desde una entidad Appointment"""
        return cls(
            id=appointment.id,
            patient_id=str(appointment.patient_id),
            date=appointment.date,
            doctor_name=appointment.doctor_name,
            reason=appointment.reason,
            status=appointment.status,
            notes=appointment.notes
        )

    def to_dict(self):
        """Convierte el DTO a un diccionario"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date.isoformat() if self.date else None,
            'doctor_name': self.doctor_name,
            'reason': self.reason,
            'status': self.status,
            'notes': self.notes
        }


@dataclass
class TreatmentDTO:
    """
    DTO para transferir datos de tratamientos médicos entre capas
    """
    id: Optional[str]
    patient_id: str
    diagnosis: str
    prescription: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str = 'active'

    @classmethod
    def from_entity(cls, treatment):
        """Crea un DTO desde una entidad Treatment"""
        return cls(
            id=treatment.id,
            patient_id=str(treatment.patient_id),
            diagnosis=treatment.diagnosis,
            prescription=treatment.prescription,
            start_date=treatment.start_date,
            end_date=treatment.end_date,
            status=treatment.status
        )

    def to_dict(self):
        """Convierte el DTO a un diccionario"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status
        }


@dataclass
class PatientSearchDTO:
    """
    DTO para criterios de búsqueda de pacientes
    """
    name: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None

    def to_dict(self):
        """Convierte el DTO a un diccionario"""
        return {
            'name': self.name,
            'age_min': self.age_min,
            'age_max': self.age_max,
            'gender': self.gender,
            'contact': self.contact
        }


@dataclass
class PatientReportDTO:
    """
    DTO para reportes de pacientes
    """
    total_patients: int
    patients_by_gender: dict
    patients_by_age_range: dict
    recent_patients: List[PatientDTO]
    active_treatments: int
    upcoming_appointments: int

    def to_dict(self):
        """Convierte el DTO a un diccionario"""
        return {
            'total_patients': self.total_patients,
            'patients_by_gender': self.patients_by_gender,
            'patients_by_age_range': self.patients_by_age_range,
            'recent_patients': [p.to_dict() for p in self.recent_patients],
            'active_treatments': self.active_treatments,
            'upcoming_appointments': self.upcoming_appointments
        }
