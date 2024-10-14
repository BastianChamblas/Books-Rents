import tkinter as tk
import math

class Hexagon:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexagon Example")
        self.root.geometry("400x400")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#1f2329")
        self.canvas.pack()

        # Coordenadas del hexágono orientado con un vértice hacia el sur
        self.hexagon_coords = [
            (200 + 100 * math.cos(math.radians(angle)), 200 + 100 * math.sin(math.radians(angle)))
            for angle in [30, 90, 150, 210, 270, 330]
        ]

        self.current_line = 0  # Línea actual que se está dibujando
        self.total_lines = len(self.hexagon_coords)  # Total de líneas del hexágono
        self.draw_lines()

    def draw_lines(self):
        if self.current_line < self.total_lines:
            next_index = (self.current_line + 1) % self.total_lines
            # Dibuja la línea actual
            self.canvas.create_line(self.hexagon_coords[self.current_line], self.hexagon_coords[next_index], fill="#FFFFFF", width=5)
            self.current_line += 1
            # Llama a esta función nuevamente después de 1000 milisegundos
            self.root.after(1000, self.draw_lines)
        else:
            # Una vez que se completa el hexágono, dibuja las otras líneas con un retraso
            self.root.after(500, self.draw_cross_line)  # Espera 500ms antes de dibujar la línea cruzada
            self.root.after(1000, self.draw_line_to_center)  # Espera 1000ms antes de dibujar la línea al centro

    def draw_cross_line(self):
        # Dibuja una línea desde el vértice inferior izquierdo hasta el vértice superior izquierdo
        lower_left_vertex = self.hexagon_coords[3]  # Vértice en 210 grados (inferior izquierdo)
        upper_left_vertex = self.hexagon_coords[0]   # Vértice en 30 grados (superior izquierdo)
        self.canvas.create_line(lower_left_vertex, upper_left_vertex, fill="#FFFFFF", width=5)  # Línea blanca más gruesa

    def draw_line_to_center(self):
        # Calcular el centro del hexágono
        center_x = 200  # Centro en X
        center_y = 200  # Centro en Y
        
        # Vértice inferior derecho en 330 grados
        lower_right_vertex = self.hexagon_coords[5]  # Vértice en 330 grados
        
        # Dibuja una línea desde el vértice inferior derecho hasta el centro del hexágono
        self.canvas.create_line(lower_right_vertex, (center_x, center_y), fill="#FFFFFF", width=10)  # Línea blanca más gruesa
        
        # Muestra el mensaje de bienvenida
        self.show_welcome_message()

    def show_welcome_message(self):
        # Escribe el mensaje "Bienvenido" en el centro del lienzo
        self.canvas.create_text(200, 350, text="Book&Rent", fill="#FFFFFF", font=("Arial", 24))

if __name__ == "__main__":
    root = tk.Tk()
    app = Hexagon(root)
    root.mainloop()
