import tkinter as tk
from tkinter import ttk, messagebox


class VistaGestionarSolicitudes:
    def __init__(self, root, controlador_solicitud):
        self.root = tk.Toplevel(root)
        self.root.title("Gestionar Solicitudes")
        self.controlador_solicitud = controlador_solicitud

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Producto", "Cantidad", "Solicitante", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.btn_aprobar = tk.Button(self.frame, text="Aprobar", command=self.aprobar_solicitud)
        self.btn_aprobar.pack(side="left", padx=5, pady=10)

        self.btn_rechazar = tk.Button(self.frame, text="Rechazar", command=self.rechazar_solicitud)
        self.btn_rechazar.pack(side="left", padx=5, pady=10)

        self.cargar_solicitudes()

    def cargar_solicitudes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        solicitudes = self.controlador_solicitud.listar_solicitudes()
        for solicitud in solicitudes:
            if solicitud.get_estado() == "pendiente":
                self.tree.insert("", "end", values=(
                    solicitud.get_id(),
                    solicitud.get_producto().get_codigo(),
                    solicitud.get_cantidad(),
                    solicitud.get_empleado(),
                    solicitud.get_estado()
                ))

    def aprobar_solicitud(self):
        self.actualizar_estado("aprobada")

    def rechazar_solicitud(self):
        self.actualizar_estado("rechazada")

    def actualizar_estado(self, nuevo_estado):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una solicitud.")
            return

        item = self.tree.item(selected[0])
        id_solicitud = item["values"][0]

        solicitud = next((s for s in self.controlador_solicitud.listar_solicitudes() if s.get_id() == id_solicitud), None)
        if solicitud is None:
            messagebox.showerror("Error", "Solicitud no encontrada.")
            return

        if nuevo_estado == "rechazada":
           
            self.controlador_solicitud.eliminar_solicitud(id_solicitud)
            messagebox.showinfo("Solicitud rechazada", "La solicitud ha sido eliminada.")
        else:
            solicitud.set_estado(nuevo_estado)
            messagebox.showinfo("Éxito", f"Solicitud marcada como {nuevo_estado}.")

        self.cargar_solicitudes()
