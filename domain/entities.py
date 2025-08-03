from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from .value_objects import PatientId, Age, Gender, Contact, MedicalHistory


@dataclass
class Patient:
    """
    Entidad principal que representa un paciente en el sistema
    """
    id: Optional[PatientId]
    name: str
    age: Age
    gender: Gender
    medical_history: MedicalHistory
    contact: Contact
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = PatientId.generate()
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.now()
        if not hasattr(self, 'updated_at'):
            self.updated_at = datetime.now()

    def update_medical_history(self, new_history: str):
        """Actualiza el historial médico del paciente"""
        self.medical_history = MedicalHistory(new_history)
        self.updated_at = datetime.now()

    def update_contact(self, new_contact: str):
        """Actualiza la información de contacto del paciente"""
        self.contact = Contact(new_contact)
        self.updated_at = datetime.now()

    def is_valid(self) -> bool:
        """Valida que el paciente tenga toda la información requerida"""
        return (
            self.name and 
            self.age.is_valid() and 
            self.gender.is_valid() and 
            self.contact.is_valid()
        )


@dataclass
class Appointment:
    """
    Entidad que representa una cita médica
    """
    id: Optional[str]
    patient_id: PatientId
    date: datetime
    doctor_name: str
    reason: str
    status: str  # 'scheduled', 'completed', 'cancelled'
    notes: Optional[str] = None

    def __post_init__(self):
        if self.id is None:
            self.id = f"apt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def complete(self):
        """Marca la cita como completada"""
        self.status = 'completed'

    def cancel(self):
        """Cancela la cita"""
        self.status = 'cancelled'


@dataclass
class Treatment:
    """
    Entidad que representa un tratamiento médico
    """
    id: Optional[str]
    patient_id: PatientId
    diagnosis: str
    prescription: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str = 'active'  # 'active', 'completed', 'discontinued'

    def __post_init__(self):
        if self.id is None:
            self.id = f"trt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def complete(self):
        """Marca el tratamiento como completado"""
        self.status = 'completed'
        self.end_date = datetime.now()

    def discontinue(self):
        """Discontinúa el tratamiento"""
        self.status = 'discontinued'
        self.end_date = datetime.now()
