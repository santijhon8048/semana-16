# restaurante_app

**Estudiante:** Cesar Santi

Aplicación de escritorio para la gestión de un restaurante, desarrollada con Python y Tkinter.

## Propósito

Esta etapa implementa la estructura base del sistema y concentra las operaciones de:

- Registro, búsqueda, actualización y eliminación de productos.
- Registro, consulta, actualización y eliminación de usuarios por un administrador.
- Diferenciación de usuarios mediante los roles Administrador, Empleado y Cliente.
- Inicio de sesión con nombre de usuario y contraseña.
- Registro y consulta de ventas.
- Lectura y escritura de datos en archivos JSON.

Los modelos incluidos son `Producto`, `Usuario` y `Venta`.

## Gestión de usuarios

La pestaña **Usuarios** solo está disponible para una cuenta con rol **Administrador**. Desde ella se pueden registrar cuentas de tipo **Administrador**, **Empleado** o **Cliente**. Los usuarios **Administrador** se pueden iniciar sesión, pero no aparecen en la tabla ni se pueden actualizar o eliminar desde esta pestaña. Los usuarios **Empleado** y **Cliente** sí se pueden consultar, actualizar y eliminar. Al seleccionar una fila, la aplicación carga sus datos en el formulario; al actualizar, dejar el campo de contraseña vacío conserva la contraseña actual.

El formulario permite seleccionar cualquiera de los tres roles al registrar una cuenta. Solo un administrador autenticado puede registrar cuentas, incluso otras cuentas administradoras. `Enter` confirma el registro y `Escape` limpia el formulario y cancela la selección.

## Estructura del proyecto

```text
restaurante_app/
├── main.py
├── README.md
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── assets/
│   ├── logo_restaurante.png
│   ├── logo_panel.png
│   ├── producto.png
│   ├── usuario.png
│   └── venta.png
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
└── ui/
    ├── __init__.py
    ├── login_view.py
    └── main_view.py
```

### Responsabilidad de cada módulo

- `modelos/`: define las entidades `Producto`, `Usuario` y `Venta`.
- `servicios/archivo_servicio.py`: carga y guarda productos, usuarios y ventas en JSON.
- `servicios/restaurante_servicio.py`: concentra las operaciones del restaurante.
- `ui/login_view.py`: muestra el formulario de inicio de sesión.
- `assets/logo_restaurante.png`: logo mostrado encima del título en el inicio de sesión.
- `ui/main_view.py`: muestra el panel para administrar productos, usuarios y ventas.
- `main.py`: configura la aplicación, carga los datos y abre la interfaz gráfica.

## Requisitos

- Python 3.10 o una versión posterior.
- Tkinter, incluido normalmente en la instalación estándar de Python.

No se requieren paquetes externos.

## Ejecución

1. Abrir una terminal en la carpeta que contiene `restaurante_app`.
2. Ejecutar desde Windows:

```bash
.\.venv\Scripts\python.exe restaurante_app\main.py
```

También puede ejecutarse entrando primero en la carpeta de la aplicación:

```bash
cd restaurante_app
python main.py
```

Al iniciar, la aplicación carga los datos de `datos/productos.json`, `datos/usuarios.json` y `datos/ventas.json`.
Para ingresar, se debe utilizar el nombre de usuario y la contraseña de un usuario registrado. Los cambios realizados desde la interfaz se guardan automáticamente en los archivos JSON correspondientes.

Los registros de `datos/usuarios.json` que no tengan el campo `rol` se cargan inicialmente como clientes. Si no existe ningún administrador, el primer usuario válido del archivo se habilita como administrador para conservar el acceso a la gestión. El rol se guarda en JSON junto con el resto de los datos cuando la aplicación guarda cambios.
