import json
import os
import signal
from collections import defaultdict
from datetime import datetime

# Definimos las rutas de las carpetas
FACTURAS_DIR = './facturas/'
DISTRIBUSION_DIR = os.path.join(FACTURAS_DIR, 'distribusion/')
VENTA_CIUDAD_DIR = os.path.join(FACTURAS_DIR, 'venta_ciudad/')
INGRESO_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_ingreso/')
VENTA_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_venta/')
GASTOS_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_gastos/')
INVENTARIO_FILE = 'inventario.json'  # Archivo para guardar el inventario

# Clase Producto para gestionar los productos
class Producto:
    def __init__(self, nombre, precio, cantidad, descuento):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.fecha_de_compra = self.obtener_fecha_actual()
        self.total = self.calcular_total()
        self.cantidad_vendida = 1
        self.ventas = []

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def calcular_total(self):
        total_descuento = self.precio * self.cantidad * (1 - self.descuento / 100)
        return total_descuento

    def imprimir_factura(self):
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
        self.cantidad_vendida += cantidad_vendida
        self.ventas.append({'cantidad': cantidad_vendida, 'ciudad': ciudad_destino, 'local': nombre_local, 'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')})
        return factura_venta

# Clase para gestionar los gastos
class Gasto:
    def __init__(self, descripcion, monto):
        self.descripcion = descripcion
        self.monto = monto
        self.fecha_de_gasto = self.obtener_fecha_actual()

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def imprimir_factura_gasto(self):
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

# Crear las carpetas necesarias
def crear_carpetas():
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

# Persistir el inventario en un archivo JSON
def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump({k: v.__dict__ for k, v in inventario.items()}, f)

# Cargar el inventario desde el archivo JSON
def cargar_inventario():
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, 'r') as f:
            inventario_data = json.load(f)
            return {nombre: Producto(**data) for nombre, data in inventario_data.items()}
    return {}

# Guardar las facturas
def guardar_factura(registro, tipo):
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

    print(f"Guardando factura en: {archivo}")  # Debug
    with open(archivo, 'a') as f:
        f.write(registro + "\n")

# Guardar la ciudad de destino y el local en venta_ciudad.txt
def guardar_venta_ciudad(producto):
    archivo_ciudad = os.path.join(VENTA_CIUDAD_DIR, 'venta_ciudad.txt')

    with open(archivo_ciudad, 'a') as f:
        for venta in producto.ventas:
            linea = f"Ciudad: {venta['ciudad']:<20} | Local: {venta['local']:<20} | Producto: {producto.nombre:<15} | Cantidad: {venta['cantidad']:<10} | Fecha: {venta['fecha']}\n"
            f.write(linea)

# Actualizar el archivo resumen_distribusion.txt
def actualizar_distribusion(inventario):
    crear_carpetas()

    if not inventario:
        print("El inventario está vacío. No se puede generar el resumen.")
        return

    archivo_distribusion = os.path.join(DISTRIBUSION_DIR, 'resumen_distribusion.txt')

    with open(archivo_distribusion, 'w') as f:
        print(f"Creando o actualizando {archivo_distribusion}...")

        f.write("{:<20} {:<10} {:<10} {:<20} {:<15}  {:<10}\n".format(
            'Producto', 'Cantidad', 'Precio', 'Productos vendidos', 'Ciudad de destino', 'Local'))
        f.write('-' * 100 + '\n')

        conteo_ventas = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        for nombre, producto in inventario.items():
            for venta in producto.ventas:
                conteo_ventas[nombre][venta['ciudad']][venta['local']] += venta['cantidad']

        for nombre, ciudades in conteo_ventas.items():
            for ciudad, locales in ciudades.items():
                for local, cantidad in locales.items():
                    f.write(f"{nombre:<20} {inventario[nombre].cantidad:<10} ${inventario[nombre].precio:<10.2f} {cantidad:<20} {ciudad:<15} {local:<10}\n")
            f.write('-' * 100 + '\n')

    print(f"El archivo resumen_distribusion.txt ha sido actualizado.")

# Crear un producto
def crear_producto():
    print('Introduce los datos del producto:')
    nombre = input('Nombre del producto: ').strip()
    precio = float(input('Precio del producto: '))
    cantidad = int(input('Cantidad del producto: '))
    descuento = float(input('Descuento en %: '))

    producto = Producto(nombre, precio, cantidad, descuento)
    guardar_factura(producto.imprimir_factura(), 'ingreso')
    return producto

# Crear un gasto
def crear_gasto():
    print('Introduce los datos del gasto:')
    descripcion = input('Descripción del gasto: ').strip()
    monto = float(input('Monto del gasto: '))
    
    gasto = Gasto(descripcion, monto)
    guardar_factura(gasto.imprimir_factura_gasto(), 'gasto')

# Función para gestionar las ventas
def realizar_venta(inventario):
    nombre_producto = input("Introduce el nombre del producto a vender: ").strip()
    if nombre_producto in inventario:
        cantidad_vendida = int(input("Introduce la cantidad a vender: "))
        ciudad_destino = input("Introduce la ciudad de destino: ").strip()
        nombre_local = input("Introduce el nombre del local: ").strip()

        if cantidad_vendida <= inventario[nombre_producto].cantidad:
            factura_venta = inventario[nombre_producto].imprimir_factura_venta(cantidad_vendida, ciudad_destino, nombre_local)
            guardar_factura(factura_venta, 'venta')
            guardar_venta_ciudad(inventario[nombre_producto])
            actualizar_distribusion(inventario)

            inventario[nombre_producto].cantidad -= cantidad_vendida
            guardar_inventario(inventario)  # Guardamos el inventario actualizado
            print("Venta realizada y factura guardada.")
        else:
            print("No hay suficiente cantidad disponible para vender.")
    else:
        print("Producto no encontrado en el inventario.")

# Función principal
def main():
    crear_carpetas()
    inventario = cargar_inventario()

    while True:
        print("\nOpciones:")
        print("1. Crear un nuevo producto")
        print("2. Crear un gasto")
        print("3. Realizar una venta")
        print("4. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            producto = crear_producto()
            inventario[producto.nombre] = producto
            guardar_inventario(inventario)  # Guardamos el nuevo producto en el inventario
        elif opcion == '2':
            crear_gasto()
        elif opcion == '3':
            realizar_venta(inventario)
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
