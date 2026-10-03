import json

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:

    def __init__(self, ruta_archivo: str) -> None:
        self.ruta_archivo = ruta_archivo

    def guardar_datos(self, datos: list[dict]) -> bool:

        try:

            with open(
                self.ruta_archivo,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except PermissionError:

            print(
                f"Error: no hay permisos para escribir "
                f"{self.ruta_archivo}."
            )

            return False

        except OSError as error:

            print(
                f"Error al guardar el archivo: {error}"
            )

            return False

    def cargar_datos(self) -> list[dict]:

        try:

            with open(
                self.ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):

                print(
                    "Error: el archivo debe contener "
                    "una lista."
                )

                return []

            return datos

        except FileNotFoundError:

            print(
                f"Información: {self.ruta_archivo} "
                "todavía no existe."
            )

            return []

        except json.JSONDecodeError:

            print(
                f"Error: {self.ruta_archivo} "
                "contiene JSON inválido."
            )

            return []

        except PermissionError:

            print(
                f"Error: no hay permisos para leer "
                f"{self.ruta_archivo}."
            )

            return []

        except OSError as error:

            print(
                f"Error al leer el archivo: {error}"
            )

            return []

    # ======================================================
    # PRODUCTOS
    # ======================================================

    def guardar_productos(
        self,
        productos: list[Producto]
    ) -> bool:

        datos = [
            producto.to_dict()
            for producto in productos
        ]

        return self.guardar_datos(datos)

    def cargar_productos(self) -> list[Producto]:

        datos = self.cargar_datos()

        productos: list[Producto] = []

        for indice, registro in enumerate(
            datos,
            start=1
        ):

            try:

                if not isinstance(registro, dict):
                    continue

                productos.append(
                    Producto.from_dict(registro)
                )

            except (KeyError, ValueError, TypeError) as error:

                print(
                    f"Advertencia en producto {indice}: "
                    f"{error}"
                )

        return productos

    # ======================================================
    # USUARIOS
    # ======================================================

    def guardar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> bool:

        datos = [
            usuario.to_dict()
            for usuario in usuarios
        ]

        return self.guardar_datos(datos)

    def cargar_usuarios(self) -> list[Usuario]:

        datos = self.cargar_datos()

        usuarios: list[Usuario] = []

        for indice, registro in enumerate(
            datos,
            start=1
        ):

            try:

                if not isinstance(registro, dict):
                    continue

                usuarios.append(
                    Usuario.from_dict(registro)
                )

            except (KeyError, ValueError, TypeError) as error:

                print(
                    f"Advertencia en usuario {indice}: "
                    f"{error}"
                )

        return usuarios

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        datos = [venta.to_dict() for venta in ventas]
        return self.guardar_datos(datos)

    def cargar_ventas(self) -> list[Venta]:
        datos = self.cargar_datos()
        ventas: list[Venta] = []

        for indice, registro in enumerate(datos, start=1):
            try:
                if not isinstance(registro, dict):
                    continue
                ventas.append(Venta.from_dict(registro))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Advertencia en venta {indice}: {error}")

        return ventas
