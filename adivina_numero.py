
import random
import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import json
import time

class AdivinaElNumero:
    def __init__(self, master):
        self.master = master
        self.master.title("Adivina el Número")
        self.master.configure(bg="#282c34")
        
        self.nombre = None
        self.numero_secreto = None
        self.nivel = None
        self.max_intentos = None

        self.high_scores = self.load_high_scores()
        self.create_widgets()

    def create_widgets(self):
        self.clear_window()
        self.label_home = tk.Label(self.master, text="Bienvenido al Juego", fg="#61dafb", bg="#282c34", font=("Helvetica", 16))
        self.label_home.pack(pady=10)

        self.boton_nuevo_juego = tk.Button(self.master, text="Nuevo Juego", command=self.pedir_nombre, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_nuevo_juego.pack(pady=5)

        self.boton_records = tk.Button(self.master, text="Lista de Records", command=self.mostrar_records, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_records.pack(pady=5)

        self.boton_perfiles = tk.Button(self.master, text="Perfiles", command=self.mostrar_perfiles, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_perfiles.pack(pady=5)

    def mostrar_perfil(self, nombre):
        self.clear_window()
        perfil_encontrado = False

        for score in self.high_scores:
            if score['nombre'] == nombre:
                perfil_encontrado = True
                tk.Label(self.master, text=f"Perfil de {nombre}", fg="#61dafb", bg="#282c34", font=("Helvetica", 16)).pack(pady=10)
                
                logros = self.obtener_logros(score)
                if logros:
                    tk.Label(self.master, text="Logros:", fg="#61dafb", bg="#282c34", font=("Helvetica", 14)).pack()
                    for logro in logros:
                        tk.Label(self.master, text=logro, fg="#61dafb", bg="#282c34", font=("Helvetica", 12)).pack()
                else:
                    tk.Label(self.master, text="Este jugador no tiene logros.", fg="#61dafb", bg="#282c34", font=("Helvetica", 14)).pack()

                break
        
        if not perfil_encontrado:
            tk.Label(self.master, text="Perfil no encontrado.", fg="#61dafb", bg="#282c34", font=("Helvetica", 14)).pack()

        self.boton_volver_perfil = tk.Button(self.master, text="Volver", command=self.mostrar_perfiles, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_volver_perfil.pack(pady=10)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def mostrar_perfiles(self):
        self.clear_window()
        self.label_perfiles = tk.Label(self.master, text="Lista de Perfiles", fg="#61dafb", bg="#282c34", font=("Helvetica", 16))
        self.label_perfiles.pack(pady=10)

        perfiles_frame = tk.Frame(self.master, bg="#282c34")
        perfiles_frame.pack(pady=10)

        if not self.high_scores:
            tk.Label(perfiles_frame, text="No hay perfiles aún.", fg="#61dafb", bg="#282c34", font=("Helvetica", 14)).pack()
        else:
            nombres_perfiles = set()  # Usar un conjunto para evitar perfiles duplicados
            for score in self.high_scores:
                nombre = score['nombre']
                if nombre not in nombres_perfiles:
                    nombres_perfiles.add(nombre)
                    tk.Button(perfiles_frame, text=nombre, command=lambda n=nombre: self.mostrar_perfil(n), bg="#61dafb", fg="#282c34", font=("Helvetica", 12)).pack(pady=5)

        self.boton_volver_perfiles = tk.Button(self.master, text="Volver", command=self.create_widgets, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_volver_perfiles.pack(pady=10)


    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def obtener_logros(self, score):
        logros = []
        if score['nivel'] == 1000 and score['intentos'] == 1:
            logros.append("Logro desbloqueado: 'Genio de la adivinanza' - Adivinaste el número en Hardcore.")
        if score['nivel'] == 200 and score['intentos'] <= 3:
            logros.append("Logro desbloqueado: 'Pro' - Adivinaste en los primeros 3 intentos en la dificultad difícil.")
        if score['nivel'] == 100 and score['intentos'] <= 5:
            logros.append("Logro desbloqueado: 'Avances de a poco' - Adivinaste en 5 intentos en la dificultad medio.")
        return logros

    def pedir_nombre(self):
        self.clear_window()
        self.label_nombre = tk.Label(self.master, text="Introduce tu nombre:", fg="#61dafb", bg="#282c34", font=("Helvetica", 14))
        self.label_nombre.pack(pady=10)

        self.entry_nombre = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry_nombre.pack(pady=5)

        self.boton_nombre = tk.Button(self.master, text="Confirmar", command=self.validar_nombre, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_nombre.pack(pady=10)

    def validar_nombre(self):
        self.nombre = self.entry_nombre.get()
        if self.nombre:
            if self.existe_usuario(self.nombre):
                self.mostrar_opcion_continuar()
            else:
                self.seleccionar_nivel()

    def existe_usuario(self, nombre):
        return any(score['nombre'] == nombre for score in self.high_scores)

    def mostrar_opcion_continuar(self):
        self.clear_window()
        self.label_continuar = tk.Label(self.master, text=f"Bienvenido de vuelta, {self.nombre}!", fg="#61dafb", bg="#282c34", font=("Helvetica", 14))
        self.label_continuar.pack(pady=10)

        self.boton_continuar = tk.Button(self.master, text="Continuar este perfil", command=self.seleccionar_nivel, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_continuar.pack(pady=5)

        self.boton_nuevo_usuario = tk.Button(self.master, text="Usuario Nuevo", command=self.pedir_nombre, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_nuevo_usuario.pack(pady=5)

        self.boton_volver_home = tk.Button(self.master, text="Volver al inicio", command=self.create_widgets, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_volver_home.pack(pady=5)


    def seleccionar_nivel(self):
        self.clear_window()
        self.label_nivel = tk.Label(self.master, text="Elige el nivel:", fg="#61dafb", bg="#282c34", font=("Helvetica", 14))
        self.label_nivel.pack(pady=10)

        self.nivel_frame = tk.Frame(self.master, bg="#282c34")
        self.nivel_frame.pack(pady=5)

        self.boton_facil = tk.Button(self.nivel_frame, text="Fácil", command=lambda: self.iniciar_juego(50, None), bg="#61dafb", fg="#282c34", font=("Helvetica", 12), width=10)
        self.boton_facil.grid(row=0, column=0, padx=5)

        self.boton_medio = tk.Button(self.nivel_frame, text="Medio", command=lambda: self.iniciar_juego(100, 10), bg="#61dafb", fg="#282c34", font=("Helvetica", 12), width=10)
        self.boton_medio.grid(row=0, column=1, padx=5)

        self.boton_dificil = tk.Button(self.nivel_frame, text="Difícil", command=lambda: self.iniciar_juego(200, 5), bg="#61dafb", fg="#282c34", font=("Helvetica", 12), width=10)
        self.boton_dificil.grid(row=0, column=2, padx=5)

        self.boton_hardcore = tk.Button(self.nivel_frame, text="Hardcore", command=lambda: self.iniciar_juego(1000, 1), bg="#61dafb", fg="#282c34", font=("Helvetica", 12), width=10)
        self.boton_hardcore.grid(row=0, column=3, padx=5)

        self.boton_personalizado = tk.Button(self.nivel_frame, text="Personalizado", command=self.nivel_personalizado, bg="#61dafb", fg="#282c34", font=("Helvetica", 12), width=10)
        self.boton_personalizado.grid(row=0, column=4, padx=5)

    def nivel_personalizado(self):
        self.clear_window()
        self.label_personalizado = tk.Label(self.master, text="Configuración Personalizada", fg="#61dafb", bg="#282c34", font=("Helvetica", 14))
        self.label_personalizado.pack(pady=10)

        self.rango_frame = tk.Frame(self.master, bg="#282c34")
        self.rango_frame.pack(pady=5)

        tk.Label(self.rango_frame, text="Mínimo:", fg="#61dafb", bg="#282c34", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.minimo_entry = tk.Entry(self.rango_frame, font=("Helvetica", 12))
        self.minimo_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.rango_frame, text="Máximo:", fg="#61dafb", bg="#282c34", font=("Helvetica", 12)).grid(row=1, column=0, padx=5)
        self.maximo_entry = tk.Entry(self.rango_frame, font=("Helvetica", 12))
        self.maximo_entry.grid(row=1, column=1, padx=5)

        self.boton_confirmar = tk.Button(self.master, text="Confirmar", command=self.iniciar_personalizado, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_confirmar.pack(pady=10)

    def iniciar_personalizado(self):
        try:
            minimo = int(self.minimo_entry.get())
            maximo = int(self.maximo_entry.get())
        except ValueError:
            messagebox.showinfo("Error", "Por favor, ingresa números válidos para el rango.")
            return

        if minimo >= maximo:
            messagebox.showinfo("Error", "El número mínimo debe ser menor que el máximo.")
            return

        self.iniciar_juego(maximo, None)

    def iniciar_juego(self, nivel, max_intentos):
        self.nivel = nivel
        self.max_intentos = max_intentos
        self.numero_secreto = random.randint(1, self.nivel)
        self.intentos = 0
        self.configurar_juego()

    def configurar_juego(self):
        self.clear_window()
        self.label = tk.Label(self.master, text=f"Adivina un número entre 1 y {self.nivel}", fg="#61dafb", bg="#282c34", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.label_intentos = tk.Label(self.master, text=f"Intentos restantes: {self.max_intentos if self.max_intentos else '∞'}", fg="#61dafb", bg="#282c34", font=("Helvetica", 12))
        self.label_intentos.pack(pady=5)

        self.entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry.pack(pady=5)

        self.boton = tk.Button(self.master, text="Adivinar", command=self.adivinar, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton.pack(pady=10)
        self.boton.bind("<Enter>", self.on_enter)
        self.boton.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget['background'] = '#005f87'

    def on_leave(self, event):
        event.widget['background'] = '#61dafb'

    def adivinar(self):
        try:
            intento = int(self.entry.get())
        except ValueError:
            messagebox.showinfo("Error", "Por favor, ingresa un número válido.")
            return

        self.intentos += 1
        intentos_restantes = self.max_intentos - self.intentos if self.max_intentos else "∞"
        self.label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")

        if intento == self.numero_secreto:
            self.guardar_puntuacion(self.intentos, self.nivel)
            self.mostrar_mensaje_felicitacion()
        else:
            if self.max_intentos and self.intentos >= self.max_intentos:
                messagebox.showinfo("Fin del juego", f"No lo lograste :(. El número era {self.numero_secreto}.")
                self.create_widgets()
            else:
                mensaje = self.generar_mensaje(abs(intento - self.numero_secreto), intento)
                messagebox.showinfo("Resultado", mensaje)


    def generar_mensaje(self, distancia, intento):
        if distancia <= 5:
            mensaje = f"¡Estás muy cerca! Sigue intentándolo."
        elif distancia <= 10:
            mensaje = f"¡Estás cerca! Sigue intentándolo."
        else:
            mensaje = f"Estás lejos. Sigue intentándolo."
        
        if intento < self.numero_secreto:
            mensaje += " El número es más alto."
        else:
            mensaje += " El número es más bajo."
        
        return mensaje

    def mostrar_mensaje_felicitacion(self):
        self.animacion_ganador()
        self.master.after(2000, lambda: messagebox.showinfo("¡Felicidades!", f"Felicidades, lo lograste en {self.intentos} intentos!"))
        self.master.after(3000, self.mostrar_opcion_continuar)

    def animacion_ganador(self):
        self.label.config(text="¡GANASTE!", fg="#ffcc00", font=("Helvetica", 36, "bold"))
        self.master.update()
        time.sleep(1)
        self.label.config(text=f"Adivina un número entre 1 y {self.nivel}", fg="#61dafb", font=("Helvetica", 14))
        self.master.update()

    def guardar_puntuacion(self, intentos, nivel):
        # Buscar si ya existe un registro para el usuario actual
        for score in self.high_scores:
            if score['nombre'] == self.nombre and score['nivel'] == nivel:
                # Si ya existe, actualizar solo si el nuevo puntaje es mejor
                if intentos < score['intentos']:
                    score['intentos'] = intentos
                    self.actualizar_high_scores()
                return
        
        # Si no hay registro existente, agregar uno nuevo
        self.high_scores.append({"nombre": self.nombre, "intentos": intentos, "nivel": nivel})
        self.actualizar_high_scores()

    def actualizar_high_scores(self):
        # Ordenar y limitar a los mejores 5 registros por nivel y nombre
        unique_scores = {}
        for score in self.high_scores:
            key = (score['nombre'], score['nivel'])
            if key not in unique_scores:
                unique_scores[key] = score
            else:
                # Actualizar solo si el nuevo puntaje es mejor
                if score['intentos'] < unique_scores[key]['intentos']:
                    unique_scores[key]['intentos'] = score['intentos']

        # Convertir de nuevo a lista y ordenar por puntaje
        self.high_scores = list(unique_scores.values())
        self.high_scores.sort(key=lambda x: x['intentos'])

        # Limitar a los mejores 5 registros
        self.high_scores = self.high_scores[:5]

        # Guardar los registros actualizados
        self.save_high_scores()

    def save_high_scores(self):
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores, file)

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def mostrar_records(self):
        self.clear_window()
        self.label_records = tk.Label(self.master, text="Lista de Records", fg="#61dafb", bg="#282c34", font=("Helvetica", 16))
        self.label_records.pack(pady=10)

        niveles = {50: "Fácil", 100: "Medio", 200: "Difícil", 1000: "Hardcore"}
        record_frame = tk.Frame(self.master, bg="#282c34")
        record_frame.pack(pady=10)

        for nivel_idx, nivel in enumerate(niveles.values()):
            tk.Label(record_frame, text=f"{nivel}", fg="#61dafb", bg="#282c34", font=("Helvetica", 14)).grid(row=0, column=nivel_idx, padx=20)

            # Filtrar los registros por nivel y tomar los mejores 5
            records_nivel = [score for score in self.high_scores if score["nivel"] == list(niveles.keys())[nivel_idx]]
            records_nivel.sort(key=lambda x: x.get('intentos', float('inf')))
            records_nivel = records_nivel[:5]

            for record_idx, record in enumerate(records_nivel):
                tk.Label(record_frame, text=f"{record['nombre']} - {record['intentos']} intentos", fg="#61dafb", bg="#282c34", font=("Helvetica", 12)).grid(row=record_idx + 1, column=nivel_idx, padx=20)

        self.boton_volver = tk.Button(self.master, text="Volver", command=self.create_widgets, bg="#61dafb", fg="#282c34", font=("Helvetica", 12))
        self.boton_volver.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    juego = AdivinaElNumero(root)
    root.mainloop()