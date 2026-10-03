class Usuario:
    ROL_ADMINISTRADOR = "Administrador"
    ROL_EMPLEADO = "Empleado"
    ROL_CLIENTE = "Cliente"
    ROLES = (ROL_ADMINISTRADOR, ROL_EMPLEADO, ROL_CLIENTE)

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        nombre_usuario: str,
        contrasena: str,
        rol: str = ROL_CLIENTE,
    ) -> None:

        if not identificacion.strip():
            raise ValueError(
                "La identificación no puede estar vacía."
            )

        if not nombre.strip():
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if not correo.strip():
            raise ValueError(
                "El correo no puede estar vacío."
            )

        if not nombre_usuario.strip():
            raise ValueError(
                "El nombre de usuario no puede estar vacío."
            )

        if not contrasena.strip():
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        if rol not in self.ROLES:
            raise ValueError("Seleccione un rol válido.")

        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.nombre_usuario = nombre_usuario.strip()
        self.contrasena = contrasena
        self.rol = rol

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "nombre_usuario": self.nombre_usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            nombre_usuario=str(datos["nombre_usuario"]),
            contrasena=str(datos["contrasena"]),
            rol=str(datos.get("rol", cls.ROL_CLIENTE)),
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Usuario: {self.nombre_usuario} | "
            f"Rol: {self.rol}"
        )