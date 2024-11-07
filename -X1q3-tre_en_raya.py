import tkinter as tk
from tkinter import messagebox


def check_winner(board, player):
    # Comprobar filas, columnas y diagonales
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Función para verificar si el tablero está lleno
def is_full(board):
    for row in board:
        if None in row:
            return False
    return True


def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):  # La maquina gana
        return 10 - depth
    if check_winner(board, 'X'):  # El jugador gana
        return depth - 10
    if is_full(board):  # Empate
        return 0
    
    if is_maximizing:
        best = -float('inf')
        
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = None
        return best
    else:
        best = float('inf')
        # Buscar las posibles jugadas
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = None
        return best


def best_move(board):
    best_value = -float('inf')
    move = None
    
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                move_value = minimax(board, 0, False)
                board[i][j] = None
                if move_value > best_value:
                    best_value = move_value
                    move = (i, j)
    return move


def on_click(row, col, buttons, board, player):
    if board[row][col] is None:
        board[row][col] = player
        buttons[row][col].config(text=player)
        
        
        if check_winner(board, player):
            label.config(text=f"¡{player} ha ganado!")
            disable_buttons(buttons)
            return
        
       
        if is_full(board):
            label.config(text="¡Es un empate!")
            return
        
        
        computer_move_pos = best_move(board)
        if computer_move_pos:
            i, j = computer_move_pos
            board[i][j] = 'O'
            buttons[i][j].config(text='O')

            
            if check_winner(board, 'O'):
                label.config(text="¡Perdiste!")
                disable_buttons(buttons)
                return
            
            
            if is_full(board):
                label.config(text="¡Es un empate!")
                return


def disable_buttons(buttons):
    for row in buttons:
        for button in row:
            button.config(state="disabled")

#reiniciar el juego
def reset_game():
    global board
    board = [[None, None, None], [None, None, None], [None, None, None]]
    label.config(text="¡Tu turno!")
    
    for row in buttons:
        for button in row:
            button.config(text="", state="normal")

#ventana principal
root = tk.Tk()
root.title("3 en Raya - Jugador vs Computadora")
root.config(bg="#f4f4f4")

# Crear tablero vacio
board = [[None, None, None], [None, None, None], [None, None, None]]

# estilo de botones
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", width=10, height=3, font=("Arial", 16), 
                                  relief="raised", bd=5, bg="#fff", fg="#333", 
                                  activebackground="#e7e7e7", command=lambda i=i, j=j: on_click(i, j, buttons, board, 'X'))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

# mensajes
label = tk.Label(root, text="¡Tu turno!", font=("Arial", 16), bg="#f4f4f4")
label.grid(row=3, column=0, columnspan=3, pady=10)

# Botpn de reinicio
reset_button = tk.Button(root, text="Reiniciar", font=("Arial", 12), bg="#4CAF50", fg="white", 
                         activebackground="#45a049", relief="raised", command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, pady=10, padx=5)

# ajuste del tamaño de la ventana
root.grid_rowconfigure(0, weight=1)  # botones de las casillas
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=0)  # mensaje de estado
root.grid_rowconfigure(4, weight=0)  # botón de reinicio
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Iniciar el juego
root.mainloop()
