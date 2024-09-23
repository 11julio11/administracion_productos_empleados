from datetime import datetime
import os
from collections import defaultdict

# Definimos las rutas de las carpetas
FACTURAS_DIR = './facturas/'
DISTRIBUSION_DIR = os.path.join(FACTURAS_DIR, 'distribusion/')
VENTA_CIUDAD_DIR = os.path.join(FACTURAS_DIR, 'venta_ciudad/')
INGRESO_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_ingreso/')
VENTA_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_venta/')
GASTOS_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_gastos/')

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

    with open(archivo, 'a') as f:
        f.write(registro + "\n")

# Guardar la ciudad de destino y el local en venta_ciudad.txt
def guardar_venta_ciudad(producto):
    archivo_ciudad = os.path.join(VENTA_CIUDAD_DIR, 'venta_ciudad.txt')

    with open(archivo_ciudad, 'a') as f:
        for venta in producto.ventas:
            linea = f"Producto: {producto.nombre:<15} | Cantidad: {venta['cantidad']:<10} | Ciudad: {venta['ciudad']:<20} | Local: {venta['local']:<20} | Fecha: {venta['fecha']}\n"
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
def registrar_gasto():
    print('Introduce los datos del gasto:')
    descripcion = input('Descripción del gasto: ').strip()
    monto = float(input('Monto del gasto: '))
    
    gasto = Gasto(descripcion, monto)
    guardar_factura(gasto.imprimir_factura_gasto(), 'gasto')
    return gasto

# Agregar un producto al inventario
def agregar_al_inventario(producto, inventario):
    if producto.nombre in inventario:
        inventario[producto.nombre].cantidad += producto.cantidad
    else:
        inventario[producto.nombre] = producto

# Mostrar inventario
def mostrar_inventario(inventario):
    for nombre, producto in inventario.items():
        print(f"{nombre}: Cantidad {producto.cantidad}, Precio ${producto.precio:.2f}, Descuento {producto.descuento}%")

# Realizar una venta
def realizar_venta(inventario):
    mostrar_inventario(inventario)
    nombre_producto = input("Introduce el nombre del producto que deseas vender: ").strip()

    if nombre_producto in inventario:
        producto = inventario[nombre_producto]
        cantidad = int(input(f"¿Cuántas unidades de {producto.nombre} quieres vender?: "))
        ciudad_destino = input("Introduce la ciudad de destino: ").strip()
        nombre_local = input("Introduce el nombre del local: ").strip()

        if cantidad > producto.cantidad:
            print("No hay suficiente inventario.")
            return

        producto.cantidad -= cantidad
        factura_venta = producto.imprimir_factura_venta(cantidad, ciudad_destino, nombre_local)
        guardar_factura(factura_venta, 'venta')
        guardar_venta_ciudad(producto)

        print(factura_venta)
        actualizar_distribusion(inventario)
    else:
        print("El producto no existe en el inventario.")

# Mostrar facturas guardadas
def mostrar_facturas(tipo):
    if tipo == 'ingreso':
        archivo = os.path.join(INGRESO_FACTURAS_DIR, 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join(VENTA_FACTURAS_DIR, 'facturas_venta.txt')
    elif tipo == 'gasto':
        archivo = os.path.join(GASTOS_FACTURAS_DIR, 'facturas_gastos.txt')
    else:
        print("Tipo de facturas no válido.")
        return

    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            contenido = f.read()
            print(f"\nFacturas de {tipo}:\n{contenido}")
    else:
        print(f"No se encontraron facturas de {tipo}.")

# Función principal
def main():
    inventario = {}
    while True:
        print("\n--- Menú de opciones ---")
        print("1. Ingresar nuevo producto")
        print("2. Registrar venta")
        print("3. Mostrar inventario")
        print("4. Registrar gasto")
        print("5. Mostrar facturas de ingreso")
        print("6. Mostrar facturas de venta")
        print("7. Mostrar facturas de gasto")
        print("8. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':
            producto = crear_producto()
            agregar_al_inventario(producto, inventario)
        elif opcion == '2':
            realizar_venta(inventario)
        elif opcion == '3':
            mostrar_inventario(inventario)
        elif opcion == '4':
            registrar_gasto()
        elif opcion == '5':
            mostrar_facturas('ingreso')
        elif opcion == '6':
            mostrar_facturas('venta')
        elif opcion == '7':
            mostrar_facturas('gasto')
        elif opcion == '8':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
