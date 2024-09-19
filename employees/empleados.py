from datetime import datetime, timedelta
import os

# Directorio para almacenar información de empleados
EMPLEADOS_DIR = './employees/'
REGISTRO_EMPLEADOS_DIR = os.path.join(EMPLEADOS_DIR, 'registro_employees/')

# Clase Empleado
class Empleado:
    def __init__(self, nombre, id_empleado):
        self.nombre = nombre
        self.id_empleado = id_empleado
        self.hora_entrada = None
        self.hora_salida = None
        self.horas_trabajadas = timedelta(0)
        self.directorio_empleado = os.path.join(REGISTRO_EMPLEADOS_DIR, self.id_empleado)
        self.crear_carpeta_empleado()

    def crear_carpeta_empleado(self):
        if not os.path.exists(self.directorio_empleado):
            os.makedirs(self.directorio_empleado)
            print(f"Carpeta creada para el empleado: {self.nombre} (ID: {self.id_empleado})")

    def registrar_entrada(self):
        self.hora_entrada = datetime.now()
        print(f"{self.nombre} ha registrado su entrada a las {self.hora_entrada.strftime('%H:%M:%S')}")
        archivo_entrada = os.path.join(self.directorio_empleado, 'entrada.txt')
        with open(archivo_entrada, 'a') as f:
            f.write(f"Entrada: {self.hora_entrada.strftime('%d/%m/%Y %H:%M:%S')}\n")

    def registrar_salida(self):
        self.hora_salida = datetime.now()
        print(f"{self.nombre} ha registrado su salida a las {self.hora_salida.strftime('%H:%M:%S')}")
        archivo_salida = os.path.join(self.directorio_empleado, 'salida.txt')
        with open(archivo_salida, 'a') as f:
            f.write(f"Salida: {self.hora_salida.strftime('%d/%m/%Y %H:%M:%S')}\n")
        self.calcular_horas_trabajadas()

    def calcular_horas_trabajadas(self):
        if self.hora_entrada and self.hora_salida:
            horas_del_turno = self.hora_salida - self.hora_entrada
            self.horas_trabajadas += horas_del_turno
            print(f"{self.nombre} ha trabajado {horas_del_turno.total_seconds() / 3600:.2f} horas en este turno.")

    def obtener_informe(self):
        return (
            f"Empleado: {self.nombre} (ID: {self.id_empleado})\n"
            f"Horas trabajadas: {self.horas_trabajadas.total_seconds() / 60:.0f} minutos\n"
            f"{'=' * 50}\n"
        )

def crear_carpeta_empleados():
    if not os.path.exists(EMPLEADOS_DIR):
        os.makedirs(EMPLEADOS_DIR)
    if not os.path.exists(REGISTRO_EMPLEADOS_DIR):
        os.makedirs(REGISTRO_EMPLEADOS_DIR)

def guardar_informe_empleado(empleado):
    archivo_informe = os.path.join(empleado.directorio_empleado, 'informe.txt')
    
    with open(archivo_informe, 'a') as f:
        f.write(empleado.obtener_informe())

# Función para gestionar el ingreso y salida del empleado
def gestionar_empleado():
    print("1. Registrar entrada")
    print("2. Registrar salida")
    opcion = input("Selecciona una opción: ")

    nombre = input("Nombre del empleado: ").strip()
    id_empleado = input("ID del empleado: ").strip()
    empleado = Empleado(nombre, id_empleado)

    if opcion == '1':
        empleado.registrar_entrada()
    elif opcion == '2':
        empleado.registrar_salida()
        guardar_informe_empleado(empleado)
    else:
        print("Opción no válida.")

# Flujo principal para gestionar empleados
def menu_empleados():
    crear_carpeta_empleados()
    while True:
        print("\n--- Menú de Empleados ---")
        print("1. Registrar entrada/salida")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            gestionar_empleado()
        elif opcion == '2':
            print("Saliendo del módulo de empleados...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == '__main__':
    menu_empleados()
