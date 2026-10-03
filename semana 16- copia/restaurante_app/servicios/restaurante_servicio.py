from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Administra las operaciones de productos, usuarios y ventas."""

    def __init__(self) -> None:
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._usuarios_por_nombre_usuario: dict[str, Usuario] = {}
        self._ventas_por_codigo: dict[str, Venta] = {}

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos_por_codigo:
            return False
        self.productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        return self._productos_por_codigo.get(codigo.strip())

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        actualizado = Producto(codigo, nombre, categoria, precio, stock)
        producto.nombre = actualizado.nombre
        producto.categoria = actualizado.categoria
        producto.precio = actualizado.precio
        producto.stock = actualizado.stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        del self._productos_por_codigo[producto.codigo]
        return True

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def cargar_productos(self, productos: list[Producto]) -> None:
        self.productos.clear()
        self._productos_por_codigo.clear()
        for producto in productos:
            self.registrar_producto(producto)

    def registrar_usuario(
        self,
        usuario: Usuario,
        administrador: Usuario,
    ) -> bool:
        if not self._es_administrador(administrador):
            return False
        if usuario.rol not in Usuario.ROLES:
            raise ValueError("Seleccione un rol válido.")
        return self._registrar_usuario(usuario)

    def _registrar_usuario(self, usuario: Usuario) -> bool:
        if (
            usuario.identificacion in self._usuarios_por_identificacion
            or usuario.nombre_usuario.casefold() in self._usuarios_por_nombre_usuario
        ):
            return False
        self.usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        self._usuarios_por_nombre_usuario[usuario.nombre_usuario.casefold()] = usuario
        return True

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        nombre_usuario: str,
        contrasena: str,
        rol: str,
        administrador: Usuario,
    ) -> bool:
        if not self._es_administrador(administrador):
            return False
        usuario = self.buscar_usuario(identificacion)
        if usuario is None or usuario.rol == Usuario.ROL_ADMINISTRADOR:
            return False
        if rol not in (Usuario.ROL_EMPLEADO, Usuario.ROL_CLIENTE):
            raise ValueError("Solo se pueden asignar los roles Empleado o Cliente.")

        actualizado = Usuario(
            identificacion=usuario.identificacion,
            nombre=nombre,
            correo=correo,
            nombre_usuario=nombre_usuario,
            contrasena=contrasena or usuario.contrasena,
            rol=rol,
        )
        usuario_existente = self._usuarios_por_nombre_usuario.get(
            actualizado.nombre_usuario.casefold()
        )
        if usuario_existente is not None and usuario_existente is not usuario:
            return False

        del self._usuarios_por_nombre_usuario[usuario.nombre_usuario.casefold()]
        usuario.nombre = actualizado.nombre
        usuario.correo = actualizado.correo
        usuario.nombre_usuario = actualizado.nombre_usuario
        usuario.contrasena = actualizado.contrasena
        usuario.rol = actualizado.rol
        self._usuarios_por_nombre_usuario[usuario.nombre_usuario.casefold()] = usuario
        return True

    def eliminar_usuario(self, identificacion: str, administrador: Usuario) -> bool:
        if not self._es_administrador(administrador):
            return False
        usuario = self.buscar_usuario(identificacion)
        if usuario is None or usuario.rol == Usuario.ROL_ADMINISTRADOR:
            return False
        self.usuarios.remove(usuario)
        del self._usuarios_por_identificacion[usuario.identificacion]
        del self._usuarios_por_nombre_usuario[usuario.nombre_usuario.casefold()]
        return True

    def _es_administrador(self, usuario: Usuario) -> bool:
        registrado = self.buscar_usuario(usuario.identificacion)
        return registrado is usuario and usuario.rol == Usuario.ROL_ADMINISTRADOR

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        return self._usuarios_por_identificacion.get(identificacion.strip())

    def autenticar_usuario(
        self,
        nombre_usuario: str,
        contrasena: str,
    ) -> Usuario | None:
        usuario = self._usuarios_por_nombre_usuario.get(nombre_usuario.strip().casefold())
        if usuario is None or usuario.contrasena != contrasena:
            return None
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def cargar_usuarios(self, usuarios: list[Usuario]) -> None:
        self.usuarios.clear()
        self._usuarios_por_identificacion.clear()
        self._usuarios_por_nombre_usuario.clear()
        for usuario in usuarios:
            self._registrar_usuario(usuario)
        if self.usuarios and not any(
            usuario.rol == Usuario.ROL_ADMINISTRADOR for usuario in self.usuarios
        ):
            self.usuarios[0].rol = Usuario.ROL_ADMINISTRADOR

    def registrar_venta(
        self,
        usuario_identificacion: str,
        producto_codigo: str,
        cantidad: int,
    ) -> Venta:
        usuario = self.buscar_usuario(usuario_identificacion)
        if usuario is None:
            raise ValueError("Seleccione un usuario registrado.")

        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            raise ValueError("Seleccione un producto registrado.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > producto.stock:
            raise ValueError("No existe suficiente stock disponible.")

        numero = len(self.ventas) + 1
        codigo = f"V{numero:05d}"
        while codigo in self._ventas_por_codigo:
            numero += 1
            codigo = f"V{numero:05d}"
        venta = Venta(
            codigo=codigo,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            usuario_identificacion=usuario.identificacion,
            nombre_usuario=usuario.nombre_usuario,
            producto_codigo=producto.codigo,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )
        producto.vender(cantidad)
        self.ventas.append(venta)
        self._ventas_por_codigo[venta.codigo] = venta
        return venta

    def listar_ventas(self) -> list[Venta]:
        return self.ventas.copy()

    def cargar_ventas(self, ventas: list[Venta]) -> None:
        self.ventas.clear()
        self._ventas_por_codigo.clear()
        for venta in ventas:
            if venta.codigo not in self._ventas_por_codigo:
                self.ventas.append(venta)
                self._ventas_por_codigo[venta.codigo] = venta