import tkinter as tk
from tkinter import scrolledtext
import mysql.connector
from datetime import datetime  # Importa el módulo datetime para manejar fechas

class ChatWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.title("ChatBot")
        self.configure(bg="#E6E6E6")
        self.geometry("400x480")
        self.main_window = main_window

        # Agrega la conexión a la base de datos
        self.db_connection = mysql.connector.connect(
            host='localhost',
            database='app_ia',
            user='root',
            password='123456'
        )

        self.create_widgets()

    def create_widgets(self):
        # Botón cerrar
        logout_button = tk.Button(self, text="Cerrar Sesion", command=self.open_login_window, font=("Arial", 12))
        logout_button.configure(bg="#79fcf0", fg="black")
        logout_button.pack(side=tk.BOTTOM, pady=10)

        # ScrolledText para mostrar el chat
        self.chat_display = scrolledtext.ScrolledText(self, width=50, height=20, font=("Arial", 12))
        self.chat_display.configure(bg="white")
        self.chat_display.pack()

        # Entry para el mensaje del usuario
        self.user_message = tk.Entry(self, width=40, font=("Arial", 12))
        self.user_message.configure(bg="white")
        self.user_message.pack()

        # Botón enviar
        send_button = tk.Button(self, text="Enviar", command=self.send_message, font=("Arial", 12))
        send_button.configure(bg="#79fcf0", fg="black")
        send_button.pack()

        self.display_message("ChatBot: ¡Bienvenido al chatBot!")

    def open_login_window(self):
        self.db_connection.close()  # Cierra la conexión al cerrar la ventana
        self.destroy()
        self.main_window.deiconify()

    def send_message(self): #Obtiene el mensaje del usuario, lo muestra en la interfaz
        user_input = self.user_message.get()
        self.display_message("Tu: " + user_input, "#E6E6E6")
        self.handle_user_message(user_input)
        self.user_message.delete(0, tk.END)

    def display_message(self, message, background_color="white"):
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.tag_configure("custom", background=background_color)
        self.chat_display.tag_add("custom", self.chat_display.index(tk.INSERT))

    def handle_user_message(self, user_input):#Procesa el mensaje del usuario, realiza una consulta a la base de datos y muesta la respuesta
        cleaned_input = user_input.lower().strip()

        try:
            cursor = self.db_connection.cursor()

            query = "SELECT respuesta FROM conversacion WHERE pregunta = %s"
            cursor.execute(query, (cleaned_input,))
            result = cursor.fetchone()

            if result:
                response = result[0]
                self.display_message("ChatBot: " + response)

                # Almacena la interacción en la base de datos
                self.store_interaction(user_input, response)

            else:
                self.display_message("ChatBot: No estoy seguro de lo que quieres, disculpa, ¿puedes intentarlo de nuevo?")

        except mysql.connector.Error as e:
            self.display_message("ChatBot: Ocurrió un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde.")

        finally:
            cursor.close()

    def store_interaction(self, user_message, bot_message):#Almacena la interaccion con el chatBot(mensaje usuario, mensaje bot y fecha)
        try:
            cursor = self.db_connection.cursor()

            # Inserta la interacción en la tabla historial
            query = "INSERT INTO historial (mensaje_usuario, mensaje_bot, fecha) VALUES (%s, %s, %s)"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query, (user_message, bot_message, current_time))

            self.db_connection.commit()

        except mysql.connector.Error as e:
            print("Error al almacenar la interacción en la base de datos:", e)

        finally:
            cursor.close()

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.withdraw()  # Oculta la ventana principal al inicio
    chat_window = ChatWindow(main_window)
    chat_window.mainloop()