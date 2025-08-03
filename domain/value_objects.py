import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class PatientId:
    """
    Value object para el identificador único del paciente
    """
    value: str

    @classmethod
    def generate(cls) -> 'PatientId':
        """Genera un nuevo ID único para el paciente"""
        return cls(str(uuid.uuid4()))

    @classmethod
    def from_string(cls, value: str) -> 'PatientId':
        """Crea un PatientId desde un string"""
        return cls(value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Age:
    """
    Value object para la edad del paciente
    """
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("La edad debe ser un número entero")
        if self.value < 0 or self.value > 150:
            raise ValueError("La edad debe estar entre 0 y 150 años")

    def is_valid(self) -> bool:
        """Valida que la edad esté en el rango permitido"""
        return 0 <= self.value <= 150

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Gender:
    """
    Value object para el género del paciente
    """
    value: str

    VALID_GENDERS = ['Masculino', 'Femenino', 'Otro']

    def __post_init__(self):
        if self.value not in self.VALID_GENDERS:
            raise ValueError(f"El género debe ser uno de: {', '.join(self.VALID_GENDERS)}")

    def is_valid(self) -> bool:
        """Valida que el género sea válido"""
        return self.value in self.VALID_GENDERS

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Contact:
    """
    Value object para la información de contacto del paciente
    """
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("La información de contacto no puede estar vacía")

    def is_valid(self) -> bool:
        """Valida que el contacto no esté vacío"""
        return bool(self.value and self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MedicalHistory:
    """
    Value object para el historial médico del paciente
    """
    value: str

    def __post_init__(self):
        if self.value is None:
            self.value = ""

    def is_valid(self) -> bool:
        """Valida el historial médico (puede estar vacío)"""
        return True

    def __str__(self) -> str:
        return self.value or "Sin historial médico"


@dataclass(frozen=True)
class Diagnosis:
    """
    Value object para el diagnóstico médico
    """
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("El diagnóstico no puede estar vacío")

    def is_valid(self) -> bool:
        """Valida que el diagnóstico no esté vacío"""
        return bool(self.value and self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Prescription:
    """
    Value object para la prescripción médica
    """
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("La prescripción no puede estar vacía")

    def is_valid(self) -> bool:
        """Valida que la prescripción no esté vacía"""
        return bool(self.value and self.value.strip())

    def __str__(self) -> str:
        return self.value
