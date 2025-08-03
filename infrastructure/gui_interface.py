import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Optional
from datetime import datetime, timedelta
from domain.dto import PatientDTO, AppointmentDTO, TreatmentDTO, PatientSearchDTO, PatientReportDTO
from application.use_cases import PatientUseCase, AppointmentUseCase, TreatmentUseCase, ReportUseCase
from infrastructure.mysql_repository import MySQLPatientRepository, MySQLAppointmentRepository, MySQLTreatmentRepository
from config import APP_CONFIG


class SaludTotalGUI:
    """
    Interfaz gráfica principal para el sistema SaludTotal
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['window_size'])
        
        # Inicializar repositorios
        self.patient_repository = MySQLPatientRepository()
        self.appointment_repository = MySQLAppointmentRepository()
        self.treatment_repository = MySQLTreatmentRepository()
        
        # Inicializar casos de uso
        self.patient_use_case = PatientUseCase(self.patient_repository)
        self.appointment_use_case = AppointmentUseCase(self.appointment_repository, self.patient_repository)
        self.treatment_use_case = TreatmentUseCase(self.treatment_repository, self.patient_repository)
        self.report_use_case = ReportUseCase(self.patient_repository, self.appointment_repository, self.treatment_repository)
        
        self.setup_ui()
        self.load_patients()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de pacientes
        self.patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patients_frame, text="Pacientes")
        self.setup_patients_tab()
        
        # Pestaña de citas
        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text="Citas Médicas")
        self.setup_appointments_tab()
        
        # Pestaña de tratamientos
        self.treatments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.treatments_frame, text="Tratamientos")
        self.setup_treatments_tab()
        
        # Pestaña de reportes
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reportes")
        self.setup_reports_tab()

    def setup_patients_tab(self):
        """Configura la pestaña de pacientes"""
        # Frame principal
        main_frame = ttk.Frame(self.patients_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Paciente")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Edad:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.age_entry = ttk.Entry(form_frame, width=10)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Género:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, 
                                   values=['Masculino', 'Femenino', 'Otro'], state='readonly')
        gender_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contacto:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.contact_entry = ttk.Entry(form_frame, width=30)
        self.contact_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Historial Médico:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.history_text = tk.Text(form_frame, height=3, width=50)
        self.history_text.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Registrar Paciente", 
                  command=self.register_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Formulario", 
                  command=self.clear_patient_form).pack(side=tk.LEFT, padx=5)
        
        # Frame para búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Pacientes")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por nombre:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", 
                  command=self.search_patients).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Mostrar Todos", 
                  command=self.load_patients).pack(side=tk.LEFT, padx=5)
        
        # Tabla de pacientes
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Pacientes")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ('ID', 'Nombre', 'Edad', 'Género', 'Contacto', 'Historial Médico')
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Editar Paciente", 
                  command=self.edit_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Eliminar Paciente", 
                  command=self.delete_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Ver Citas", 
                  command=self.view_patient_appointments).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Ver Tratamientos", 
                  command=self.view_patient_treatments).pack(side=tk.LEFT, padx=5)

    def setup_appointments_tab(self):
        """Configura la pestaña de citas médicas"""
        main_frame = ttk.Frame(self.appointments_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para formulario de cita
        form_frame = ttk.LabelFrame(main_frame, text="Programar Nueva Cita")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Paciente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(form_frame, textvariable=self.patient_var, width=30)
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Fecha:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        ttk.Label(form_frame, text="Doctor:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.doctor_entry = ttk.Entry(form_frame, width=30)
        self.doctor_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Razón:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.reason_entry = ttk.Entry(form_frame, width=30)
        self.reason_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Notas:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.notes_text = tk.Text(form_frame, height=3, width=50)
        self.notes_text.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Programar Cita", 
                  command=self.schedule_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Formulario", 
                  command=self.clear_appointment_form).pack(side=tk.LEFT, padx=5)
        
        # Tabla de citas
        table_frame = ttk.LabelFrame(main_frame, text="Citas Programadas")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Paciente', 'Fecha', 'Doctor', 'Razón', 'Estado')
        self.appointments_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Completar Cita", 
                  command=self.complete_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cancelar Cita", 
                  command=self.cancel_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cargar Citas", 
                  command=self.load_appointments).pack(side=tk.LEFT, padx=5)

    def setup_treatments_tab(self):
        """Configura la pestaña de tratamientos"""
        main_frame = ttk.Frame(self.treatments_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para formulario de tratamiento
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Tratamiento")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Paciente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.treatment_patient_var = tk.StringVar()
        self.treatment_patient_combo = ttk.Combobox(form_frame, textvariable=self.treatment_patient_var, width=30)
        self.treatment_patient_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Diagnóstico:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.diagnosis_entry = ttk.Entry(form_frame, width=30)
        self.diagnosis_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Prescripción:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.prescription_text = tk.Text(form_frame, height=4, width=50)
        self.prescription_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Registrar Tratamiento", 
                  command=self.register_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Formulario", 
                  command=self.clear_treatment_form).pack(side=tk.LEFT, padx=5)
        
        # Tabla de tratamientos
        table_frame = ttk.LabelFrame(main_frame, text="Tratamientos Registrados")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Paciente', 'Diagnóstico', 'Prescripción', 'Fecha Inicio', 'Estado')
        self.treatments_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.treatments_tree.heading(col, text=col)
            self.treatments_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.treatments_tree.yview)
        self.treatments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.treatments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Completar Tratamiento", 
                  command=self.complete_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Discontinuar Tratamiento", 
                  command=self.discontinue_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cargar Tratamientos", 
                  command=self.load_treatments).pack(side=tk.LEFT, padx=5)

    def setup_reports_tab(self):
        """Configura la pestaña de reportes"""
        main_frame = ttk.Frame(self.reports_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón para generar reporte
        ttk.Button(main_frame, text="Generar Reporte Completo", 
                  command=self.generate_report).pack(pady=10)
        
        # Frame para mostrar reporte
        self.report_frame = ttk.LabelFrame(main_frame, text="Reporte de Pacientes")
        self.report_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget para mostrar el reporte
        self.report_text = tk.Text(self.report_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(self.report_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def register_patient(self):
        """Registra un nuevo paciente"""
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            contact = self.contact_entry.get().strip()
            history = self.history_text.get("1.0", tk.END).strip()
            
            if not all([name, age, gender, contact]):
                messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos")
                return
            
            patient_dto = self.patient_use_case.create_patient(name, age, gender, history, contact)
            messagebox.showinfo("Éxito", f"Paciente {patient_dto.name} registrado correctamente")
            self.clear_patient_form()
            self.load_patients()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar paciente: {str(e)}")

    def clear_patient_form(self):
        """Limpia el formulario de pacientes"""
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_var.set('')
        self.contact_entry.delete(0, tk.END)
        self.history_text.delete("1.0", tk.END)

    def load_patients(self):
        """Carga la lista de pacientes"""
        try:
            # Limpiar tabla
            for item in self.patients_tree.get_children():
                self.patients_tree.delete(item)
            
            # Cargar pacientes
            patients = self.patient_use_case.get_all_patients()
            for patient in patients:
                self.patients_tree.insert('', 'end', values=(
                    patient.id,
                    patient.name,
                    patient.age,
                    patient.gender,
                    patient.contact,
                    patient.medical_history[:50] + "..." if len(patient.medical_history) > 50 else patient.medical_history
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")

    def search_patients(self):
        """Busca pacientes según criterios"""
        try:
            search_term = self.search_entry.get().strip()
            if not search_term:
                self.load_patients()
                return
            
            search_dto = PatientSearchDTO(name=search_term)
            patients = self.patient_use_case.search_patients(search_dto)
            
            # Limpiar tabla
            for item in self.patients_tree.get_children():
                self.patients_tree.delete(item)
            
            # Mostrar resultados
            for patient in patients:
                self.patients_tree.insert('', 'end', values=(
                    patient.id,
                    patient.name,
                    patient.age,
                    patient.gender,
                    patient.contact,
                    patient.medical_history[:50] + "..." if len(patient.medical_history) > 50 else patient.medical_history
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar pacientes: {str(e)}")

    def edit_patient(self):
        """Edita un paciente seleccionado"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente para editar")
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient = self.patient_use_case.get_patient_by_id(patient_id)
        
        if patient:
            # Crear ventana de edición
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Editar Paciente: {patient.name}")
            edit_window.geometry("400x300")
            
            # Campos de edición
            ttk.Label(edit_window, text="Historial Médico:").pack(pady=5)
            history_text = tk.Text(edit_window, height=5, width=50)
            history_text.insert("1.0", patient.medical_history)
            history_text.pack(pady=5)
            
            ttk.Label(edit_window, text="Contacto:").pack(pady=5)
            contact_entry = ttk.Entry(edit_window, width=40)
            contact_entry.insert(0, patient.contact)
            contact_entry.pack(pady=5)
            
            def save_changes():
                try:
                    new_history = history_text.get("1.0", tk.END).strip()
                    new_contact = contact_entry.get().strip()
                    
                    if new_contact:
                        self.patient_use_case.update_patient_contact(patient_id, new_contact)
                    if new_history:
                        self.patient_use_case.update_patient_medical_history(patient_id, new_history)
                    
                    messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
                    edit_window.destroy()
                    self.load_patients()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar paciente: {str(e)}")
            
            ttk.Button(edit_window, text="Guardar Cambios", command=save_changes).pack(pady=10)

    def delete_patient(self):
        """Elimina un paciente seleccionado"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente para eliminar")
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient_name = self.patients_tree.item(selection[0])['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al paciente {patient_name}?"):
            try:
                self.patient_use_case.delete_patient(patient_id)
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar paciente: {str(e)}")

    def schedule_appointment(self):
        """Programa una nueva cita"""
        try:
            patient_id = self.patient_var.get().split(" - ")[0] if self.patient_var.get() else ""
            date_str = self.date_entry.get()
            doctor = self.doctor_entry.get().strip()
            reason = self.reason_entry.get().strip()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if not all([patient_id, date_str, doctor, reason]):
                messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos")
                return
            
            # Parsear fecha
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            
            appointment_dto = self.appointment_use_case.create_appointment(
                patient_id, appointment_date, doctor, reason, notes
            )
            
            messagebox.showinfo("Éxito", "Cita programada correctamente")
            self.clear_appointment_form()
            self.load_appointments()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al programar cita: {str(e)}")

    def clear_appointment_form(self):
        """Limpia el formulario de citas"""
        self.patient_var.set('')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.doctor_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)

    def load_appointments(self):
        """Carga la lista de citas"""
        try:
            # Limpiar tabla
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)
            
            # Cargar citas
            appointments = self.appointment_use_case.get_all_appointments()
            for appointment in appointments:
                # Obtener nombre del paciente
                patient = self.patient_use_case.get_patient_by_id(appointment.patient_id)
                patient_name = patient.name if patient else "Paciente no encontrado"
                
                self.appointments_tree.insert('', 'end', values=(
                    appointment.id,
                    patient_name,
                    appointment.date.strftime("%Y-%m-%d %H:%M"),
                    appointment.doctor_name,
                    appointment.reason,
                    appointment.status
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar citas: {str(e)}")

    def complete_appointment(self):
        """Marca una cita como completada"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cita para completar")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        
        try:
            self.appointment_use_case.complete_appointment(appointment_id)
            messagebox.showinfo("Éxito", "Cita marcada como completada")
            self.load_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Error al completar cita: {str(e)}")

    def cancel_appointment(self):
        """Cancela una cita"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cita para cancelar")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta cita?"):
            try:
                self.appointment_use_case.cancel_appointment(appointment_id)
                messagebox.showinfo("Éxito", "Cita cancelada correctamente")
                self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar cita: {str(e)}")

    def register_treatment(self):
        """Registra un nuevo tratamiento"""
        try:
            patient_id = self.treatment_patient_var.get().split(" - ")[0] if self.treatment_patient_var.get() else ""
            diagnosis = self.diagnosis_entry.get().strip()
            prescription = self.prescription_text.get("1.0", tk.END).strip()
            
            if not all([patient_id, diagnosis, prescription]):
                messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos")
                return
            
            treatment_dto = self.treatment_use_case.create_treatment(patient_id, diagnosis, prescription)
            messagebox.showinfo("Éxito", "Tratamiento registrado correctamente")
            self.clear_treatment_form()
            self.load_treatments()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar tratamiento: {str(e)}")

    def clear_treatment_form(self):
        """Limpia el formulario de tratamientos"""
        self.treatment_patient_var.set('')
        self.diagnosis_entry.delete(0, tk.END)
        self.prescription_text.delete("1.0", tk.END)

    def load_treatments(self):
        """Carga la lista de tratamientos"""
        try:
            # Limpiar tabla
            for item in self.treatments_tree.get_children():
                self.treatments_tree.delete(item)
            
            # Cargar tratamientos
            treatments = self.treatment_use_case.get_all_treatments()
            for treatment in treatments:
                # Obtener nombre del paciente
                patient = self.patient_use_case.get_patient_by_id(treatment.patient_id)
                patient_name = patient.name if patient else "Paciente no encontrado"
                
                self.treatments_tree.insert('', 'end', values=(
                    treatment.id,
                    patient_name,
                    treatment.diagnosis,
                    treatment.prescription[:50] + "..." if len(treatment.prescription) > 50 else treatment.prescription,
                    treatment.start_date.strftime("%Y-%m-%d"),
                    treatment.status
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tratamientos: {str(e)}")

    def complete_treatment(self):
        """Marca un tratamiento como completado"""
        selection = self.treatments_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un tratamiento para completar")
            return
        
        treatment_id = self.treatments_tree.item(selection[0])['values'][0]
        
        try:
            self.treatment_use_case.complete_treatment(treatment_id)
            messagebox.showinfo("Éxito", "Tratamiento marcado como completado")
            self.load_treatments()
        except Exception as e:
            messagebox.showerror("Error", f"Error al completar tratamiento: {str(e)}")

    def discontinue_treatment(self):
        """Discontinúa un tratamiento"""
        selection = self.treatments_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un tratamiento para discontinuar")
            return
        
        treatment_id = self.treatments_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de discontinuar este tratamiento?"):
            try:
                self.treatment_use_case.discontinue_treatment(treatment_id)
                messagebox.showinfo("Éxito", "Tratamiento discontinuado correctamente")
                self.load_treatments()
            except Exception as e:
                messagebox.showerror("Error", f"Error al discontinuar tratamiento: {str(e)}")

    def generate_report(self):
        """Genera un reporte completo"""
        try:
            report = self.report_use_case.generate_patient_report()
            
            # Limpiar reporte anterior
            self.report_text.delete("1.0", tk.END)
            
            # Generar contenido del reporte
            report_content = f"""
REPORTE COMPLETO - CLÍNICA SALUDTOTAL
Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M")}

ESTADÍSTICAS GENERALES:
- Total de pacientes: {report.total_patients}
- Tratamientos activos: {report.active_treatments}
- Citas próximas: {report.upcoming_appointments}

DISTRIBUCIÓN POR GÉNERO:
"""
            for gender, count in report.patients_by_gender.items():
                report_content += f"- {gender}: {count} pacientes\n"
            
            report_content += "\nDISTRIBUCIÓN POR EDAD:\n"
            for age_range, count in report.patients_by_age_range.items():
                report_content += f"- {age_range} años: {count} pacientes\n"
            
            report_content += f"\nPACIENTES RECIENTES (últimos 30 días):\n"
            for patient in report.recent_patients[:10]:  # Mostrar solo los primeros 10
                report_content += f"- {patient.name} ({patient.age} años, {patient.gender})\n"
            
            self.report_text.insert("1.0", report_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")

    def update_patient_combos(self):
        """Actualiza los combos de pacientes en todas las pestañas"""
        try:
            patients = self.patient_use_case.get_all_patients()
            patient_options = [f"{p.id} - {p.name}" for p in patients]
            
            # Actualizar combo en pestaña de citas
            self.patient_combo['values'] = patient_options
            
            # Actualizar combo en pestaña de tratamientos
            self.treatment_patient_combo['values'] = patient_options
            
        except Exception as e:
            print(f"Error al actualizar combos de pacientes: {str(e)}")

    def view_patient_appointments(self):
        """Muestra las citas de un paciente seleccionado"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente")
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient_name = self.patients_tree.item(selection[0])['values'][1]
        
        try:
            appointments = self.appointment_use_case.get_appointments_by_patient(patient_id)
            
            # Crear ventana para mostrar citas
            appointments_window = tk.Toplevel(self.root)
            appointments_window.title(f"Citas de {patient_name}")
            appointments_window.geometry("800x400")
            
            # Crear tabla
            columns = ('ID', 'Fecha', 'Doctor', 'Razón', 'Estado')
            tree = ttk.Treeview(appointments_window, columns=columns, show='headings')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            for appointment in appointments:
                tree.insert('', 'end', values=(
                    appointment.id,
                    appointment.date.strftime("%Y-%m-%d %H:%M"),
                    appointment.doctor_name,
                    appointment.reason,
                    appointment.status
                ))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar citas: {str(e)}")

    def view_patient_treatments(self):
        """Muestra los tratamientos de un paciente seleccionado"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente")
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient_name = self.patients_tree.item(selection[0])['values'][1]
        
        try:
            treatments = self.treatment_use_case.get_treatments_by_patient(patient_id)
            
            # Crear ventana para mostrar tratamientos
            treatments_window = tk.Toplevel(self.root)
            treatments_window.title(f"Tratamientos de {patient_name}")
            treatments_window.geometry("800x400")
            
            # Crear tabla
            columns = ('ID', 'Diagnóstico', 'Prescripción', 'Fecha Inicio', 'Estado')
            tree = ttk.Treeview(treatments_window, columns=columns, show='headings')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            for treatment in treatments:
                tree.insert('', 'end', values=(
                    treatment.id,
                    treatment.diagnosis,
                    treatment.prescription[:50] + "..." if len(treatment.prescription) > 50 else treatment.prescription,
                    treatment.start_date.strftime("%Y-%m-%d"),
                    treatment.status
                ))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tratamientos: {str(e)}")

    def run(self):
        """Ejecuta la aplicación"""
        # Cargar datos iniciales
        self.load_patients()
        self.load_appointments()
        self.load_treatments()
        self.update_patient_combos()
        
        # Ejecutar la aplicación
        self.root.mainloop()
