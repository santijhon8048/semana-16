class Venta:
    def __init__(
        self,
        codigo: str,
        fecha: str,
        usuario_identificacion: str,
        nombre_usuario: str,
        producto_codigo: str,
        producto_nombre: str,
        cantidad: int,
        precio_unitario: float,
    ) -> None:
        if not codigo.strip():
            raise ValueError("El código de venta no puede estar vacío.")
        if not fecha.strip():
            raise ValueError("La fecha de venta no puede estar vacía.")
        if not usuario_identificacion.strip() or not nombre_usuario.strip():
            raise ValueError("La venta debe tener un usuario registrado.")
        if not producto_codigo.strip() or not producto_nombre.strip():
            raise ValueError("La venta debe tener un producto registrado.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")

        self.codigo = codigo.strip()
        self.fecha = fecha.strip()
        self.usuario_identificacion = usuario_identificacion.strip()
        self.nombre_usuario = nombre_usuario.strip()
        self.producto_codigo = producto_codigo.strip()
        self.producto_nombre = producto_nombre.strip()
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = cantidad * precio_unitario

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "fecha": self.fecha,
            "usuario_identificacion": self.usuario_identificacion,
            "nombre_usuario": self.nombre_usuario,
            "producto_codigo": self.producto_codigo,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, datos: dict):
        return cls(
            codigo=str(datos["codigo"]),
            fecha=str(datos["fecha"]),
            usuario_identificacion=str(datos["usuario_identificacion"]),
            nombre_usuario=str(datos["nombre_usuario"]),
            producto_codigo=str(datos["producto_codigo"]),
            producto_nombre=str(datos["producto_nombre"]),
            cantidad=int(datos["cantidad"]),
            precio_unitario=float(datos["precio_unitario"]),
        )
