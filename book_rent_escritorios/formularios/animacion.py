import tkinter as tk
import math

class Hexagon:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_width = 900  # Ancho del canvas
        self.canvas_height = 700  # Alto del canvas
        self.hexagon_coords = [
            (self.canvas_width / 2 + 100 * math.cos(math.radians(angle)), 
             self.canvas_height / 2 + 100 * math.sin(math.radians(angle)))
            for angle in [30, 90, 150, 210, 270, 330]
        ]
        self.current_line = 0  # Línea actual que se está dibujando
        self.total_lines = len(self.hexagon_coords)  # Total de líneas del hexágono
        self.draw_lines()

    def draw_lines(self):
        if self.current_line < self.total_lines:
            next_index = (self.current_line + 1) % self.total_lines
            self.canvas.create_line(self.hexagon_coords[self.current_line], 
                                    self.hexagon_coords[next_index], 
                                    fill="#FFFFFF", 
                                    width=5)
            self.current_line += 1
            self.canvas.after(1000, self.draw_lines)
        else:
            self.canvas.after(500, self.draw_cross_line)
            self.canvas.after(1000, self.draw_line_to_center)

    def draw_cross_line(self):
        lower_left_vertex = self.hexagon_coords[3]
        upper_left_vertex = self.hexagon_coords[0]
        self.canvas.create_line(lower_left_vertex, upper_left_vertex, fill="#FFFFFF", width=5)

    def draw_line_to_center(self):
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        lower_right_vertex = self.hexagon_coords[5]
        self.canvas.create_line(lower_right_vertex, (center_x, center_y), fill="#FFFFFF", width=5)
        self.show_welcome_message()

    def show_welcome_message(self):
        right_of_hexagon_x = self.hexagon_coords[5][0] + 300
        center_y = self.canvas_height / 2
        font_size = int(self.canvas_width / 20)
        self.canvas.create_text(right_of_hexagon_x, center_y, text="Book&Rent", fill="#FFFFFF", font=("Arial", font_size))
        self.canvas.after(2000, self.canvas.destroy)


def mostrar_animacion_hexagono(parent):
    parent.canvas_animacion = tk.Canvas(parent, width=1024, height=600, bg="#1f2329")
    parent.canvas_animacion.place(x=0, y=0, relwidth=1, relheight=1)
    hexagon = Hexagon(parent.canvas_animacion)
