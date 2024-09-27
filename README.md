# Sistema de Gestión de Productos y Empleados

Este proyecto es un sistema diseñado para gestionar productos, ventas, gastos, y empleados, permitiendo un control eficiente de las operaciones de un negocio.

## Características

- **Gestión de Productos**: Registro de productos, cambios de precio y eliminación.
- **Gestión de Ventas**: Registrar ventas, generar facturas de ventas y distribuir productos por ciudad.
- **Gestión de Gastos**: Registro de gastos operacionales.
- **Gestión de Empleados**: Registro de empleados, control de turnos de trabajo con temporizador, generación de informes de actividad.
- **Manejo de Facturación**: Generación de facturas separadas para ingresos, ventas y gastos.
- **Persistencia de Datos**: Almacenamiento de datos de productos y empleados en archivos JSON.

## Estructura del Proyecto
- [employees](employees)
  - [registro_employees](employees/registro_employees)
    - [cesar_perez_rodriguez](employees/registro_employees/cesar_perez_rodriguez)
    - [david_perez_gomez_marin](employees/registro_employees/david_perez_gomez_marin)
- [facturas](facturas)
  - [distribucion](facturas/distribucion)
    - [resumen_distribucion.txt](facturas/distribucion/resumen_distribucion.txt)
  - [facturas_gastos](facturas/facturas_gastos)
    - [facturas_gastos.txt](facturas/facturas_gastos/facturas_gastos.txt)
  - [facturas_ingreso](facturas/facturas_ingreso)
    - [facturas_ingreso.txt](facturas/facturas_ingreso/facturas_ingreso.txt)
  - [facturas_venta](facturas/facturas_venta)
    - [facturas_venta.txt](facturas/facturas_venta/facturas_venta.txt)
  - [venta_ciudad](facturas/venta_ciudad)
    - [venta_ciudad.txt](facturas/venta_ciudad/venta_ciudad.txt)
- [ingreso_y_ventas](ingreso_y_ventas)
  - [__init__.py](ingreso_y_ventas/__init__.py)
  - [gestion_productos.py](ingreso_y_ventas/gestion_productos.py)
- [employees_data.json](employees_data.json)
- [inventario.json](inventario.json)
- [README.md](README.md)



markdown
Copiar código

## Requisitos

- Python 3.x
- Librerías de Python: `os`, `json`, `datetime`, `signal`

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clona este repositorio:
   
   git clone git@github.com:11julio11/factura_python.git
   cd nombre-del-repositorio
Instala las dependencias necesarias:


pip install -r requirements.txt
Ejecuta el archivo main.py para iniciar el sistema:


# python main.py

Uso del Sistema

# Al ejecutar el sistema, tendrás acceso a un menú interactivo con las siguientes opciones:

Ingresar producto: Permite agregar nuevos productos al inventario.
Vender producto: Registra la venta de productos y genera facturas.
Registrar gasto: Permite introducir los gastos operacionales.
Mostrar facturas: Muestra facturas de ingreso, venta y gastos.
Mostrar inventario: Lista todos los productos disponibles en el inventario.
Actualizar distribución: Permite registrar la distribución de productos por ciudad.
Gestionar empleados: Registro y control de los turnos de los empleados.
Salir: Cierra el sistema.
Gestión de Empleados
La opción de gestión de empleados permite:

# Registrar nuevos empleados con su información personal.
Controlar el inicio y fin de los turnos de trabajo.
Generar informes detallados sobre el tiempo trabajado de cada empleado, almacenados en archivos de texto específicos por empleado.
Gestión de Facturación
El sistema permite generar facturas para:

# Ingreso de productos: Registra los productos que entran al inventario.
Venta de productos: Registra ventas y genera un archivo de texto para cada venta.
Gastos operativos: Permite agregar los gastos relacionados con la operación del negocio.
Los archivos de facturas se almacenan en carpetas específicas bajo la carpeta facturas.

# Contribuciones
Si deseas contribuir al proyecto:

# Haz un fork del repositorio.
Crea una nueva rama para tus cambios:

git checkout -b feature/nueva-funcionalidad
Realiza tus cambios y haz commit de ellos:

git commit -m "Añadir nueva funcionalidad"
Sube tus cambios a GitHub:

git push origin feature/nueva-funcionalidad

Abre un Pull Request para revisión.





He reorganizado la estructura para que las carpetas relacionadas estén agrupadas y sea más fácil de entender. Si necesitas más cambios, házmelo saber.






