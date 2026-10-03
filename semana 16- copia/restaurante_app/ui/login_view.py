import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    def __init__(self, master: tk.Misc, servicio: RestauranteServicio, on_login) -> None:
        super().__init__(master, padding=32)
        self.servicio = servicio
        self.on_login = on_login
        self.nombre_usuario = tk.StringVar()
        self.contrasena = tk.StringVar()
        self._construir()

    def _construir(self) -> None:
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Login.TFrame", background="#183a35")
        estilo.configure("LoginLogo.TLabel", background="#183a35")
        estilo.configure("LoginTitle.TLabel", background="#183a35", foreground="#ffffff")
        estilo.configure("LoginText.TLabel", background="#183a35", foreground="#dce9e4")
        estilo.configure(
            "Login.TEntry",
            fieldbackground="#ffffff",
            foreground="#20332f",
            padding=8,
            insertcolor="#176b5b",
        )
        estilo.configure(
            "Login.TButton",
            background="#df7548",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8),
            borderwidth=0,
        )
        estilo.map(
            "Login.TButton",
            background=[("active", "#c95f35"), ("pressed", "#a94827")],
        )
        self.configure(style="Login.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        contenido = ttk.Frame(self, style="Login.TFrame", padding=32)
        contenido.grid(row=0, column=0, sticky="nsew")
        contenido.columnconfigure(0, weight=1)
        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo_restaurante.png"
        self.logo = tk.PhotoImage(file=str(ruta_logo))
        tk.Label(
            contenido,
            image=self.logo,
            background="#183a35",
            borderwidth=0,
        ).grid(row=0, column=0, pady=(10, 10))
        fila_titulo = 1
        ttk.Label(contenido, text="Restaurante", style="LoginTitle.TLabel", font=("Segoe UI", 22, "bold")).grid(
            row=fila_titulo, column=0, pady=(0, 6)
        )
        ttk.Label(contenido, text="Iniciar sesión", style="LoginText.TLabel", font=("Segoe UI", 12)).grid(
            row=fila_titulo + 1, column=0, pady=(0, 24)
        )
        ttk.Label(contenido, text="Nombre de usuario", style="LoginText.TLabel").grid(
            row=fila_titulo + 2, column=0, sticky="w"
        )
        campo_usuario = ttk.Entry(
            contenido, textvariable=self.nombre_usuario, width=32, style="Login.TEntry"
        )
        campo_usuario.grid(row=fila_titulo + 3, column=0, pady=(6, 12), sticky="ew")
        ttk.Label(contenido, text="Contraseña", style="LoginText.TLabel").grid(
            row=fila_titulo + 4, column=0, sticky="w"
        )
        campo_contrasena = ttk.Entry(
            contenido,
            textvariable=self.contrasena,
            show="*",
            width=32,
            style="Login.TEntry",
        )
        campo_contrasena.grid(row=fila_titulo + 5, column=0, pady=(6, 18), sticky="ew")
        ttk.Button(
            contenido,
            text="Ingresar",
            command=self._ingresar,
            style="Login.TButton",
        ).grid(
            row=fila_titulo + 6, column=0, sticky="ew"
        )
        campo_usuario.focus_set()
        campo_usuario.bind("<Return>", lambda _evento: campo_contrasena.focus_set())
        campo_contrasena.bind("<Return>", lambda _evento: self._ingresar())

    def _ingresar(self) -> None:
        usuario = self.servicio.autenticar_usuario(
            self.nombre_usuario.get(), self.contrasena.get()
        )
        if usuario is None:
            messagebox.showerror(
                "Acceso denegado", "El nombre de usuario o la contraseña son incorrectos."
            )
            return
        self.on_login(usuario)

