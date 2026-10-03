from pathlib import Path
import tkinter as tk
from tkinter import ttk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    def __init__(self) -> None:
        self.raiz = tk.Tk()
        self.raiz.title("Restaurante_app")
        self.raiz.geometry("900x560")
        self.raiz.minsize(720, 420)
        self.servicio = RestauranteServicio()
        datos = Path(__file__).resolve().parent / "datos"
        datos.mkdir(exist_ok=True)
        self.archivo_productos = ArchivoServicio(str(datos / "productos.json"))
        self.archivo_usuarios = ArchivoServicio(str(datos / "usuarios.json"))
        self.archivo_ventas = ArchivoServicio(str(datos / "ventas.json"))
        self.servicio.cargar_productos(self.archivo_productos.cargar_productos())
        self.servicio.cargar_usuarios(self.archivo_usuarios.cargar_usuarios())
        self.servicio.cargar_ventas(self.archivo_ventas.cargar_ventas())
        self._mostrar_login()

    def _mostrar_login(self) -> None:
        self._limpiar_ventana()
        vista = LoginView(self.raiz, self.servicio, self._mostrar_principal)
        vista.pack(fill="both", expand=True)

    def _mostrar_principal(self, usuario) -> None:
        self._limpiar_ventana()
        vista = MainView(self.raiz, self.servicio, self._guardar_datos, usuario)
        vista.pack(fill="both", expand=True)

    def _guardar_datos(self) -> None:
        self.archivo_productos.guardar_productos(self.servicio.listar_productos())
        self.archivo_usuarios.guardar_usuarios(self.servicio.listar_usuarios())
        self.archivo_ventas.guardar_ventas(self.servicio.listar_ventas())

    def _limpiar_ventana(self) -> None:
        for widget in self.raiz.winfo_children():
            widget.destroy()

    def ejecutar(self) -> None:
        self.raiz.mainloop()


if __name__ == "__main__":
    RestauranteApp().ejecutar()
