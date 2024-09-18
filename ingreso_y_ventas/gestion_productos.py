from datetime import datetime
import os
from collections import defaultdict

# Definimos las rutas de las carpetas
FACTURAS_DIR = './facturas/'
DISTRIBUSION_DIR = os.path.join(FACTURAS_DIR, 'distribusion/')
VENTA_CIUDAD_DIR = os.path.join(FACTURAS_DIR, 'venta_ciudad/')
INGRESO_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_ingreso/')
VENTA_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_venta/')

# Creamos una clase para gestionar los productos
class Producto:
    def __init__(self, nombre, precio, cantidad, descuento):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.fecha_de_compra = self.obtener_fecha_actual()
        self.total = self.calcular_total()
        self.cantidad_vendida = 0  # Inicializamos la cantidad vendida a 0
        self.ventas = []  # Lista para almacenar las ventas, ciudades y nombres de locales
    
    # Método para obtener la fecha actual
    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")
    
    # Método para calcular el total del producto con el descuento aplicado
    def calcular_total(self):
        total_descuento = self.precio * self.cantidad * (1 - self.descuento / 100)
        return total_descuento

    # Método para imprimir la factura de ingreso
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

    # Método para imprimir la factura de venta con la ciudad de destino y el nombre del local
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
            f"Nombre del local: {nombre_local}\n"  # Agregar el nombre del local
            f"{'=' * 50}\n"
        )
        self.cantidad_vendida += cantidad_vendida  # Actualizamos la cantidad vendida
        self.ventas.append({'cantidad': cantidad_vendida, 'ciudad': ciudad_destino, 'local': nombre_local, 'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')})
        return factura_venta

# Asegurarse de que las carpetas necesarias existan
def crear_carpetas():
    if not os.path.exists(FACTURAS_DIR):
        os.makedirs(FACTURAS_DIR)
    if not os.path.exists(DISTRIBUSION_DIR):
        os.makedirs(DISTRIBUSION_DIR)
    if not os.path.exists(VENTA_CIUDAD_DIR):
        os.makedirs(VENTA_CIUDAD_DIR)  # Crear la carpeta venta_ciudad si no existe
    if not os.path.exists(INGRESO_FACTURAS_DIR):
        os.makedirs(INGRESO_FACTURAS_DIR)  # Crear la carpeta facturas_ingreso si no existe
    if not os.path.exists(VENTA_FACTURAS_DIR):
        os.makedirs(VENTA_FACTURAS_DIR)  # Crear la carpeta facturas_venta si no existe

# Guardar la factura en el archivo correspondiente
def guardar_factura(registro, tipo):
    crear_carpetas()  # Asegurarse de que las carpetas se crean antes de guardar
    if tipo == 'ingreso':
        archivo = os.path.join(INGRESO_FACTURAS_DIR, 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join(VENTA_FACTURAS_DIR, 'facturas_venta.txt')
    else:
        print("Tipo de factura no válido.")
        return

    with open(archivo, 'a') as f:
        f.write(registro + "\n")

# Guardar la ciudad de destino y el nombre del local en el archivo venta_ciudad.txt
def guardar_venta_ciudad(producto):
    archivo_ciudad = os.path.join(VENTA_CIUDAD_DIR, 'venta_ciudad.txt')

    with open(archivo_ciudad, 'a') as f:
        for venta in producto.ventas:
            f.write(f"Producto: {producto.nombre}, Cantidad vendida: {venta['cantidad']}, Ciudad de destino: {venta['ciudad']}, Nombre del local: {venta['local']}, Fecha: {venta['fecha']}\n")

# Función para crear un producto
def crear_producto():
    print('Introduce los datos del producto:')
    nombre = input('Nombre del producto: ').strip()
    precio = float(input('Precio del producto: '))
    cantidad = int(input('Cantidad del producto: '))
    descuento = float(input('Descuento en %: '))

    producto = Producto(nombre, precio, cantidad, descuento)
    guardar_factura(producto.imprimir_factura(), 'ingreso')  # Guardar la factura de ingreso
    return producto

# Función para agregar un producto al inventario
def agregar_al_inventario(producto, inventario):
    if producto.nombre in inventario:
        inventario[producto.nombre].cantidad += producto.cantidad
    else:
        inventario[producto.nombre] = producto

# Función para mostrar el inventario
def mostrar_inventario(inventario):
    for nombre, producto in inventario.items():
        print(f'Producto: {nombre}, Cantidad: {producto.cantidad}, Precio: ${producto.precio:.2f}, Descuento: {producto.descuento}%')

# Función para gestionar la venta de un producto y preguntar por la ciudad de destino y el nombre del local
def gestionar_salida(inventario):
    mostrar_inventario(inventario)
    producto_salida = input('Introduce el nombre del producto que deseas vender: ').strip()

    if producto_salida in inventario:
        cantidad_salida = int(input('Introduce la cantidad que deseas vender: '))
        if inventario[producto_salida].cantidad >= cantidad_salida:
            ciudad_destino = input('Introduce la ciudad de destino de la venta: ').strip()  # Preguntar ciudad destino
            nombre_local = input('Introduce el nombre del local de venta: ').strip()  # Preguntar nombre del local
            
            factura_venta = inventario[producto_salida].imprimir_factura_venta(cantidad_salida, ciudad_destino, nombre_local)
            inventario[producto_salida].cantidad -= cantidad_salida
            guardar_factura(factura_venta, 'venta')
            guardar_venta_ciudad(inventario[producto_salida])  # Guardar la ciudad de destino y el nombre del local en venta_ciudad.txt
            
            print(f"\nVenta realizada a la ciudad: {ciudad_destino} en el local: {nombre_local}")  # Mostrar la ciudad de destino y el nombre del local
            return factura_venta
        else:
            print(f'No hay suficiente stock de {producto_salida}.')
    else:
        print(f'El producto {producto_salida} no existe en el inventario.')
    return ""

# Mostrar facturas guardadas
def mostrar_facturas(tipo):
    if tipo == 'ingreso':
        archivo = os.path.join(INGRESO_FACTURAS_DIR, 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join(VENTA_FACTURAS_DIR, 'facturas_venta.txt')
    else:
        print("Tipo de factura no válido.")
        return

    if not os.path.exists(archivo):
        print(f"No hay facturas de {tipo} disponibles.")
        return

    with open(archivo, 'r') as f:
        print(f.read())

# Actualizar el archivo de resumen de distribución, incluyendo la ciudad de destino y el contador
def actualizar_distribusion(inventario):
    crear_carpetas()  # Asegurarse de que la carpeta de distribución esté creada
    archivo_distribusion = os.path.join(DISTRIBUSION_DIR, 'resumen_distribusion.txt')

    with open(archivo_distribusion, 'w') as f:
        # Escribir la cabecera de la tabla
        f.write("{:<20} {:<10} {:<10} {:<20} {:<15}\n".format('Producto', 'Cantidad', 'Precio', 'Productos vendidos', 'Ciudad de destino'))
        
        # Contador de ventas por ciudad y local
        conteo_ventas = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        for nombre, producto in inventario.items():
            for venta in producto.ventas:
                conteo_ventas[nombre][venta['ciudad']][venta['local']] += venta['cantidad']

        # Escribir cada producto en la tabla con el contador de ventas
        for nombre, ciudades in conteo_ventas.items():
            for ciudad, locales in ciudades.items():
                for local, cantidad in locales.items():
                    f.write(f"{nombre:<20} {inventario[nombre].cantidad:<10} ${inventario[nombre].precio:<10.2f} {cantidad:<20} {ciudad:<15}\n")

    print(f"Distribución actualizada en: {archivo_distribusion}")

# Función principal del programa
def main():
    inventario = {}
    crear_carpetas()  # Crear las carpetas necesarias al iniciar el programa

    while True:
        print("\n1. Agregar producto")
        print("2. Vender producto")
        print("3. Mostrar inventario")
        print("4. Actualizar distribución")
        print("5. Mostrar facturas de ingreso")
        print("6. Mostrar facturas de venta")
        print("7. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            producto = crear_producto()
            agregar_al_inventario(producto, inventario)
            actualizar_distribusion(inventario)

        elif opcion == '2':
            factura_venta = gestionar_salida(inventario)
            if factura_venta:
                print(factura_venta)
            actualizar_distribusion(inventario)

        elif opcion == '3':
            mostrar_inventario(inventario)

        elif opcion == '4':
            actualizar_distribusion(inventario)

        elif opcion == '5':
            mostrar_facturas('ingreso')

        elif opcion == '6':
            mostrar_facturas('venta')

        elif opcion == '7':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
