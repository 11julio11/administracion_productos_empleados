# Importamos el módulo datetime para obtener la fecha y hora actuales
from datetime import datetime

# Creamos una clase Producto para gestionar las propiedades y funciones de cada producto
class Producto:
    def __init__(self, nombre, precio, cantidad, descuento):
        # Inicializamos los atributos del producto
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.fecha_de_compra = self.obtener_fecha_actual()  # Fecha actual al agregar el producto
        self.total = self.calcular_total()  # Calculamos el total del producto con el descuento aplicado

    # Método para obtener la fecha actual en formato dd/mm/yyyy
    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    # Método para calcular el total del producto aplicando el descuento
    def calcular_total(self):
        total_descuento = self.precio * self.cantidad * (1 - self.descuento / 100)
        return total_descuento

    # Método para imprimir la factura de ingreso del producto (al agregarlo al inventario)
    def imprimir_factura(self):
        factura = (
            f"\n{'=' * 30}\n"
            f"            FACTURA DE INGRESO           \n"
            f"{'=' * 30}\n"
            f"Fecha de ingreso: {self.fecha_de_compra}\n"
            f"Producto: {self.nombre}\n"
            f"Precio unitario: ${self.precio:.2f}\n"
            f"Cantidad: {self.cantidad}\n"
            f"Descuento: {self.descuento}%\n"
            f"Total a pagar: ${self.total:.2f}\n"
            f"{'=' * 30}\n"
        )
        print(factura)
        return factura  # Retornamos la factura para guardarla en archivo

    # Método para imprimir la factura de venta del producto
    def imprimir_factura_venta(self, cantidad_vendida):
        # Calculamos el total de la venta con el descuento
        total_venta = self.precio * cantidad_vendida * (1 - self.descuento / 100)
        factura_venta = (
            f"\n{'=' * 30}\n"
            f"         FACTURA DE VENTA        \n"
            f"{'=' * 30}\n"
            f"Fecha de venta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Producto: {self.nombre}\n"
            f"Cantidad vendida: {cantidad_vendida}\n"
            f"Precio unitario: ${self.precio:.2f}\n"
            f"Descuento: {self.descuento}%\n"
            f"Total a pagar: ${total_venta:.2f}\n"
            f"{'=' * 30}\n"
        )
        print(factura_venta)
        return factura_venta  # Retornamos la factura para guardarla en archivo

    # Método para cambiar el precio del producto y recalcular el total
    def cambiar_precio(self, precio):
        self.precio = precio
        self.total = self.calcular_total()  # Recalculamos el total con el nuevo precio

# Función para crear un nuevo producto, solicitando los datos al usuario
def crear_producto():
    print('Introduce los datos del producto:')
    nombre = input('Nombre del producto: ').strip()  # Eliminamos espacios adicionales
    precio = float(input('Precio del producto: '))
    cantidad = int(input('Cantidad del producto: '))
    descuento = float(input('Descuento en %: '))

    # Creamos una instancia de Producto con los datos ingresados
    producto = Producto(nombre, precio, cantidad, descuento)
    factura = producto.imprimir_factura()  # Imprimimos la factura y la guardamos
    
    return producto, factura  # Retornamos el producto y la factura

# Función para agregar un producto al inventario
def agregar_al_inventario(producto, inventario):
    inventario[producto.nombre] = producto  # Agregamos el producto al inventario

# Función para mostrar el inventario completo
def mostrar_inventario(inventario):
    for nombre, producto in inventario.items():
        print(f'Producto: {nombre}, Cantidad: {producto.cantidad}, Precio: ${producto.precio:.2f}, Descuento: {producto.descuento}%')

# Función para gestionar la salida (venta) de productos
def gestionar_salida(inventario):
    mostrar_inventario(inventario)  # Mostramos el inventario antes de la venta
    producto_salida = input('Introduce el nombre del producto que deseas vender: ').strip()

    # Verificamos si el producto existe en el inventario
    if producto_salida in inventario:
        cantidad_salida = int(input('Introduce la cantidad que deseas vender: '))
        
        # Verificamos si hay suficiente stock del producto
        if inventario[producto_salida].cantidad >= cantidad_salida:
            # Creamos un nuevo producto para gestionar la venta
            producto_salida_obj = Producto(
                nombre=producto_salida,
                precio=inventario[producto_salida].precio,
                cantidad=cantidad_salida,
                descuento=inventario[producto_salida].descuento
            )
            # Generamos e imprimimos la factura de venta
            factura_venta = producto_salida_obj.imprimir_factura_venta(cantidad_salida)
            
            # Actualizamos el inventario (restamos la cantidad vendida)
            inventario[producto_salida].cantidad -= cantidad_salida
            
            return factura_venta  # Retornamos la factura de la venta para guardarla
        else:
            print(f'No hay suficiente stock de {producto_salida}.')
    else:
        print(f'El producto {producto_salida} no existe en el inventario.')
    return ""  # Retornamos una cadena vacía si no se pudo completar la venta

# Función para guardar las facturas en archivos separados (ingreso y venta)
def guardar_en_archivo(registro, tipo):
    if tipo == 'ingreso':
        archivo = "facturas_ingreso.txt"  # Guardamos facturas de ingreso
    elif tipo == 'venta':
        archivo = "facturas_venta.txt"  # Guardamos facturas de venta
    else:
        print("Tipo de factura no válido.")
        return
    
    # Abrimos el archivo correspondiente y agregamos la factura
    with open(archivo, 'a') as f:
        f.write(registro + "\n")  # Agregamos un salto de línea al final

# Función principal del programa
def main():
    inventario = {}  # Diccionario para almacenar los productos en inventario
    while True:
        # Mostramos el menú de opciones
        print("\n1. Agregar producto")
        print("2. Vender producto")
        print("3. Mostrar inventario")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':  # Opción para agregar productos
            producto, factura = crear_producto()
            agregar_al_inventario(producto, inventario)  # Agregamos el producto al inventario
            guardar_en_archivo(factura, 'ingreso')  # Guardamos la factura de ingreso

        elif opcion == '2':  # Opción para vender productos
            registro_salida = gestionar_salida(inventario)
            if registro_salida:
                guardar_en_archivo(registro_salida, 'venta')  # Guardamos la factura de venta

        elif opcion == '3':  # Opción para mostrar el inventario
            mostrar_inventario(inventario)

        elif opcion == '4':  # Opción para salir del programa
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Ejecutamos la función principal solo si el archivo es ejecutado directamente
if __name__ == "__main__":
    main()
