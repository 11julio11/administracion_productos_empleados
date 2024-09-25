import json  # Importamos el módulo para trabajar con archivos JSON.
import os  # Importamos el módulo para interactuar con el sistema de archivos.
import signal  # Importamos el módulo para manejar señales del sistema.
from datetime import datetime  # Importamos datetime para trabajar con fechas y horas.

# Definimos las rutas de las carpetas donde se almacenarán las facturas.
FACTURAS_DIR = './facturas/'  # Carpeta principal para las facturas.
DISTRIBUSION_DIR = os.path.join(FACTURAS_DIR, 'distribusion/')  # Carpeta para distribución.
VENTA_CIUDAD_DIR = os.path.join(FACTURAS_DIR, 'venta_ciudad/')  # Carpeta para ventas por ciudad.
INGRESO_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_ingreso/')  # Carpeta para facturas de ingreso.
VENTA_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_venta/')  # Carpeta para facturas de venta.
GASTOS_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_gastos/')  # Carpeta para facturas de gastos.
INVENTARIO_FILE = 'inventario.json'  # Archivo para guardar el inventario de productos.

# Clase Producto para gestionar los productos en el inventario.
class Producto:
    def __init__(self, nombre, precio, cantidad, descuento, fecha_de_compra=None, total=None, cantidad_vendida=0, ventas=None):
        self.nombre = nombre  # Nombre del producto.
        self.precio = precio  # Precio del producto.
        self.cantidad = cantidad  # Cantidad disponible en inventario.
        self.descuento = descuento  # Descuento aplicable al producto.
        self.fecha_de_compra = fecha_de_compra if fecha_de_compra is not None else self.obtener_fecha_actual()  # Fecha de ingreso del producto.
        self.total = total if total is not None else self.calcular_total()  # Total a pagar considerando el descuento.
        self.cantidad_vendida = cantidad_vendida  # Contador de cantidad vendida.
        self.ventas = ventas if ventas is not None else []  # Lista para almacenar información sobre las ventas.

    def obtener_fecha_actual(self):
        # Devuelve la fecha actual en formato DD/MM/YYYY.
        return datetime.now().strftime("%d/%m/%Y")

    def calcular_total(self):
        # Calcula el total a pagar después de aplicar el descuento.
        total_descuento = self.precio * self.cantidad * (1 - self.descuento / 100)
        return total_descuento

    def imprimir_factura_ingreso(self):
        # Genera una factura de ingreso del producto.
        factura = (
            f"\n{'=' * 50}\n"
            f"          FACTURA DE INGRESO   \n"
            f"{'=' * 50}\n"
            f"Fecha de ingreso: {self.fecha_de_compra}\n"
            f"Producto: {self.nombre}\n"
            f"Precio unitario: ${self.precio:.2f}\n"
            f"Cantidad: {self.cantidad}\n"
            f"Descuento: {self.descuento}%\n"
            f"Total a pagar: ${self.total:.2f}\n"
            f"{'=' * 50}\n"
        )
        return factura

    def imprimir_factura_venta(self, cantidad_vendida, ciudad_destino, nombre_local):
        # Genera una factura de venta del producto.
        total_venta = self.precio * cantidad_vendida * (1 - self.descuento / 100)
        factura_venta = (
            f"\n{'=' * 50}\n"
            f"            FACTURA DE VENTA    \n"
            f"{'=' * 50}\n"
            f"Fecha de venta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Producto: {self.nombre}\n"
            f"Cantidad vendida: {cantidad_vendida}\n"
            f"Precio unitario: ${self.precio:.2f}\n"
            f"Descuento: {self.descuento}%\n"
            f"Total a pagar: ${total_venta:.2f}\n"
            f"Ciudad de destino: {ciudad_destino}\n"
            f"Nombre del local: {nombre_local}\n"
            f"{'=' * 50}\n"
        )
        self.cantidad_vendida += cantidad_vendida  # Actualiza la cantidad vendida total.
        self.cantidad -= cantidad_vendida  # Actualiza la cantidad disponible en inventario.
        self.ventas.append({'cantidad': cantidad_vendida, 'ciudad': ciudad_destino, 'local': nombre_local, 'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')})  # Añade la venta a la lista.
        return factura_venta

    def mostrar_inventario(self):
        # Muestra la información del producto.
        return (
            f"Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | "
            f"Cantidad: {self.cantidad} | "
            f"Descuento: {self.descuento}% | "
            f"Cantidad Vendida: {self.cantidad_vendida}\n"
        )

# Clase para gestionar los gastos.
class Gasto:
    def __init__(self, descripcion, monto):
        self.descripcion = descripcion  # Descripción del gasto.
        self.monto = monto  # Monto del gasto.
        self.fecha_de_gasto = self.obtener_fecha_actual()  # Fecha del gasto.

    def obtener_fecha_actual(self):
        # Devuelve la fecha actual en formato DD/MM/YYYY.
        return datetime.now().strftime("%d/%m/%Y")

    def imprimir_factura_gasto(self):
        # Genera una factura del gasto.
        factura_gasto = (
            f"\n{'=' * 50}\n"
            f"            FACTURA DE GASTO    \n"
            f"{'=' * 50}\n"
            f"Fecha de gasto: {self.fecha_de_gasto}\n"
            f"Descripción: {self.descripcion}\n"
            f"Monto: ${self.monto:.2f}\n"
            f"{'=' * 50}\n"
        )
        return factura_gasto

# Crear las carpetas necesarias para almacenar las facturas.
def crear_carpetas():
    # Verifica y crea cada carpeta necesaria para almacenar las facturas.
    if not os.path.exists(FACTURAS_DIR):
        os.makedirs(FACTURAS_DIR)
    if not os.path.exists(DISTRIBUSION_DIR):
        os.makedirs(DISTRIBUSION_DIR)
    if not os.path.exists(VENTA_CIUDAD_DIR):
        os.makedirs(VENTA_CIUDAD_DIR)
    if not os.path.exists(INGRESO_FACTURAS_DIR):
        os.makedirs(INGRESO_FACTURAS_DIR)
    if not os.path.exists(VENTA_FACTURAS_DIR):
        os.makedirs(VENTA_FACTURAS_DIR)
    if not os.path.exists(GASTOS_FACTURAS_DIR):
        os.makedirs(GASTOS_FACTURAS_DIR)

# Persistir el inventario en un archivo JSON.
def guardar_inventario(inventario):
    # Guarda el inventario en un archivo JSON.
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump({k: v.__dict__ for k, v in inventario.items()}, f)

# Cargar el inventario desde el archivo JSON.
def cargar_inventario():
    # Carga el inventario desde el archivo JSON si existe.
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, 'r') as f:
            inventario_data = json.load(f)
            return {nombre: Producto(**data) for nombre, data in inventario_data.items()}  # Devuelve un diccionario de productos.
    return {}

# Guardar las facturas en archivos correspondientes.
def guardar_factura(registro, tipo):
    # Crea carpetas y guarda el registro en el archivo correspondiente según el tipo.
    crear_carpetas()
    if tipo == 'ingreso':
        archivo = os.path.join(INGRESO_FACTURAS_DIR, 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join(VENTA_FACTURAS_DIR, 'facturas_venta.txt')
    elif tipo == 'gasto':
        archivo = os.path.join(GASTOS_FACTURAS_DIR, 'facturas_gastos.txt')
    else:
        print("Tipo de factura no válido.")
        return

    with open(archivo, 'a') as f:
        f.write(registro + "\n")  # Añade el registro al archivo.

# Guardar la ciudad de destino y el local en venta_ciudad.txt.
def guardar_venta_ciudad(producto):
    # Guarda las ventas en un archivo específico por ciudad.
    archivo_ciudad = os.path.join(VENTA_CIUDAD_DIR, 'venta_ciudad.txt')

    with open(archivo_ciudad, 'a') as f:
        for venta in producto.ventas:
            f.write(f"Producto: {producto.nombre} | Ciudad: {venta['ciudad']} | Local: {venta['local']} | Cantidad: {venta['cantidad']} | Fecha: {venta['fecha']}\n")

# Actualizar el archivo resumen_distribusion.txt con el resumen de productos.
def actualizar_distribusion(inventario):
    # Actualiza el archivo de distribución con el resumen de productos.
    resumen_file = os.path.join(DISTRIBUSION_DIR, 'resumen_distribusion.txt')
    with open(resumen_file, 'w') as f:
        for nombre, producto in inventario.items():
            f.write(f"Producto: {nombre} | Cantidad vendida: {producto.cantidad_vendida} | Stock: {producto.cantidad}\n")
            for venta in producto.ventas:  # Iteramos sobre las ventas registradas del producto.
                f.write(f"Ciudad: {venta['ciudad']} | Local: {venta['local']}| Producto: {nombre} | Cantidad: {venta['cantidad']} | Fecha: {venta['fecha']}\n")
 # Escribe el resumen.

# Manejar la señal de interrupción (Ctrl+C) para cerrar el programa.
def manejar_salida(signal_num, frame):
    print("\nSaliendo del programa. ¡Hasta luego!")
    exit(0)

signal.signal(signal.SIGINT, manejar_salida)

def main():
    # Función principal que ejecuta el programa.
    crear_carpetas()  # Crea las carpetas necesarias al inicio.
    inventario = cargar_inventario()  # Carga el inventario existente.

    while True:
        print("\nOpciones:")
        print("1. Ingresar producto")
        print("2. Vender producto")
        print("3. Registrar gasto")
        print("4. Mostrar facturas")
        print("5. Mostrar inventario")  # Opción para mostrar inventario.
        print("6. Actualizar distribución")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            cantidad = int(input("Ingrese la cantidad del producto: "))
            descuento = float(input("Ingrese el descuento (%): "))
            producto = Producto(nombre, precio, cantidad, descuento)
            inventario[nombre] = producto  # Añade el nuevo producto al inventario.
            guardar_inventario(inventario)  # Guarda el inventario.
            factura = producto.imprimir_factura_ingreso()  # Genera la factura de ingreso.
            guardar_factura(factura, 'ingreso')  # Guarda la factura de ingreso.
            print(factura)  # Muestra la factura de ingreso.

        elif opcion == '2':
            nombre = input("Ingrese el nombre del producto a vender: ")
            if nombre in inventario:
                cantidad_vendida = int(input("Ingrese la cantidad a vender: "))
                ciudad_destino = input("Ingrese la ciudad de destino: ")
                nombre_local = input("Ingrese el nombre del local: ")
                factura_venta = inventario[nombre].imprimir_factura_venta(cantidad_vendida, ciudad_destino, nombre_local)  # Genera la factura de venta.
                guardar_factura(factura_venta, 'venta')  # Guarda la factura de venta.
                guardar_venta_ciudad(inventario[nombre])  # Guarda la venta por ciudad.
                actualizar_distribusion(inventario)  # Actualiza el archivo de distribución.
                guardar_inventario(inventario)  # Actualiza el inventario en el archivo JSON.
                print(factura_venta)  # Muestra la factura de venta.
            else:
                print("Producto no encontrado en el inventario.")

        elif opcion == '3':
            descripcion = input("Ingrese la descripción del gasto: ")
            monto = float(input("Ingrese el monto del gasto: "))
            gasto = Gasto(descripcion, monto)  # Crea un nuevo gasto.
            factura_gasto = gasto.imprimir_factura_gasto()  # Genera la factura del gasto.
            guardar_factura(factura_gasto, 'gasto')  # Guarda la factura del gasto.
            print(factura_gasto)  # Muestra la factura del gasto.

        elif opcion == '4':
            print("Mostrando facturas de ingreso, venta y gasto.")
            print("Facturas de ingreso:")
            with open(os.path.join(INGRESO_FACTURAS_DIR, 'facturas_ingreso.txt'), 'r') as f:
                print(f.read())
            print("Facturas de venta:")
            with open(os.path.join(VENTA_FACTURAS_DIR, 'facturas_venta.txt'), 'r') as f:
                print(f.read())
            print("Facturas de gasto:")
            with open(os.path.join(GASTOS_FACTURAS_DIR, 'facturas_gastos.txt'), 'r') as f:
                print(f.read())

        elif opcion == '5':
            print("Inventario actual:")
            for producto in inventario.values():
                print(producto.mostrar_inventario())  # Muestra el inventario.

        elif opcion == '6':
            actualizar_distribusion(inventario)  # Actualiza el archivo de distribución.
            print("Distribución actualizada.")

        elif opcion == '7':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    main()  # Ejecuta la función principal.
