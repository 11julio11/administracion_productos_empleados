from datetime import datetime
import os

DISTRIBUSION_DIR = './distribusion/'

class Producto:
    def __init__(self, nombre, precio, cantidad, descuento):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.fecha_de_compra = self.obtener_fecha_actual()
        self.total = self.calcular_total()

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

    def imprimir_factura_venta(self, cantidad_vendida):
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
            f"{'=' * 50}\n"
        )
        return factura_venta

def guardar_factura(registro, tipo):
    if tipo == 'ingreso':
        archivo = os.path.join('facturas', 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join('facturas', 'facturas_venta.txt')
    else:
        print("Tipo de factura no válido.")
        return
    
    # Asegúrate de que el directorio para las facturas exista
    if not os.path.exists('facturas'):
        os.makedirs('facturas')
    
    with open(archivo, 'a') as f:
        f.write(registro + "\n")

def crear_producto():
    print('Introduce los datos del producto:')
    nombre = input('Nombre del producto: ').strip()
    precio = float(input('Precio del producto: '))
    cantidad = int(input('Cantidad del producto: '))
    descuento = float(input('Descuento en %: '))

    producto = Producto(nombre, precio, cantidad, descuento)
    return producto

def agregar_al_inventario(producto, inventario):
    if producto.nombre in inventario:
        inventario[producto.nombre].cantidad += producto.cantidad
    else:
        inventario[producto.nombre] = producto

def mostrar_inventario(inventario):
    for nombre, producto in inventario.items():
        print(f'Producto: {nombre}, Cantidad: {producto.cantidad}, Precio: ${producto.precio:.2f}, Descuento: {producto.descuento}%')

def gestionar_salida(inventario):
    mostrar_inventario(inventario)
    producto_salida = input('Introduce el nombre del producto que deseas vender: ').strip()

    if producto_salida in inventario:
        cantidad_salida = int(input('Introduce la cantidad que deseas vender: '))
        if inventario[producto_salida].cantidad >= cantidad_salida:
            factura_venta = inventario[producto_salida].imprimir_factura_venta(cantidad_salida)
            inventario[producto_salida].cantidad -= cantidad_salida
            guardar_factura(factura_venta, 'venta')
            return factura_venta
        else:
            print(f'No hay suficiente stock de {producto_salida}.')
    else:
        print(f'El producto {producto_salida} no existe en el inventario.')
    return ""

def mostrar_facturas(tipo):
    if tipo == 'ingreso':
        archivo = os.path.join('facturas', 'facturas_ingreso.txt')
    elif tipo == 'venta':
        archivo = os.path.join('facturas', 'facturas_venta.txt')
    else:
        print("Tipo de factura no válido.")
        return
    
    if not os.path.exists(archivo):
        print(f"No hay facturas de {tipo} disponibles.")
        return
    
    with open(archivo, 'r') as f:
        print(f.read())

def actualizar_distribusion(inventario):
    archivo_distribusion = os.path.join(DISTRIBUSION_DIR, 'resumen_distribusion.txt')

    with open(archivo_distribusion, 'w') as f:
        f.write("{:<15} {:<10} {:<10}\n".format('Producto', 'Cantidad', 'Precio'))
        for nombre, producto in inventario.items():
            f.write(f"{nombre:<15} {producto.cantidad:<10} ${producto.precio:<10.2f}\n")

    print(f"Distribución actualizada en: {archivo_distribusion}")

def main():
    inventario = {}

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
            actualizar_distribusion(inventario, DISTRIBUSION_DIR)

        elif opcion == '2':
            factura_venta = gestionar_salida(inventario)
            if factura_venta:
                print(factura_venta)
            actualizar_distribusion(inventario, DISTRIBUSION_DIR)

        elif opcion == '3':
            mostrar_inventario(inventario)

        elif opcion == '4':
            actualizar_distribusion(inventario, DISTRIBUSION_DIR)

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
