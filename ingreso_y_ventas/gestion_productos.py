# Importar módulos necesarios
import json  # Manejo de datos JSON
import os  # Interacción con el sistema operativo
import signal  # Manejo de señales del sistema (ej. interrupciones)
from datetime import datetime  # Manejo de fechas y horas


# Definimos las rutas de las carpetas donde se almacenarán las facturas y registros.

FACTURAS_DIR = './facturas/'
DISTRIBUCION_DIR = os.path.join(FACTURAS_DIR, 'distribucion/')
VENTA_CIUDAD_DIR = os.path.join(FACTURAS_DIR, 'venta_ciudad/')
INGRESO_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_ingreso/')
VENTA_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_venta/')
GASTOS_FACTURAS_DIR = os.path.join(FACTURAS_DIR, 'facturas_gastos/')
INVENTARIO_FILE = 'inventario.json'

EMPLOYEES_DIR = './employees/'  # Carpeta principal para empleados.
REGISTRO_EMPLOYEES_DIR = os.path.join(EMPLOYEES_DIR, 'registro_employees/')
EMPLOYEES_FILE = 'employees_data.json'  # Archivo para guardar los datos de empleados.

# ---------------------------------- Gestión de Productos ----------------------------------
class Producto:
    def __init__(self, nombre, precio, cantidad, descuento, fecha_de_compra=None, total=None, cantidad_vendida=0, ventas=None):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.fecha_de_compra = fecha_de_compra if fecha_de_compra else self.obtener_fecha_actual()
        self.total = total if total else self.calcular_total()
        self.cantidad_vendida = cantidad_vendida
        self.ventas = ventas if ventas else []

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def calcular_total(self):
        if self.descuento < 0 or self.descuento > 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")
        return self.precio * self.cantidad * (1 - self.descuento / 100)

    def imprimir_factura_ingreso(self):
        return (
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

    def imprimir_factura_venta(self, cantidad_vendida, ciudad_destino, nombre_local):
        total_venta = self.precio * cantidad_vendida * (1 - self.descuento / 100)
        self.cantidad_vendida += cantidad_vendida
        self.cantidad -= cantidad_vendida
        venta = {
            'cantidad': cantidad_vendida,
            'ciudad': ciudad_destino,
            'local': nombre_local,
            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        self.ventas.append(venta)
        return (
            f"\n{'=' * 50}\n"
            f"            FACTURA DE VENTA    \n"
            f"{'=' * 50}\n"
            f"Fecha de venta: {venta['fecha']}\n"
            f"Producto: {self.nombre}\n"
            f"Cantidad vendida: {cantidad_vendida}\n"
            f"Precio unitario: ${self.precio:.2f}\n"
            f"Descuento: {self.descuento}%\n"
            f"Total a pagar: ${total_venta:.2f}\n"
            f"Ciudad de destino: {ciudad_destino}\n"
            f"Nombre del local: {nombre_local}\n"
            f"{'=' * 50}\n"
        )

    def mostrar_inventario(self):
        return (
            f"Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | "
            f"Cantidad: {self.cantidad} | "
            f"Descuento: {self.descuento}% | "
            f"Cantidad Vendida: {self.cantidad_vendida}\n"
        )


# ---------------------------------- Gestión de Gastos ----------------------------------
class Gasto:
    def __init__(self, descripcion, monto, ciudad, local):
        self.descripcion = descripcion
        self.monto = monto
        self.ciudad = ciudad
        self.local = local
        self.fecha_de_gasto = self.obtener_fecha_actual()

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def imprimir_factura_gasto(self):
        return (
            f"\n{'=' * 50}\n"
            f"            FACTURA DE GASTO    \n"
            f"{'=' * 50}\n"
            f"Fecha de gasto: {self.fecha_de_gasto}\n"
            f"Descripción: {self.descripcion}\n"
            f"Monto: ${self.monto:.2f}\n"
            f"Ciudad: {self.ciudad}\n"
            f"Local: {self.local}\n"
            f"{'=' * 50}\n"
        )


# ---------------------------------- Gestión de Empleados ----------------------------------

class Empleado:
    def __init__(self, nombre, apellido, edad, telefono, correo, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.fecha_ingreso = datetime.now().strftime("%d/%m/%Y")
        self.turnos = []

    def iniciar_turno(self):
        inicio_turno = datetime.now()
        self.turnos.append({'inicio': inicio_turno, 'fin': None})
        print(f"Turno iniciado para {self.nombre} {self.apellido} a las {inicio_turno.strftime('%H:%M:%S')}")

    def terminar_turno(self):
        if self.turnos and self.turnos[-1]['fin'] is None:
            fin_turno = datetime.now()
            self.turnos[-1]['fin'] = fin_turno
            duracion = fin_turno - self.turnos[-1]['inicio']
            print(f"Turno terminado para {self.nombre} {self.apellido} a las {fin_turno.strftime('%H:%M:%S')}")
            print(f"Duración del turno: {duracion}")
        else:
            print("No hay un turno iniciado o ya ha sido finalizado.")

    def mostrar_informe(self):
        informe = (
            f"\n{'='*50}\n"
            f"INFORME DEL EMPLEADO: {self.nombre} {self.apellido}\n"
            f"{'='*50}\n"
            f"Edad: {self.edad}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo}\n"
            f"Dirección: {self.direccion}\n"
            f"Fecha de ingreso: {self.fecha_ingreso}\n"
        )
        for idx, turno in enumerate(self.turnos, 1):
            inicio = turno['inicio'].strftime('%d/%m/%Y %H:%M:%S')
            fin = turno['fin'].strftime('%d/%m/%Y %H:%M:%S') if turno['fin'] else 'En curso'
            informe += f"Turno {idx}: Inicio: {inicio} | Fin: {fin}\n"
        return informe

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'fecha_ingreso': self.fecha_ingreso,
            'turnos': [
                {
                    'inicio': turno['inicio'].strftime('%Y-%m-%d %H:%M:%S'),
                    'fin': turno['fin'].strftime('%Y-%m-%d %H:%M:%S') if turno['fin'] else None
                }
                for turno in self.turnos
            ]
        }

    @staticmethod
    def from_dict(data):
        empleado = Empleado(
            nombre=data['nombre'],
            apellido=data['apellido'],
            edad=data['edad'],
            telefono=data['telefono'],
            correo=data['correo'],
            direccion=data['direccion']
        )
        empleado.fecha_ingreso = data['fecha_ingreso']
        for turno in data['turnos']:
            turno_data = {
                'inicio': datetime.strptime(turno['inicio'], '%Y-%m-%d %H:%M:%S'),
                'fin': datetime.strptime(turno['fin'], '%Y-%m-%d %H:%M:%S') if turno['fin'] else None
            }
            empleado.turnos.append(turno_data)
        return empleado


# ---------------------------------- Funciones Generales ----------------------------------

def crear_carpetas():
    for directory in [
        FACTURAS_DIR, DISTRIBUCION_DIR, VENTA_CIUDAD_DIR,
        INGRESO_FACTURAS_DIR, VENTA_FACTURAS_DIR, GASTOS_FACTURAS_DIR,
        EMPLOYEES_DIR, REGISTRO_EMPLOYEES_DIR
    ]:
        os.makedirs(directory, exist_ok=True)

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump({k: v.__dict__ for k, v in inventario.items()}, f)

def cargar_inventario():
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, 'r') as f:
            inventario_data = json.load(f)
            return {nombre: Producto(**data) for nombre, data in inventario_data.items()}
    return {}

def guardar_factura(registro, tipo):
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


def guardar_venta_ciudad(producto):
    archivo_ciudad = os.path.join(VENTA_CIUDAD_DIR, 'venta_ciudad.txt')
    with open(archivo_ciudad, 'a') as f:
        for venta in producto.ventas:
            f.write(f"Producto: {producto.nombre} | Cantidad: {venta['cantidad']} | Ciudad: {venta['ciudad']} | Local: {venta['local']} | Fecha: {venta['fecha']}\n")

def actualizar_distribucion(inventario):
    resumen_file = os.path.join(DISTRIBUCION_DIR, 'resumen_distribucion.txt')
    with open(resumen_file, 'w') as f:
        for nombre, producto in inventario.items():
            f.write(f"Producto: {nombre} | Cantidad vendida: {producto.cantidad_vendida} | Stock: {producto.cantidad}\n")
            for venta in producto.ventas:
                f.write(f"Ciudad: {venta['ciudad']} | Local: {venta['local']} | Producto: {nombre} | Cantidad: {venta['cantidad']} | Fecha: {venta['fecha']}\n")

def manejar_salida(signal_num, frame):
    print("\nSaliendo del programa. ¡Hasta luego!")
    exit(0)

signal.signal(signal.SIGINT, manejar_salida)

# ---------------------------------- Gestión de Empleados ----------------------------------

def cargar_empleados():
    if os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, 'r') as f:
            empleados_data = json.load(f)
            return [Empleado.from_dict(data) for data in empleados_data]
    return []

def guardar_empleados(empleados):
    with open(EMPLOYEES_FILE, 'w') as f:
        json.dump([emp.to_dict() for emp in empleados], f)

def buscar_empleado(empleados, nombre_buscar):
    nombre_buscar = nombre_buscar.strip().lower()
    for empleado in empleados:
        if empleado.nombre.strip().lower() == nombre_buscar:
            return empleado
    return None

def registrar_empleado(empleados):
    nombre = input("Ingrese el nombre del empleado: ")
    apellido = input("Ingrese el apellido del empleado: ")
    edad = input("Ingrese la edad del empleado: ")
    telefono = input("Ingrese el teléfono del empleado: ")
    correo = input("Ingrese el correo electrónico del empleado: ")
    direccion = input("Ingrese la dirección del empleado: ")
    
    empleado = Empleado(nombre, apellido, edad, telefono, correo, direccion)
    
    # Crear la carpeta individual del empleado
    empleado_dir = os.path.join(REGISTRO_EMPLOYEES_DIR, f"{nombre}_{apellido}/")
    os.makedirs(empleado_dir, exist_ok=True)

    # Guardar la información del empleado en un archivo
    info_file = os.path.join(empleado_dir, 'informacion_empleado.txt')
    with open(info_file, 'w') as f:
        f.write(f"Nombre: {nombre}\nApellido: {apellido}\nEdad: {edad}\nTeléfono: {telefono}\nCorreo: {correo}\nDirección: {direccion}\n")

    empleados.append(empleado)
    guardar_empleados(empleados)
    print(f"Empleado {nombre} {apellido} registrado correctamente en {empleado_dir}.")



def iniciar_turno(empleados):
    nombre = input("Ingrese el nombre del empleado para iniciar turno: ").strip().lower()
    empleado = buscar_empleado(empleados, nombre)
    if empleado:
        empleado.iniciar_turno()
        empleado_dir = os.path.join(REGISTRO_EMPLOYEES_DIR, f"{empleado.nombre}_{empleado.apellido}/")
        turnos_file = os.path.join(empleado_dir, 'turnos.txt')
        
        # Guardar los turnos en la carpeta del empleado
        with open(turnos_file, 'a') as f:
            f.write(f"Inicio del turno: {empleado.turnos[-1]['inicio']}\n")
        
        guardar_empleados(empleados)
    else:
        print(f"No se encontró ningún empleado con el nombre {nombre}.")



def terminar_turno(empleados):
    nombre = input("Ingrese el nombre del empleado para terminar turno: ").strip().lower()
    empleado = buscar_empleado(empleados, nombre)
    if empleado:
        empleado.terminar_turno()
        guardar_empleados(empleados)
    else:
        print(f"No se encontró ningún empleado con el nombre {nombre}.")

def mostrar_informe_empleado(empleados):
    nombre = input("Ingrese el nombre del empleado para ver el informe: ").strip().lower()
    empleado = buscar_empleado(empleados, nombre)
    if empleado:
        informe = empleado.mostrar_informe()
        empleado_dir = os.path.join(REGISTRO_EMPLOYEES_DIR, f"{empleado.nombre}_{empleado.apellido}/")
        informe_file = os.path.join(empleado_dir, 'informe.txt')
        
        with open(informe_file, 'w') as f:
            f.write(informe)
        
        print(informe)
    else:
        print(f"No se encontró ningún empleado con el nombre {nombre}.")



def listar_empleados(empleados):
    if empleados:
        print("Empleados registrados:")
        for emp in empleados:
            print(f"{emp.nombre} {emp.apellido}")
    else:
        print("No hay empleados registrados.")

def gestionar_empleados(empleados):
    while True:
        print("\nGestión de Empleados:")
        print("1. Registrar nuevo empleado")
        print("2. Iniciar turno")
        print("3. Terminar turno")
        print("4. Mostrar informe de empleado")
        print("5. Listar empleados")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_empleado(empleados)
        elif opcion == '2':
            iniciar_turno(empleados)
        elif opcion == '3':
            terminar_turno(empleados)
        elif opcion == '4':
            mostrar_informe_empleado(empleados)
        elif opcion == '5':
            listar_empleados(empleados)
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# ---------------------------------- Menú Principal ----------------------------------

def main():
    crear_carpetas()
    inventario = cargar_inventario()
    empleados = cargar_empleados()

    while True:
        print("\nBienvenido, por favor ingrese una opción:")
        print("-------------------------------------------")
        print("1. Ingresar producto")
        print("2. Vender producto")
        print("3. Registrar gasto")
        print("4. Mostrar facturas")
        print("5. Mostrar inventario")
        print("6. Actualizar distribución")
        print("7. Gestionar empleados")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            cantidad = int(input("Ingrese la cantidad del producto: "))
            descuento = float(input("Ingrese el descuento (%): "))
            producto = Producto(nombre, precio, cantidad, descuento)
            inventario[nombre] = producto
            guardar_inventario(inventario)
            factura = producto.imprimir_factura_ingreso()
            guardar_factura(factura, 'ingreso')
            print(factura)

        elif opcion == '2':
            nombre = input("Ingrese el nombre del producto a vender: ")
            if nombre in inventario:
                cantidad_vendida = int(input("Ingrese la cantidad a vender: "))
                if cantidad_vendida > inventario[nombre].cantidad:
                    print("No hay suficiente stock para realizar la venta.")
                    continue
                ciudad_destino = input("Ingrese la ciudad de destino: ")
                nombre_local = input("Ingrese el nombre del local: ")
                factura_venta = inventario[nombre].imprimir_factura_venta(cantidad_vendida, ciudad_destino, nombre_local)
                guardar_factura(factura_venta, 'venta')
                guardar_venta_ciudad(inventario[nombre])
                actualizar_distribucion(inventario)
                guardar_inventario(inventario)
                print(factura_venta)
            else:
                print("Producto no encontrado en el inventario.")

        elif opcion == '3':
            descripcion = input("Ingrese la descripción del gasto: ")
            monto = float(input("Ingrese el monto del gasto: "))
            ciudad = input("Ingrese la ciudad: ")
            local = input("Ingrese el nombre del local: ")
            gasto = Gasto(descripcion, monto, ciudad, local)
            factura_gasto = gasto.imprimir_factura_gasto()
            guardar_factura(factura_gasto, 'gasto')
            print(factura_gasto)

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
                print(producto.mostrar_inventario())

        elif opcion == '6':
            actualizar_distribucion(inventario)
            print("Distribución actualizada.")

        elif opcion == '7':
            gestionar_empleados(empleados)
            guardar_empleados(empleados)

        elif opcion == '8':
            print("Saliendo del programa.")
            guardar_inventario(inventario)
            guardar_empleados(empleados)
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    main()