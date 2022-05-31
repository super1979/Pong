import tkinter as tk
import random
import winsound
from threading import Thread
import time

class Pong:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title('Pong')
        self.window.configure(width=1300, height=650, bg='grey')
        self.window.resizable(False, False)

        self.on = True
        self.speed = 0.01
        self.speed_interval = 0.001

        self.create_scoreboard()
        self.create_canvas()
        self.create_panel()
        
        new_thread = Thread(target=self.start, daemon=True)
        new_thread.start()
        self.window.mainloop()

    def create_scoreboard(self):

        self.l_win = 0
        self.r_win = 0
        self.scoreboard = tk.Label(self.window, bg='grey', font=('Arial', '24'), fg='white')
        self.scoreboard['text'] = f'Player A: {self.l_win}  Player B: {self.r_win}'
        self.scoreboard.grid(row=0, column=0)

    def create_canvas(self):

        self.drawing_board = tk.Canvas(self.window, bg='black', height='600', width='800', highlightcolor='black', highlightbackground='black')
        self.drawing_board.grid(row=1, column=0)
        self.graphics()

    def graphics(self):

        self.left_paddle = self.drawing_board.create_rectangle(40, 240, 60, 340, fill='white')
        self.right_paddle = self.drawing_board.create_rectangle(740, 240, 760, 340, fill='white')

        self.create_ball()
        self.key_bindings()
    
    def create_ball(self):

        self.ball = self.drawing_board.create_oval(390, 290, 410, 310, fill='white')
        self.random_start()
        
    def random_start(self):

        a = 0
        while a == 0:
            a = random.randint(-1, 1)
        self.ball_dx = a * 2
        b = 0
        while b == 0:
            b = random.randint(-1, 1)
        self.ball_dy = b * 2
        self.drawing_board.coords(self.ball, 390, 290, 410, 310)
        self.scoreboard['text'] = f'Player A: {self.l_win}  Player B: {self.r_win}'
        self.drawing_board.coords(self.left_paddle, 40, 250, 60, 350)
        self.drawing_board.coords(self.right_paddle, 740, 240, 760, 340)

    def key_bindings(self):

        self.window.bind('w', self.up)
        self.window.bind('s', self.down)
        self.window.bind('<KeyPress-Up>', self.up)
        self.window.bind('<KeyPress-Down>', self.down)
    
    def up(self, event):

        if event.keysym == 'Up':
            y = self.drawing_board.coords(self.right_paddle)
            if y[1] >= 20:
                self.drawing_board.move(self.right_paddle, 0, -20)
        else:
            y = self.drawing_board.coords(self.left_paddle)
            if y[1] >= 20: 
                self.drawing_board.move(self.left_paddle, 0, -20)

    def down(self, event):

        if event.keysym == 'Down':
            y = self.drawing_board.coords(self.right_paddle)
            if y[3] <= 580:
                self.drawing_board.move(self.right_paddle, 0, 20)
        else:
            y = self.drawing_board.coords(self.left_paddle)
            if y[3] <= 580:
                self.drawing_board.move(self.left_paddle, 0, 20)
    
    def create_panel(self):

        self.right_panel = tk.Frame(self.window, bg='white', height=650, width=450)
        self.right_panel.grid(row=0, column=1, rowspan=2)
        self.right_panel.grid_propagate(0)
        self.create_instructions()
        self.create_buttons()

    def create_instructions(self):

        tk.Label(self.right_panel, text='Instructions', font=('Arial', '24', 'underline'), bg='white').grid(row=0, sticky=tk.W)
        tk.Label(self.right_panel, text="1. Use 'w' to move the left paddle up and 's' to move it down.", font=('Arial', '12'), bg='white').grid(row=1, sticky=tk.W)
        tk.Label(self.right_panel, text='2. Use up arrow to move the right paddle up and down arrow\n     to move it down.', font=('Arial', '12'), bg='white', justify=tk.LEFT).grid(row=2, sticky=tk.W)
        tk.Label(self.right_panel, text="3. Press the 'Restart' button below to reset the game.", font=('Arial', '12'), bg='white').grid(row=3, sticky=tk.W)
        tk.Label(self.right_panel, text="4. To quit, press the 'Quit' button below.\n    Do not use the window close button.", font=('Arial', '12'), bg='white', justify=tk.LEFT).grid(row=5, sticky=tk.W)
        tk.Label(self.right_panel, text="5. To increase/decrease the speed, press the appropriate button\n    below.", font=('Arial', '12'), bg='white', justify=tk.LEFT).grid(row=7, sticky=tk.W)

    def create_buttons(self):

        tk.Button(self.right_panel, text='Quit', font=('Arial', '12'), command=self.quit).grid(row=6)
        tk.Button(self.right_panel, text='Restart', font=('Arial', '12'), command=self.restart).grid(row=4)
        frame = tk.Frame(self.right_panel, bg='white')
        frame.grid(row=8)
        tk.Button(frame, text='Faster', font=('Arial', '12'), command=self.increase).grid(row=0, column=0)
        tk.Button(frame, text='Slower', font=('Arial', '12'), command=self.decrease).grid(row=0, column=1)

    def quit(self):

        self.on = False
        
    def restart(self):

        self.l_win = 0
        self.r_win = 0
        self.random_start()

    def increase(self):

        if self.speed > self.speed_interval:
            self.speed -= self.speed_interval
        else:
            self.speed_interval /= 10
            self.speed -= self.speed_interval

    def decrease(self):

        if self.speed / self.speed_interval >= 10:
            self.speed_interval *= 10
            self.speed += self.speed_interval
        else:
            self.speed += self.speed_interval

    def start(self):

        while self.on:
            self.drawing_board.move(self.ball, self.ball_dx, self.ball_dy)

            self.border_check()
            self.collision_check()
            time.sleep(self.speed)
        self.window.destroy()

    def border_check(self):

        coords = self.drawing_board.coords(self.ball)

        if coords[1] <= 0:
            self.drawing_board.coords(self.ball, coords[0], 0, coords[2], 20)
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

        if coords[3] >= 600:
            self.drawing_board.coords(self.ball, coords[0], 580, coords[2], 600)
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

        if coords[2] >= 800:
            self.l_win += 1
            self.random_start()

        if coords[0] <= 0:
            self.r_win += 1
            self.random_start()

    def collision_check(self):

        coords_ball = self.drawing_board.coords(self.ball)
        coords_lpaddle = self.drawing_board.coords(self.left_paddle)
        coords_rpaddle = self.drawing_board.coords(self.right_paddle)

        if coords_ball[2] == 740 and coords_ball[3] >= coords_rpaddle[1] and coords_ball[1] <= coords_rpaddle[3]:
            self.ball_dx *= -1
            winsound.Beep(1000, 10)
        
        if coords_ball[1] == coords_rpaddle[3] and coords_ball[2] > coords_rpaddle[0] and coords_ball[0] < coords_rpaddle[2]:
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

        if coords_ball[3] == coords_rpaddle[1] and coords_ball[2] > coords_rpaddle[0] and coords_ball[0] < coords_rpaddle[2]:
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

        if coords_ball[0] == 60 and coords_ball[3] >= coords_lpaddle[1] and coords_ball[1] <= coords_lpaddle[3]:
            self.ball_dx *= -1
            winsound.Beep(1000, 10)
        
        if coords_ball[1] == coords_lpaddle[3] and coords_ball[0] < coords_lpaddle[2] and coords_ball[2] > coords_lpaddle[0]:
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

        if coords_ball[3] == coords_lpaddle[1] and coords_ball[0] < coords_lpaddle[2] and coords_ball[2] > coords_lpaddle[0]:
            self.ball_dy *= -1
            winsound.Beep(1000, 10)

game = Pong()
