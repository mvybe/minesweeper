import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


colors = {
    1: 'blue',
    2: '#550ec7',
    3: '#22a345',
    4: '#638a08',
    5: '#8f0b49',
    6: '#cf1361',
    7: '#4947c4',
    8: '#ad3ce3',
}


class MyButton(tk.Button):
    
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        
        super(MyButton, self).__init__(master,  width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False
    
    def __repr__(self):
        return f'MyButton{self.x}, {self.y}, {self.number}, {self.is_mine}'

class Minesweeper:
    
    # Создание окна.
    window = tk.Tk()

    # Количество рядов, колон, мин.
    row = 12
    column = 10
    mines = 3
    is_game_over = False
    is_first_click = True
    
    def __init__(self):
        
        # Создание кнопок.
        self.buttons = []

        for i in range(Minesweeper.row + 2):
            # Временный список.
            temp = []
            for j in range(Minesweeper.column + 2):
                btn = MyButton(Minesweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
            
    def right_click(self, event):
        if Minesweeper.is_game_over:
            return
        
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        
        if Minesweeper.is_game_over:
            return
        
        if Minesweeper.is_first_click:
            self.insert_mines(clicked_button.number) 
            self.count_mines_in_buttons()
            self.print_buttons()
            Minesweeper.is_first_click = False
        
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            Minesweeper.is_game_over = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, Minesweeper.row + 1):
                for j in range(1, Minesweeper.column + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'

        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)
 
    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
                cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        #if  not abs(dx - dy) == 1:
                        #    continue
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1<=next_btn.x<=Minesweeper.row and 1<=next_btn.y<=Minesweeper.column and next_btn not in queue:
                            queue.append(next_btn)
    # Перезапуск игры
    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        Minesweeper.is_first_click = True
        Minesweeper.is_game_over = False
    
    def create_settings_window(self):
        window_settings = tk.Toplevel(self.window)
        
        window_settings.wm_title('Настройки')
        
        tk.Label(window_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(window_settings)
        row_entry.insert(0, Minesweeper.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        
        tk.Label(window_settings, text='Количество колон').grid(row=1, column=0)
        column_entry = tk.Entry(window_settings)
        column_entry.insert(0, Minesweeper.column)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        
        tk.Label(window_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(window_settings)
        mines_entry.insert(0, Minesweeper.mines)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        seve_btn = tk.Button(window_settings, text='Сохранить', command=lambda :self.change_settings(row_entry, column_entry, mines_entry))
        seve_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
        
    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение.')
            return
            
        Minesweeper.row = int(row.get())
        Minesweeper.column = int(column.get())
        Minesweeper.mines = int(mines.get())
        self.reload()
 
    # Вывод кнопок            
    def create_widgets(self):
        # Меню
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        settings_menu = tk.Menu(menubar, tearoff = 0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_window)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Меню', menu=settings_menu)
        
        count = 1
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row = i, column = j, stick='NWES')
                count += 1
                
        for i in range(1, Minesweeper.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
            
        for i in range(1, Minesweeper.column + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)   
                
    def open_all_buttons(self):
        for i in range(Minesweeper.row + 2):
            for j in range(Minesweeper.column + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        
        self.create_widgets()
        #self.insert_mines() 
        #self.count_mines_in_buttons()
        #self.print_buttons()
        #self.open_all_buttons()
        
        # Вывод окна.
        Minesweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()
            
    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for column_dx in [-1, 0, 1]:
                                neighbour = self.buttons[i+row_dx][j+column_dx]
                                if neighbour.is_mine:
                                    count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod       
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, Minesweeper.column * Minesweeper.row + 1))
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:Minesweeper.mines]
        

game = Minesweeper()
game.start()

