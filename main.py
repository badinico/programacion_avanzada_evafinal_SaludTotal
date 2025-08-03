import sys
import tkinter as tk
from tkinter import messagebox
from infrastructure.gui_interface import SaludTotalGUI
from config import APP_CONFIG


def main():
    """
    Función principal que inicia la aplicación
    """
    try:
        print("Iniciando aplicación SaludTotal...")
        print(f"Versión: {APP_CONFIG['version']}")
        print(f"Título: {APP_CONFIG['title']}")
        
        # Crear y ejecutar la interfaz gráfica
        app = SaludTotalGUI()
        app.run()
        
    except Exception as e:
        # Mostrar error en caso de problemas
        error_message = f"Error al iniciar la aplicación: {str(e)}"
        print(error_message)
        
        # Intentar mostrar error en GUI si es posible
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showerror("Error de Inicio", error_message)
            root.destroy()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
