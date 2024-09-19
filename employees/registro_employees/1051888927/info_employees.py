import os

# Este archivo puede ser utilizado para manejar la información adicional de los empleados
def agregar_info_empleado(nombre, apellido, edad, telefono, correo, direccion, id_empleado):
    directorio_empleado = f'./employees/registro_employees/{id_empleado}/'
    
    if not os.path.exists(directorio_empleado):
        os.makedirs(directorio_empleado)
    
    info_archivo = os.path.join(directorio_empleado, 'info.txt')
    with open(info_archivo, 'w') as f:
        f.write(f"Nombre: {nombre}\n")
        f.write(f"Apellido: {apellido}\n")
        f.write(f"Edad: {edad}\n")
        f.write(f"Teléfono: {telefono}\n")
        f.write(f"Correo: {correo}\n")
        f.write(f"Dirección: {direccion}\n")
