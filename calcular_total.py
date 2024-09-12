from datetime import datetime

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
        return factura

    def imprimir_factura_venta(self, cantidad_vendida):
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
        return factura_venta

    def cambiar_precio(self, precio):
        self.precio = precio
        self.total = self.calcular_total()

def crear_producto():
    print('Introduce los datos del producto:')
    nombre = input('Nombre del producto: ').strip()
    precio = float(input('Precio del producto: '))
    cantidad = int(input('Cantidad del producto: '))
    descuento = float(input('Descuento en %: '))

    producto = Producto(nombre, precio, cantidad, descuento)
    factura = producto.imprimir_factura()
    
    return producto, factura

def agregar_al_inventario(producto, inventario):
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
            # Crear un nuevo objeto Producto para la factura de la salida
            producto_salida_obj = Producto(
                nombre=producto_salida,
                precio=inventario[producto_salida].precio,
                cantidad=cantidad_salida,
                descuento=inventario[producto_salida].descuento
            )
            # Generar y mostrar la factura de la venta
            factura_venta = producto_salida_obj.imprimir_factura_venta(cantidad_salida)
            
            # Actualizar la cantidad en el inventario
            inventario[producto_salida].cantidad -= cantidad_salida
            
            # Registrar la venta
            return factura_venta
        else:
            print(f'No hay suficiente stock de {producto_salida}.')
    else:
        print(f'El producto {producto_salida} no existe en el inventario.')
    return ""

def guardar_en_archivo(registro, tipo):
    if tipo == 'ingreso':
        archivo = "facturas_ingreso.txt"
    elif tipo == 'venta':
        archivo = "facturas_venta.txt"
    else:
        print("Tipo de factura no válido.")
        return
    
    with open(archivo, 'a') as f:
        f.write(registro + "\n")  # Aseguramos que cada registro esté separado por una línea

def main():
    inventario = {}
    while True:
        print("\n1. Agregar producto")
        print("2. Vender producto")
        print("3. Mostrar inventario")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            producto, factura = crear_producto()
            agregar_al_inventario(producto, inventario)
            guardar_en_archivo(factura, 'ingreso')

        elif opcion == '2':
            registro_salida = gestionar_salida(inventario)
            if registro_salida:
                guardar_en_archivo(registro_salida, 'venta')

        elif opcion == '3':
            mostrar_inventario(inventario)

        elif opcion == '4':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
