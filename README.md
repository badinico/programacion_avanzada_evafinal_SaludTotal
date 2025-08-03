# Sistema de Gestión de Pacientes - SaludTotal

Sistema de escritorio desarrollado en Python con Tkinter para la gestión integral de pacientes en la clínica médica SaludTotal. La aplicación permite realizar seguimiento de citas médicas, registrar información sobre tratamientos y medicamentos recetados, y generar informes sobre el estado de salud de los pacientes.

## Características Principales

### Gestión de Pacientes
- Registro de nuevos pacientes con información completa
- Búsqueda y filtrado de pacientes por diferentes criterios
- Actualización de historial médico y datos de contacto
- Visualización de lista completa de pacientes

### Gestión de Citas Médicas
- Programación de citas médicas con fecha, doctor y razón
- Seguimiento del estado de las citas (programada, completada, cancelada)
- Visualización de citas por paciente
- Gestión de citas próximas

### Gestión de Tratamientos
- Registro de tratamientos médicos con diagnóstico y prescripción
- Seguimiento del estado de tratamientos (activo, completado, discontinuado)
- Visualización de tratamientos por paciente
- Control de fechas de inicio y fin de tratamientos

### Reportes y Estadísticas
- Generación de reportes completos de pacientes
- Estadísticas por género y rango de edad
- Información sobre tratamientos activos y citas próximas
- Lista de pacientes recientes

## Arquitectura del Proyecto

El proyecto sigue la arquitectura **Domain-Driven Design (DDD)** con las siguientes capas:

```
programacion_avanzada_evafinal_SaludTotal/
├── domain/                    # Capa de dominio
│   ├── entities.py           # Entidades del dominio
│   ├── value_objects.py      # Objetos de valor
│   ├── services.py           # Servicios de dominio
│   └── dto.py               # Objetos de transferencia de datos
├── application/              # Capa de aplicación
│   └── use_cases.py         # Casos de uso
├── infrastructure/           # Capa de infraestructura
│   ├── mysql_repository.py  # Repositorios MySQL
│   └── gui_interface.py     # Interfaz gráfica
├── config.py                # Configuración de la aplicación
├── main.py                  # Punto de entrada
├── requirements.txt          # Dependencias
└── setup.py                 # Configuración del paquete
```

## Requisitos del Sistema

- Python 3.8 o superior
- MySQL 5.7 o superior
- Tkinter (incluido con Python)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd programacion_avanzada_evafinal_SaludTotal
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos MySQL

#### Opción A: Usando Docker (recomendado)
```bash
docker run --name mysql-saludtotal \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=saludtotal_db \
  -p 3306:3306 \
  -d mysql:8.0
```

#### Opción B: Instalación local
1. Instalar MySQL Server
2. Crear base de datos: `CREATE DATABASE saludtotal_db;`
3. Configurar usuario y permisos

### 5. Configurar la aplicación
Editar `config.py` según tu configuración de MySQL:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'saludtotal_db',
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### 6. Insertar datos de ejemplo (opcional)
```bash
python insert_sample_data.py
```

## Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Instalar como paquete
```bash
pip install -e .
saludtotal  # Comando directo
```

## Funcionalidades Detalladas

### Gestión de Pacientes

#### Registrar Nuevo Paciente
1. Ir a la pestaña "Pacientes"
2. Completar el formulario con:
   - Nombre completo
   - Edad (0-150 años)
   - Género (Masculino/Femenino/Otro)
   - Información de contacto
   - Historial médico (opcional)
3. Hacer clic en "Registrar Paciente"

#### Buscar Pacientes
- Usar el campo de búsqueda por nombre
- Hacer clic en "Buscar" para filtrar resultados
- Hacer clic en "Mostrar Todos" para ver todos los pacientes

#### Editar Paciente
1. Seleccionar un paciente de la lista
2. Hacer clic en "Editar Paciente"
3. Modificar historial médico o contacto
4. Guardar cambios

### Gestión de Citas

#### Programar Nueva Cita
1. Ir a la pestaña "Citas Médicas"
2. Seleccionar paciente del combo
3. Especificar fecha y hora
4. Ingresar nombre del doctor
5. Describir razón de la consulta
6. Agregar notas adicionales (opcional)
7. Hacer clic en "Programar Cita"

#### Gestionar Citas
- **Completar Cita**: Marcar como completada
- **Cancelar Cita**: Cancelar cita programada
- **Ver Citas por Paciente**: Desde la pestaña de pacientes

### Gestión de Tratamientos

#### Registrar Nuevo Tratamiento
1. Ir a la pestaña "Tratamientos"
2. Seleccionar paciente
3. Ingresar diagnóstico
4. Especificar prescripción médica
5. Hacer clic en "Registrar Tratamiento"

#### Gestionar Tratamientos
- **Completar Tratamiento**: Marcar como finalizado
- **Discontinuar Tratamiento**: Suspender tratamiento
- **Ver Tratamientos por Paciente**: Desde la pestaña de pacientes

### Reportes

#### Generar Reporte Completo
1. Ir a la pestaña "Reportes"
2. Hacer clic en "Generar Reporte Completo"
3. El reporte incluye:
   - Estadísticas generales
   - Distribución por género
   - Distribución por edad
   - Pacientes recientes
   - Tratamientos activos
   - Citas próximas

## Estructura de la Base de Datos

### Tabla Pacientes
```sql
CREATE TABLE Pacientes (
    ID VARCHAR(36) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Edad INT NOT NULL,
    Genero VARCHAR(10) NOT NULL,
    HistorialMedico TEXT,
    Contacto VARCHAR(100) NOT NULL,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME NOT NULL
);
```

### Tabla Citas
```sql
CREATE TABLE Citas (
    ID VARCHAR(50) PRIMARY KEY,
    PatientID VARCHAR(36) NOT NULL,
    Fecha DATETIME NOT NULL,
    Doctor VARCHAR(100) NOT NULL,
    Razon VARCHAR(200) NOT NULL,
    Estado VARCHAR(20) NOT NULL,
    Notas TEXT,
    FOREIGN KEY (PatientID) REFERENCES Pacientes(ID)
);
```

### Tabla Tratamientos
```sql
CREATE TABLE Tratamientos (
    ID VARCHAR(50) PRIMARY KEY,
    PatientID VARCHAR(36) NOT NULL,
    Diagnostico VARCHAR(200) NOT NULL,
    Prescripcion TEXT NOT NULL,
    FechaInicio DATETIME NOT NULL,
    FechaFin DATETIME,
    Estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Pacientes(ID)
);
```

## Validaciones y Reglas de Negocio

### Pacientes
- Nombre: Obligatorio, no puede estar vacío
- Edad: Entre 0 y 150 años
- Género: Debe ser uno de: Masculino, Femenino, Otro
- Contacto: Obligatorio, no puede estar vacío
- Historial médico: Opcional

### Citas
- Fecha: No puede ser en el pasado
- Doctor: Obligatorio
- Razón: Obligatoria
- Paciente: Debe existir en el sistema

### Tratamientos
- Diagnóstico: Obligatorio
- Prescripción: Obligatoria
- Paciente: Debe existir en el sistema
- Fecha de inicio: Automática (fecha actual)

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **MySQL**: Base de datos
- **mysql-connector-python**: Conector de base de datos
- **Domain-Driven Design**: Arquitectura del proyecto

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

SaludTotal Development Team - info@saludtotal.com

## Changelog

### v1.0.0
- Implementación inicial del sistema
- Gestión completa de pacientes
- Gestión de citas médicas
- Gestión de tratamientos
- Generación de reportes
- Interfaz gráfica intuitiva
- Arquitectura DDD
- Conexión a MySQL

