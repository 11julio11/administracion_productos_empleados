# Sistema de Gestión de Productos

Este proyecto es un sistema de gestión para manejar productos, incluyendo la adición de nuevos productos, venta de productos, y la generación de facturas de ingreso y venta. También se actualiza un archivo de distribución con la información relevante sobre el inventario.

## Funcionalidades

- **Agregar Producto**: Permite ingresar un nuevo producto con su nombre, precio, cantidad y descuento. Se genera una factura de ingreso para el producto.
- **Vender Producto**: Facilita la venta de productos del inventario, genera una factura de venta y actualiza la cantidad disponible en el inventario.
- **Mostrar Inventario**: Muestra una lista de todos los productos en el inventario con su cantidad, precio y descuento.
- **Actualizar Distribución**: Genera un archivo `resumen_distribusion.txt` con el resumen del inventario, incluyendo la cantidad disponible y los productos vendidos.
- **Mostrar Facturas**: Permite ver las facturas de ingreso y venta.

## Cambios Realizados

- **Actualización de la Clase `Producto`**: Ahora incluye una propiedad `cantidad_vendida` para registrar la cantidad de productos vendidos.
- **Actualización de la Función `imprimir_factura_venta`**: Se actualiza la propiedad `cantidad_vendida` cuando se realiza una venta.
- **Modificación de la Función `actualizar_distribusion`**: Se añadió una columna para mostrar la cantidad de productos vendidos en el archivo `resumen_distribusion.txt`.




