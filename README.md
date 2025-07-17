# Proyecto de Gestión de Inventario de Artículos de Oficina

Este proyecto es una aplicación de escritorio desarrollada en Python para la gestión de inventario de artículos de oficina. Utiliza una arquitectura modular basada en el patrón MVC (Modelo-Vista-Controlador) y una interfaz gráfica construida con Tkinter.

## Arquitectura del Proyecto

El proyecto está organizado en los siguientes módulos principales:

- **Entidades/**: Contiene las clases que representan las entidades del dominio, como `Usuario`, `Producto`, `Movimiento` y `Solicitud`.
- **Controladoras/**: Incluye los controladores responsables de la lógica de negocio y la gestión de las entidades.
- **Vistas/**: Implementa la interfaz gráfica de usuario (GUI) usando Tkinter, permitiendo la interacción con el sistema.
- **Utils/**: Utilidades y funciones auxiliares, como la gestión de seguridad y el manejo de contraseñas.
- **main.py**: Punto de entrada de la aplicación.

## Funcionalidades Principales

- **Gestión de Usuarios**: Registro, edición y visualización de usuarios con diferentes roles (admin, responsable, empleado).
- **Gestión de Productos**: Alta, edición y visualización de productos en el inventario.
- **Movimientos de Inventario**: Registro de entradas y salidas de productos.
- **Gestión de Solicitudes**: Permite a los usuarios solicitar productos y gestionar dichas solicitudes.
- **Reportes**: Visualización de reportes de stock y movimientos.
- **Seguridad**: Manejo de contraseñas seguras mediante hashing con `bcrypt`.

## Dependencias

- Python 3.10+
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (incluido en la mayoría de las instalaciones de Python)
- [bcrypt](https://pypi.org/project/bcrypt/) (para el manejo seguro de contraseñas)

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone <URL-del-repositorio>
   cd ProyectoFinalLenguajesDeProgramacion
   ```

2. **Instala las dependencias:**
   Si no tienes `pip` configurado, revisa que Python esté en tu PATH y usa:
   ```sh
   pip install bcrypt
   ```

3. **Ejecuta la aplicación:**
   ```sh
   python main.py
   ```

## Uso

Al ejecutar el proyecto, se abrirá una ventana de login. Ingresa con uno de los usuarios predefinidos (por ejemplo, usuario: `admin`, contraseña: `admin123`). Desde el menú principal podrás acceder a las diferentes funcionalidades según tu rol.

## Estructura de Carpetas

```
ProyectoFinalLenguajesDeProgramacion/
│   main.py
├── Controladoras/
├── Entidades/
├── Utils/
├── Vistas/
```

## Notas
- El sistema está pensado para ser ejecutado en entornos Windows, pero puede adaptarse a otros sistemas operativos.
- Si tienes problemas con la instalación de dependencias, asegúrate de tener Python y pip correctamente configurados.

## Licencia
Este proyecto es de uso académico y puede ser modificado para fines educativos. Elaborado para el curso de lenguajes de programación de la Universidad Tecnológica del Perú
