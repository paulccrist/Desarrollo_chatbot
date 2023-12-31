import mysql.connector
from mysql.connector import Error
import getpass  # Para ocultar la contraseña al ingresarla

class CrudApp:
    def __init__(self):
        # Conexión a la base de datos MySQL
        self.connection = self.connect_to_database()

    def connect_to_database(self):#Para conectar a la base de datos MYSQL
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='app_ia',
                user='root',
                password='123456'
        )
            if connection.is_connected():
                print("Conectado a la base de datos")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):#Cierra la conexion a la base de datos
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")
            
    def obtener_usuario_por_correo(self, correo):#Obtiene la informacion de un usuario por su direccion de correo electronico
        try:
            cursor = self.connection.cursor()
            sql_select = "SELECT * FROM usuarios WHERE correo = %s"
            cursor.execute(sql_select, (correo,))
            user_data = cursor.fetchone()
            return user_data
        except Error as e:
            print(f"Error al obtener información del usuario: {e}")
            return None
            
            
            
#===============================================================================================================================================================================
                                                                #REALIZANDO UN CRUD => CREATE READ UPDATE DELETE
#===============================================================================================================================================================================
    
    
    
    # Crear un nuevo usuario en la base de datos
    def insertar(self, nombres, apellidos, correo, contrasena):
        try:
            cursor = self.connection.cursor()
            sql_insert = "INSERT INTO usuarios (nombres, apellidos, correo, contraseña) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert, (nombres, apellidos, correo, contrasena))
            self.connection.commit()
            print("Usuario creado...")
        except Error as e:
            print(f"Error al crear: {e}")



    # Mostrar todos los usuarios en la base de datos
    def seleccionar(self):
        try:
            cursor = self.connection.cursor()
            sql_select = "SELECT * FROM usuarios"
            cursor.execute(sql_select)
            records = cursor.fetchall()

            for row in records:
                print(f"ID = {row[0]}, Nombres = {row[1]}, Apellidos = {row[2]}, Correo = {row[3]}, Contraseña = {row[4]}\n")
        except Error as e:
            print(f"Error al mostrar: {e}")



    # Actualizar usuarios
    def actualizar(self):
        idusuario = input("Ingrese el ID del usuario para actualizar: ")
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM usuarios WHERE idusuarios = {idusuario}")
            user_data = cursor.fetchone()

            if user_data:
                nuevos_nombres = input("Actualice Nombres: ")
                nuevos_apellidos = input("Actualice Apellidos: ")
                nuevo_correo = input("Actualice Correo: ")
                nueva_contrasena = input("Actualice Contraseña: ")

                sql_update = "UPDATE usuarios SET nombres = %s, apellidos = %s, correo = %s, contraseña = %s  WHERE idusuarios = %s"
                cursor.execute(sql_update, (nuevos_nombres, nuevos_apellidos, nuevo_correo, nueva_contrasena, idusuario))
                self.connection.commit()
                print("Se actualizó con éxito.")
            else:
                print(f"No se encontró ningún usuario con ID {idusuario}")
        except Error as e:
            print(f"Error al actualizar: {e}")



    # Eliminar usuario por ID
    def eliminar(self):
        id_usuario = input("Ingrese el ID del usuario que desea eliminar: ")
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM usuarios WHERE idusuarios = {id_usuario}")
            user_data = cursor.fetchone()
            
            if user_data:
                sql_delete = "DELETE FROM usuarios WHERE idusuarios = %s"
                cursor.execute(sql_delete, (id_usuario,))
                self.connection.commit()
                print("Usuario eliminado.")
            else:
                print(f"No se encontró ningún usuario con ID {id_usuario}")
        except Error as e:
            print(f"Error al eliminar: {e}")

if __name__ == "__main__":
    app = CrudApp()

    while True:
        print("\nMenu:")
        print("1. Insertar")
        print("2. Seleccionar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("5. Salir")

        choice = input("Ingrese el número de la opción que desea: ")

        if choice == "1":
            nombres = input("Ingrese nombres: ")
            apellidos = input("Ingrese apellidos: ")
            correo = input("Ingrese correo: ")
            contrasena = input("Ingrese contraseña: ")
            
            app.insertar(nombres, apellidos, correo, contrasena)
        elif choice == "2":
            app.seleccionar()
        elif choice == "3":
            app.actualizar()
        elif choice == "4":
            app.eliminar()
        elif choice == "5":
            app.close_connection()
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")