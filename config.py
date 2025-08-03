# Configuración de la base de datos MySQL para la clínica SaludTotal
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'video_games_db',
    'user': 'root',
    'password': '123456',  # Contraseña del contenedor Docker
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Configuración de la aplicación SaludTotal
APP_CONFIG = {
    'title': 'SaludTotal - Sistema de Gestión de Pacientes',
    'version': '1.0.0',
    'window_size': '1200x800',
    'theme': 'default'
}

# Configuración de validación
VALIDATION_CONFIG = {
    'min_age': 0,
    'max_age': 150,
    'required_fields': ['name', 'age', 'gender', 'contact']
} 