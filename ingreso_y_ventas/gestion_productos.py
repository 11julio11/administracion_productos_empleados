import json  # Importamos el módulo para trabajar con archivos JSON.
import os  # Importamos el módulo para interactuar con el sistema de archivos.
import signal  # Importamos el módulo para manejar señales del sistema.
from collections import defaultdict  # Importamos defaultdict para crear diccionarios con valores por defecto.
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
    def __init__(self, nombre, precio, cantidad, descuento):
        self.nombre = nombre  # Nombre del producto.
        self.precio = precio  # Precio del producto.
        self.cantidad = cantidad  # Cantidad disponible en inventario.
        self.descuento = descuento  # Descuento aplicable al producto.
        self.fecha_de_compra = self.obtener_fecha_actual()  # Fecha de ingreso del producto.
        self.total = self.calcular_total()  # Total a pagar considerando el descuento.
        self.cantidad_vendida = 1  # Contador de cantidad vendida.
        self.ventas = []  # Lista para almacenar información sobre las ventas.

    def obtener_fecha_actual(self):
        # Devuelve la fecha actual en formato DD/MM/YYYY.
        return datetime.now().strftime("%d/%m/%Y")

    def calcular_total(self):
        # Calcula el total a pagar después de aplicar el descuento.
        total_descuento = self.precio * self.cantidad * (1 - self.descuento / 100)
        return total_descuento

    def imprimir_factura(self):
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
        self.ventas.append({'cantidad': cantidad_vendida, 'ciudad': ciudad_destino, 'local': nombre_local, 'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')})  # Añade la venta a la lista.
        return factura_venta

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
            linea = f"Ciudad: {venta['ciudad']:<20} | Local: {venta['local']:<20} | Producto: {producto.nombre:<15} | Cantidad: {venta['cantidad']:<10} | Fecha: {venta['fecha']}\n"
            f.write(linea)  # Escribe la línea de venta en el archivo.

# Actualizar el archivo resumen_distribusion.txt.
def actualizar_distribusion(inventario):
    # Crea un resumen de la distribución de productos.
    crear_carpetas()

    if not inventario:
        print("El inventario está vacío. No se puede generar el resumen.")
        return

    archivo_distribusion = os.path.join(DISTRIBUSION_DIR, 'resumen_distribusion.txt')

    with open(archivo_distribusion, 'w') as f:
        for producto in inventario.values():
            f.write(f"Producto: {producto.nombre}, Cantidad vendida: {producto.cantidad_vendida}\n")  # Guarda el resumen.

# Manejo de señales para cerrar el programa.
def signal_handler(sig, frame):
    # Función que se ejecuta al recibir una señal de cierre.
    print("Cerrando el programa...")
    exit(0)

# Configurar la señal para manejar el cierre del programa.
signal.signal(signal.SIGINT, signal_handler)  # Permite cerrar el programa con Ctrl+C.

# Función principal para ejecutar el programa.
def main():
    crear_carpetas()  # Crea las carpetas necesarias.
    inventario = cargar_inventario()  # Carga el inventario existente.
    
    # Aquí puedes implementar más lógica del programa, como agregar productos, registrar ventas, etc.

if __name__ == "__main__":
    main()  # Llama a la función principal al ejecutar el script.
