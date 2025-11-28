import tkinter as tk
import random
import os
from PIL import Image, ImageTk

class CellGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра с клетками")
        
        # Размер поля
        self.size = 5
        
        # Создаем поле через случайные клики
        self.grid = self.generate_random_field()
        
        # Загружаем изображение тыквы
        self.pumpkin_image = None
        self.load_pumpkin_image()
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Обновляем отображение
        self.update_display()
    
    def load_pumpkin_image(self):
        """Загружает изображение тыквы, если оно существует"""
        pumpkin_paths = ["pumpkin.png", "pumpkin.jpg", "тыква.png", "тыква.jpg"]
        
        for path in pumpkin_paths:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    # Масштабируем изображение до размера клетки
                    img = img.resize((60, 60), Image.Resampling.LANCZOS)
                    self.pumpkin_image = ImageTk.PhotoImage(img)
                    print(f"Изображение загружено: {path}")
                    return
                except Exception as e:
                    print(f"Ошибка при загрузке {path}: {e}")
        
        print("Изображение тыквы не найдено. Используется цветная заливка.")
        self.pumpkin_image = None
    
    def create_widgets(self):
        """Создает виджеты интерфейса"""
        # Фрейм для поля
        self.grid_frame = tk.Frame(self.root, padx=10, pady=10)
        self.grid_frame.pack()
        
        # Создаем кнопки-клетки
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(
                    self.grid_frame,
                    width=8,
                    height=4,
                    command=lambda r=i, c=j: self.on_cell_click(r, c),
                    relief=tk.RAISED,
                    borderwidth=2
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # Метка статуса
        self.status_label = tk.Label(
            self.root,
            text="Кликните на клетку, чтобы переключить её и соседей",
            font=("Arial", 12),
            pady=10
        )
        self.status_label.pack()
        
        # Кнопка перезапуска
        self.restart_button = tk.Button(
            self.root,
            text="Новая игра",
            command=self.restart_game,
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        self.restart_button.pack(pady=5)
    
    def update_display(self):
        """Обновляет визуальное отображение поля"""
        for i in range(self.size):
            for j in range(self.size):
                btn = self.buttons[i][j]
                if self.grid[i][j]:  # Живая клетка
                    if self.pumpkin_image:
                        btn.config(image=self.pumpkin_image, text="", compound=tk.CENTER)
                    else:
                        # Если изображение не загружено, используем цвет
                        btn.config(image="", bg="orange", text="🎃")
                else:  # Мертвая клетка
                    btn.config(image="", bg="white", text="")
        
        # Проверяем победу
        if self.check_win():
            self.status_label.config(
                text="🎉 Поздравляем! Вы выиграли! Все клетки мертвы!",
                fg="green",
                font=("Arial", 14, "bold")
            )
        else:
            # Считаем живые клетки
            alive_count = sum(sum(row) for row in self.grid)
            self.status_label.config(
                text=f"Живых клеток: {alive_count}",
                fg="black",
                font=("Arial", 12)
            )
    
    def toggle_cell_state(self, row, col):
        """Переключает состояние клетки и её соседей (без обновления дисплея)"""
        # Переключаем саму клетку
        self.grid[row][col] = not self.grid[row][col]
        
        # Переключаем соседей (верх, низ, лево, право)
        neighbors = [
            (row - 1, col),  # верх
            (row + 1, col),  # низ
            (row, col - 1),  # лево
            (row, col + 1),  # право
        ]
        
        for nr, nc in neighbors:
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.grid[nr][nc] = not self.grid[nr][nc]
    
    def on_cell_click(self, row, col):
        """Обрабатывает клик по клетке"""
        self.toggle_cell_state(row, col)
        # Обновляем отображение
        self.update_display()
    
    def _toggle_cell_on_grid(self, grid, row, col):
        """Вспомогательный метод: переключает состояние клетки и соседей на переданном поле"""
        # Переключаем саму клетку
        grid[row][col] = not grid[row][col]
        
        # Переключаем соседей (верх, низ, лево, право)
        neighbors = [
            (row - 1, col),  # верх
            (row + 1, col),  # низ
            (row, col - 1),  # лево
            (row, col + 1),  # право
        ]
        
        for nr, nc in neighbors:
            if 0 <= nr < self.size and 0 <= nc < self.size:
                grid[nr][nc] = not grid[nr][nc]
    
    def generate_random_field(self):
        """Генерирует поле через случайные клики начиная с пустого поля"""
        # Начинаем с пустого поля (все клетки мертвые)
        grid = [[False for _ in range(self.size)] for _ in range(self.size)]
        
        # Производим случайное количество кликов (от 5 до 15 для разнообразия)
        num_clicks = random.randint(5, 15)
        
        for _ in range(num_clicks):
            # Случайно выбираем клетку для клика
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            # Симулируем клик на временном поле
            self._toggle_cell_on_grid(grid, row, col)
        
        return grid
    
    def check_win(self):
        """Проверяет, все ли клетки мертвы"""
        return all(not cell for row in self.grid for cell in row)
    
    def restart_game(self):
        """Начинает новую игру"""
        self.grid = self.generate_random_field()
        self.update_display()

def main():
    root = tk.Tk()
    game = CellGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
