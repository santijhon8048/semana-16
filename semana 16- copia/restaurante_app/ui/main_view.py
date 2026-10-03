import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        guardar_datos,
        usuario_actual,
    ) -> None:
        super().__init__(master, padding=18)
        self.servicio = servicio
        self.guardar_datos = guardar_datos
        self.usuario_actual = usuario_actual
        self.venta_usuario = tk.StringVar()
        self.venta_producto = tk.StringVar()
        self.venta_cantidad = tk.StringVar(value="1")
        self.venta_total = tk.StringVar(value="Total estimado: $0.00")
        self.venta_estado = tk.StringVar(value="Seleccione usuario, producto y cantidad.")
        self._usuarios_venta: dict[str, str] = {}
        self._productos_venta: dict[str, str] = {}
        self.iconos: dict[str, tk.PhotoImage] = {}
        self._cargar_iconos()
        self._construir()
        self._actualizar_tablas()

    def _cargar_iconos(self) -> None:
        ruta_assets = Path(__file__).resolve().parent.parent / "assets"
        for nombre in ("logo_panel", "usuario", "producto", "venta"):
            try:
                imagen = tk.PhotoImage(file=str(ruta_assets / f"{nombre}.png"))
                self.iconos[nombre] = imagen
            except tk.TclError:
                continue

    def _construir(self) -> None:
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        fondo = "#f3f6f2"
        texto = "#20332f"
        estilo.configure("App.TFrame", background=fondo)
        estilo.configure("Titulo.TLabel", background=fondo, foreground="#183a35")
        estilo.configure(
            "Estado.TLabel",
            background="#e2eee8",
            foreground="#245746",
            padding=(10, 8),
        )
        estilo.configure("TNotebook", background=fondo, borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            background="#dce5df",
            foreground="#38514a",
            padding=(16, 8),
            font=("Segoe UI", 10, "bold"),
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#176b5b")],
            foreground=[("selected", "#ffffff")],
        )
        estilo.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10),
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=texto,
        )
        estilo.configure(
            "Treeview.Heading",
            background="#315e52",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(8, 7),
        )
        estilo.map(
            "Treeview",
            background=[("selected", "#b9d8c9")],
            foreground=[("selected", "#183a35")],
        )
        for nombre, color, activo in (
            ("Registrar", "#176b5b", "#105447"),
            ("Consultar", "#3d6380", "#304f66"),
            ("Actualizar", "#a86724", "#87521b"),
            ("Limpiar", "#64756e", "#4f5e58"),
            ("Eliminar", "#b74c43", "#963b34"),
        ):
            estilo.configure(
                f"{nombre}.TButton",
                background=color,
                foreground="#ffffff",
                padding=(10, 7),
                borderwidth=0,
            )
            estilo.map(
                f"{nombre}.TButton",
                background=[("active", activo), ("pressed", activo)],
                foreground=[("disabled", "#e5e9e6")],
            )
        self.configure(style="App.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        encabezado = ttk.Frame(self, style="App.TFrame")
        encabezado.grid(row=0, column=0, sticky="w", pady=(0, 12))
        if "logo_panel" in self.iconos:
            ttk.Label(encabezado, image=self.iconos["logo_panel"]).pack(
                side="left", padx=(0, 10)
            )
        ttk.Label(
            encabezado,
            text="Panel principal",
            style="Titulo.TLabel",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")
        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=1, column=0, sticky="nsew")
        self.productos_tab = ttk.Frame(self.tabs, padding=12)
        self.ventas_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.productos_tab, text="Productos")
        self.tabs.add(self.ventas_tab, text="Ventas")
        self._construir_productos()
        if self.usuario_actual.rol == self.usuario_actual.ROL_ADMINISTRADOR:
            self.usuarios_tab = ttk.Frame(self.tabs, padding=12)
            self.tabs.insert(1, self.usuarios_tab, text="Usuarios")
            self._construir_usuarios()
        self._construir_ventas()

    def _construir_ventas(self) -> None:
        tab = self.ventas_tab
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        formulario = ttk.LabelFrame(tab, text="Registrar venta", padding=12)
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        etiqueta_usuario = ttk.Label(formulario, text="Usuario")
        if "usuario" in self.iconos:
            etiqueta_usuario.configure(image=self.iconos["usuario"], compound="left")
        etiqueta_usuario.grid(row=0, column=0, sticky="w", padx=(0, 12))

        etiqueta_producto = ttk.Label(formulario, text="Producto")
        if "producto" in self.iconos:
            etiqueta_producto.configure(image=self.iconos["producto"], compound="left")
        etiqueta_producto.grid(row=0, column=1, sticky="w")

        self.venta_usuario_combo = ttk.Combobox(
            formulario, textvariable=self.venta_usuario, state="readonly"
        )
        self.venta_usuario_combo.grid(
            row=1, column=0, sticky="ew", padx=(0, 12), pady=(4, 10)
        )
        self.venta_producto_combo = ttk.Combobox(
            formulario, textvariable=self.venta_producto, state="readonly"
        )
        self.venta_producto_combo.grid(
            row=1, column=1, sticky="ew", pady=(4, 10)
        )

        ttk.Label(formulario, text="Cantidad").grid(row=2, column=0, sticky="w")
        ttk.Label(formulario, textvariable=self.venta_total).grid(
            row=2, column=1, sticky="e"
        )
        self.venta_cantidad_spin = ttk.Spinbox(
            formulario,
            from_=1,
            to=9999,
            textvariable=self.venta_cantidad,
            width=10,
            command=self._actualizar_total_estimado,
        )
        self.venta_cantidad_spin.grid(row=3, column=0, sticky="w", pady=(4, 10))
        self.venta_cantidad_spin.bind(
            "<KeyRelease>", lambda _evento: self._actualizar_total_estimado()
        )
        self.venta_usuario_combo.bind(
            "<<ComboboxSelected>>", lambda _evento: self._actualizar_total_estimado()
        )
        self.venta_producto_combo.bind(
            "<<ComboboxSelected>>", lambda _evento: self._actualizar_total_estimado()
        )

        icono_venta = self.iconos.get("venta")
        ttk.Button(
            formulario,
            text="Registrar venta",
            image=icono_venta,
            compound="left" if icono_venta else "none",
            command=self._registrar_venta,
            style="Registrar.TButton",
        ).grid(row=3, column=1, sticky="e", pady=(4, 10))

        self.ventas_tree = ttk.Treeview(
            tab,
            columns=("codigo", "fecha", "usuario", "producto", "cantidad", "unitario", "total"),
            show="headings",
        )
        encabezados = {
            "codigo": "Venta",
            "fecha": "Fecha",
            "usuario": "Usuario",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "unitario": "P. unitario",
            "total": "Total",
        }
        for columna, titulo in encabezados.items():
            self.ventas_tree.heading(columna, text=titulo)
        self.ventas_tree.column("codigo", width=90, anchor="center")
        self.ventas_tree.column("fecha", width=145, anchor="center")
        self.ventas_tree.column("usuario", width=110)
        self.ventas_tree.column("producto", width=190)
        self.ventas_tree.column("cantidad", width=75, anchor="center")
        self.ventas_tree.column("unitario", width=100, anchor="e")
        self.ventas_tree.column("total", width=100, anchor="e")
        barra = ttk.Scrollbar(tab, orient="vertical", command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=barra.set)
        self.ventas_tree.grid(row=1, column=0, sticky="nsew")
        barra.grid(row=1, column=1, sticky="ns")
        ttk.Label(tab, textvariable=self.venta_estado, style="Estado.TLabel").grid(
            row=2, column=0, sticky="ew", pady=(8, 0)
        )

    def _construir_productos(self) -> None:
        tab = self.productos_tab
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        formulario = ttk.LabelFrame(tab, text="Datos del producto", padding=10)
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)
        formulario.columnconfigure(5, weight=1)
        campos = ["Código", "Nombre", "Categoría", "Precio", "Stock"]
        self.producto_vars = {campo: tk.StringVar() for campo in campos}
        for columna, campo in enumerate(campos):
            posicion = columna * 2
            ttk.Label(formulario, text=campo).grid(
                row=0, column=posicion, padx=(4, 6), sticky="w"
            )
            ttk.Entry(formulario, textvariable=self.producto_vars[campo], width=16).grid(
                row=1, column=posicion, columnspan=2, padx=(4, 10), pady=(4, 0), sticky="ew"
            )
        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=10, pady=(12, 0), sticky="w")
        ttk.Button(
            acciones,
            text="Registrar",
            command=self._agregar_producto,
            style="Registrar.TButton",
        ).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(
            acciones,
            text="Cargar / consultar",
            command=self._cargar_producto,
            style="Consultar.TButton",
        ).pack(
            side="left", padx=6
        )
        ttk.Button(
            acciones,
            text="Actualizar",
            command=self._actualizar_producto,
            style="Actualizar.TButton",
        ).pack(
            side="left", padx=6
        )
        ttk.Button(
            acciones,
            text="Limpiar",
            command=self._limpiar_producto,
            style="Limpiar.TButton",
        ).pack(
            side="left", padx=6
        )
        self.producto_estado = tk.StringVar(value="Seleccione una acción para comenzar.")
        ttk.Label(tab, textvariable=self.producto_estado, style="Estado.TLabel").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.productos_tree = ttk.Treeview(
            tab, columns=("codigo", "nombre", "categoria", "precio", "stock"), show="headings"
        )
        for columna, titulo in zip(self.productos_tree["columns"], campos):
            self.productos_tree.heading(columna, text=titulo)
        self.productos_tree.column("codigo", width=100, anchor="center")
        self.productos_tree.column("nombre", width=180)
        self.productos_tree.column("categoria", width=140)
        self.productos_tree.column("precio", width=90, anchor="e")
        self.productos_tree.column("stock", width=80, anchor="center")
        barra = ttk.Scrollbar(tab, orient="vertical", command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=barra.set)
        self.productos_tree.grid(row=1, column=0, sticky="nsew")
        barra.grid(row=1, column=1, sticky="ns")
        ttk.Button(
            tab,
            text="Eliminar seleccionado",
            command=self._eliminar_producto,
            style="Eliminar.TButton",
        ).grid(
            row=3, column=0, sticky="e", pady=(10, 0)
        )

    def _construir_usuarios(self) -> None:
        tab = self.usuarios_tab
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        formulario = ttk.LabelFrame(tab, text="Datos del usuario", padding=10)
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)
        campos = ["Identificación", "Nombre", "Correo", "Nombre de usuario", "Contraseña"]
        self.usuario_vars = {campo: tk.StringVar() for campo in campos}
        for indice, campo in enumerate(campos):
            fila, columna = divmod(indice, 2)
            columna *= 2
            ttk.Label(formulario, text=campo).grid(
                row=fila * 2, column=columna, sticky="w", padx=(4, 8)
            )
            entrada = ttk.Entry(
                formulario,
                textvariable=self.usuario_vars[campo],
                show="*" if campo == "Contraseña" else "",
            )
            entrada.grid(
                row=fila * 2 + 1,
                column=columna,
                columnspan=2,
                sticky="ew",
                padx=(4, 12),
                pady=(4, 8),
            )
            entrada.bind("<Return>", self._atajo_registrar_usuario)
            entrada.bind("<Escape>", self._atajo_limpiar_usuario)
            if campo == "Identificación":
                self.usuario_identificacion_entry = entrada

        ttk.Label(formulario, text="Rol").grid(
            row=4, column=2, sticky="w", padx=(4, 8)
        )
        self.usuario_rol = tk.StringVar(value=Usuario.ROL_CLIENTE)
        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.usuario_rol,
            values=Usuario.ROLES,
            state="readonly",
        )
        self.usuario_rol_combo.grid(
            row=5, column=2, columnspan=2, sticky="ew", padx=(4, 12), pady=(4, 8)
        )
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self._rol_usuario_seleccionado)
        self.usuario_rol_combo.bind("<Return>", self._atajo_registrar_usuario)
        self.usuario_rol_combo.bind("<Escape>", self._atajo_limpiar_usuario)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=6, column=0, columnspan=4, sticky="w", pady=(4, 0))
        self._usuario_botones = {}
        for texto, metodo, estilo in (
            ("Registrar", self._registrar_usuario, "Registrar.TButton"),
            ("Actualizar", self._actualizar_usuario, "Actualizar.TButton"),
            ("Eliminar", self._eliminar_usuario, "Eliminar.TButton"),
            ("Limpiar", self._limpiar_usuario, "Limpiar.TButton"),
        ):
            boton = ttk.Button(acciones, text=texto, command=metodo, style=estilo)
            boton.pack(side="left", padx=(0, 6))
            self._usuario_botones[texto] = boton

        self.usuario_estado = tk.StringVar(value="Formulario listo para gestionar usuarios.")
        ttk.Label(tab, textvariable=self.usuario_estado, style="Estado.TLabel").grid(
            row=2, column=0, sticky="ew", pady=(8, 0)
        )
        columnas = ("identificacion", "nombre", "nombre_usuario", "rol")
        self.usuarios_tree = ttk.Treeview(
            tab,
            columns=columnas,
            show="headings",
        )
        encabezados = {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "nombre_usuario": "Nombre de usuario",
            "rol": "Rol",
        }
        for columna, titulo in encabezados.items():
            self.usuarios_tree.heading(columna, text=titulo)
        self.usuarios_tree.column("identificacion", width=120, anchor="center")
        self.usuarios_tree.column("nombre", width=180)
        self.usuarios_tree.column("nombre_usuario", width=170)
        self.usuarios_tree.column("rol", width=120, anchor="center")
        self.usuarios_tree.bind("<<TreeviewSelect>>", self._seleccionar_usuario)
        self.usuarios_tree.bind("<Return>", self._atajo_registrar_usuario)
        self.usuarios_tree.bind("<Escape>", self._atajo_limpiar_usuario)
        barra = ttk.Scrollbar(tab, orient="vertical", command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=barra.set)
        self.usuarios_tree.grid(row=1, column=0, sticky="nsew")
        barra.grid(row=1, column=1, sticky="ns")
        self._actualizar_usuarios_tree()

    def _usuario_desde_formulario(self) -> Usuario:
        return Usuario(
            identificacion=self.usuario_vars["Identificación"].get(),
            nombre=self.usuario_vars["Nombre"].get(),
            correo=self.usuario_vars["Correo"].get(),
            nombre_usuario=self.usuario_vars["Nombre de usuario"].get(),
            contrasena=self.usuario_vars["Contraseña"].get(),
            rol=self.usuario_rol.get(),
        )

    def _seleccionar_usuario(self, _evento=None) -> None:
        seleccion = self.usuarios_tree.selection()
        if not seleccion:
            return
        identificacion = self.usuarios_tree.item(seleccion[0], "values")[0]
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            return
        self._usuario_seleccionado = usuario.identificacion
        self.usuario_identificacion_entry.state(["readonly"])
        self.usuario_vars["Identificación"].set(usuario.identificacion)
        self.usuario_vars["Nombre"].set(usuario.nombre)
        self.usuario_vars["Correo"].set(usuario.correo)
        self.usuario_vars["Nombre de usuario"].set(usuario.nombre_usuario)
        self.usuario_vars["Contraseña"].set("")
        self.usuario_rol.set(usuario.rol)
        self.usuario_estado.set(
            f"Usuario {usuario.identificacion} cargado para actualización."
        )

    def _rol_usuario_seleccionado(self, _evento=None) -> None:
        self.usuario_estado.set(f"Rol seleccionado: {self.usuario_rol.get()}.")

    def _atajo_registrar_usuario(self, _evento=None) -> str:
        self._registrar_usuario()
        return "break"

    def _atajo_limpiar_usuario(self, _evento=None) -> str:
        self._limpiar_usuario()
        return "break"

    def _registrar_usuario(self) -> None:
        try:
            usuario = self._usuario_desde_formulario()
            if not self.servicio.registrar_usuario(usuario, self.usuario_actual):
                raise ValueError(
                    "La identificación o el nombre de usuario ya están registrados."
                )
            self.guardar_datos()
            self._actualizar_usuarios_tree()
            self._limpiar_usuario()
            self.usuario_estado.set(f"Usuario {usuario.identificacion} registrado.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Usuario inválido", str(error))

    def _actualizar_usuario(self) -> None:
        identificacion = getattr(self, "_usuario_seleccionado", "")
        try:
            if not identificacion:
                raise ValueError("Seleccione un usuario para actualizar.")
            if not self.servicio.actualizar_usuario(
                identificacion=identificacion,
                nombre=self.usuario_vars["Nombre"].get(),
                correo=self.usuario_vars["Correo"].get(),
                nombre_usuario=self.usuario_vars["Nombre de usuario"].get(),
                contrasena=self.usuario_vars["Contraseña"].get(),
                rol=self.usuario_rol.get(),
                administrador=self.usuario_actual,
            ):
                raise ValueError(
                    "No se pudo actualizar: revise el usuario y que el nombre de usuario no esté duplicado."
                )
            self.guardar_datos()
            self._actualizar_usuarios_tree()
            self._limpiar_usuario()
            self.usuario_estado.set(f"Usuario {identificacion} actualizado.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Usuario inválido", str(error))

    def _eliminar_usuario(self) -> None:
        identificacion = getattr(self, "_usuario_seleccionado", "")
        if not identificacion:
            messagebox.showerror("Usuario no seleccionado", "Seleccione un usuario.")
            return
        if not messagebox.askyesno(
            "Eliminar usuario", f"¿Desea eliminar al usuario {identificacion}?"
        ):
            return
        if not self.servicio.eliminar_usuario(identificacion, self.usuario_actual):
            messagebox.showerror("No se pudo eliminar", "El usuario ya no está disponible.")
            return
        self.guardar_datos()
        self._actualizar_usuarios_tree()
        self._limpiar_usuario()
        self.usuario_estado.set(f"Usuario {identificacion} eliminado.")

    def _limpiar_usuario(self) -> None:
        self._limpiar(self.usuario_vars)
        self.usuario_identificacion_entry.state(["!readonly"])
        self.usuario_rol.set(Usuario.ROL_CLIENTE)
        self._usuario_seleccionado = ""
        seleccion = self.usuarios_tree.selection()
        if seleccion:
            self.usuarios_tree.selection_remove(*seleccion)
        self.usuario_estado.set("Formulario listo para gestionar usuarios.")

    def _actualizar_usuarios_tree(self) -> None:
        if not hasattr(self, "usuarios_tree"):
            return
        self.usuarios_tree.delete(*self.usuarios_tree.get_children())
        for usuario in self.servicio.listar_usuarios():
            if usuario.rol == Usuario.ROL_ADMINISTRADOR:
                continue
            self.usuarios_tree.insert(
                "",
                "end",
                iid=usuario.identificacion,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.nombre_usuario,
                    usuario.rol,
                ),
            )

    def _agregar_producto(self) -> None:
        try:
            producto = self._producto_desde_formulario()
            if not self.servicio.registrar_producto(producto):
                raise ValueError("El código ya está registrado.")
            self.guardar_datos()
            self._limpiar_producto()
            self._actualizar_tablas()
            self.producto_estado.set(f"Producto {producto.codigo} registrado correctamente.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Producto inválido", str(error))

    def _cargar_producto(self) -> None:
        producto = self.servicio.buscar_producto(self.producto_vars["Código"].get())
        if producto is None:
            messagebox.showerror("Producto no encontrado", "No existe un producto con ese código.")
            return
        self._mostrar_producto(producto)
        self.producto_estado.set(f"Producto {producto.codigo} cargado para consulta o actualización.")

    def _actualizar_producto(self) -> None:
        try:
            codigo = self.producto_vars["Código"].get()
            producto = self._producto_desde_formulario()
            if not self.servicio.actualizar_producto(
                codigo,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.stock,
            ):
                raise ValueError("No existe un producto con ese código.")
            self.guardar_datos()
            self._actualizar_tablas()
            self.producto_estado.set(f"Producto {codigo.strip()} actualizado correctamente.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Producto inválido", str(error))

    def _producto_desde_formulario(self) -> Producto:
        return Producto(
            self.producto_vars["Código"].get(),
            self.producto_vars["Nombre"].get(),
            self.producto_vars["Categoría"].get(),
            float(self.producto_vars["Precio"].get()),
            int(self.producto_vars["Stock"].get()),
        )

    def _mostrar_producto(self, producto: Producto) -> None:
        valores = {
            "Código": producto.codigo,
            "Nombre": producto.nombre,
            "Categoría": producto.categoria,
            "Precio": str(producto.precio),
            "Stock": str(producto.stock),
        }
        for campo, valor in valores.items():
            self.producto_vars[campo].set(valor)

    def _limpiar_producto(self) -> None:
        self._limpiar(self.producto_vars)
        self.producto_estado.set("Formulario listo para un nuevo producto.")

    def _eliminar_producto(self) -> None:
        seleccion = self.productos_tree.selection()
        if not seleccion:
            return
        codigo = self.productos_tree.item(seleccion[0], "values")[0]
        if self.servicio.eliminar_producto(codigo):
            self.guardar_datos()
            self._actualizar_tablas()
            self._limpiar_producto()
            self.producto_estado.set(f"Producto {codigo} eliminado correctamente.")

    def _actualizar_total_estimado(self) -> None:
        codigo = self._productos_venta.get(self.venta_producto.get())
        producto = self.servicio.buscar_producto(codigo or "")
        try:
            cantidad = int(self.venta_cantidad.get())
        except ValueError:
            cantidad = 0
        total = producto.precio * cantidad if producto is not None and cantidad > 0 else 0
        self.venta_total.set(f"Total estimado: ${total:.2f}")

    def _registrar_venta(self) -> None:
        usuario_identificacion = self._usuarios_venta.get(self.venta_usuario.get(), "")
        producto_codigo = self._productos_venta.get(self.venta_producto.get(), "")
        try:
            cantidad = int(self.venta_cantidad.get())
            venta = self.servicio.registrar_venta(
                usuario_identificacion,
                producto_codigo,
                cantidad,
            )
            self.guardar_datos()
            self._actualizar_tablas()
            self.venta_cantidad.set("1")
            self.venta_estado.set(
                f"Venta {venta.codigo} registrada. Total: ${venta.total:.2f}."
            )
            self._actualizar_total_estimado()
        except (ValueError, TypeError) as error:
            messagebox.showerror("No se pudo registrar la venta", str(error))

    def _actualizar_tablas(self) -> None:
        for tabla in (
            getattr(self, "productos_tree", None),
            getattr(self, "ventas_tree", None),
        ):
            if tabla is not None:
                tabla.delete(*tabla.get_children())
        for producto in self.servicio.listar_productos():
            self.productos_tree.insert("", "end", values=(producto.codigo, producto.nombre, producto.categoria, f"{producto.precio:.2f}", producto.stock))
        self._actualizar_usuarios_tree()
        if hasattr(self, "ventas_tree"):
            for venta in self.servicio.listar_ventas():
                self.ventas_tree.insert(
                    "",
                    "end",
                    values=(
                        venta.codigo,
                        venta.fecha,
                        venta.nombre_usuario,
                        venta.producto_nombre,
                        venta.cantidad,
                        f"${venta.precio_unitario:.2f}",
                        f"${venta.total:.2f}",
                    ),
                )
        if hasattr(self, "venta_usuario_combo"):
            self._usuarios_venta = {
                f"{usuario.nombre} - {usuario.identificacion}": usuario.identificacion
                for usuario in self.servicio.listar_usuarios()
            }
            self._productos_venta = {
                f"{producto.nombre} - {producto.codigo} | ${producto.precio:.2f} | stock {producto.stock}": producto.codigo
                for producto in self.servicio.listar_productos()
            }
            self.venta_usuario_combo["values"] = tuple(self._usuarios_venta)
            self.venta_producto_combo["values"] = tuple(self._productos_venta)
            self._actualizar_total_estimado()

    @staticmethod
    def _limpiar(variables: dict[str, tk.StringVar]) -> None:
        for variable in variables.values():
            variable.set("")
