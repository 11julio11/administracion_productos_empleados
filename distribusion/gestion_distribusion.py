import os
from ingreso_y_venta.gestion_productos import agregar_al_inventario, mostrar_inventario, crear_producto, gestionar_salida, mostrar_facturas

DISTRIBUSION_DIR = './distribusion/'

if not os.path.exists(DISTRIBUSION_DIR):
    os.makedirs(DISTRIBUSION_DIR)

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
