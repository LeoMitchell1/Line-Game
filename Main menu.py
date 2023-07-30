import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
from pygame import mixer
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageDraw, ImageFilter

# Function to play a click sound
def click_sound():
    mixer.init()
    click_sound = mixer.Sound("Click sound.mp3")
    click_sound.play()

# Initialize and play background music
mixer.init()
background_music = mixer.Sound("Background Music.mp3")
background_music.play(loops=-1)

# Function to close the menu window
def menu_close():
    main_window.withdraw()


# Function to start the game with specified options
def start_game(grid_size, player_vs_player, difficulty, win_condition):
    menu_close()

    global player1_turn_check

    # Game window setup
    game_window = tk.Tk()
    game_window.title("Line Game")
    game_window.geometry('700x800')
    game_window.resizable(False, False)

    canvas_width = 700
    canvas_height = 800

    c = tk.Canvas(game_window, width=canvas_width, height=canvas_height, bg='#18191A')
    c.pack()

    # Game variables
    dot_size = 16
    dot_spacing = 100
    line_thickness = 12

    player1_turn_check = True
    player_first = True
    num_row = grid_size - 1
    num_col = grid_size


    # Display Labels
    result_label = tk.Label(game_window, text='', font=('Arial', 20, 'bold'), bg='#18191A', fg='white')
    result_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    win_condition_label = tk.Label(game_window, text="Win Condition: " + str(win_condition), font=('Arial', 16, 'bold'), bg='#18191A', fg='white')
    win_condition_label.place(relx=0.04, rely=0.06, anchor=tk.SW)

    player_count_label = tk.Label(game_window, text="Player count: 0", font=('Arial', 16, 'bold'), bg='#18191A', fg='#FF1199')
    player_count_label.place(relx=0.1, rely=0.18, anchor=tk.SW)

    computer_count_label = tk.Label(game_window, text="Computer count: 0", font=('Arial', 16, 'bold'), bg='#18191A', fg='#11FFEE')
    computer_count_label.place(relx=0.61, rely=0.18, anchor=tk.SW)


    if player_vs_player == True:
        player_count_label.config(text= "Player 1 count: 0")
        computer_count_label.config(text= "Player 2 count: 0")
        computer_count_label.place(relx=0.67, rely=0.18, anchor=tk.SW)
    
    grid_width = num_col * (dot_size + dot_spacing) + dot_size
    grid_height = num_row * (dot_size + dot_spacing) + dot_size

    # Calculate the new starting coordinates (centered in the canvas)
    start_x = ((canvas_width - grid_width) // 2) + 65
    start_y = ((canvas_height - grid_height) // 2) + 20

    computer_lines = []
    player_lines = []


    # Player win function
    def player_wins():
        global game_over
        game_over = True
        result_label.config(text='Congratulations! Player Wins.')


    # Computer win function
    def computer_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Computer Wins.')


    # Player 1 win function
    def player1_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Player 1 Wins.')
    

    # Player 2 win function
    def player2_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Player 2 Wins.')


    # Function to handle player's turn (for single-player mode)
    def player_turn(event):
        global game_over

        if game_over:
            return
        line_id = event.widget.find_closest(event.x, event.y)[0]
        color = c.itemcget(line_id, 'fill')

        if color == '#FF1199' or color == '#11FFEE':
            return

        if color == '#18191A':
            c.itemconfig(line_id, fill='#FF1199')
            click_sound()
            player_lines.append(line_id)
            update_player_count()
            computer_turn()

        longest_player_length = count_longest_line(player_lines)
        longest_computer_length = count_longest_line(computer_lines)

        check_red_win_condition(longest_player_length)
        check_blue_win_condition(longest_computer_length)
        
        if all_colored():
            if game_over == False:
                result_label.config(text='Game Over! There are no more moves.')
                game_over = True
            else:
                return


    # Function to handle player's turn (for player-vs-player mode)
    def player_vs_player_turn(event):
        global game_over, player1_turn_check

        if game_over:
            return
        line_id = event.widget.find_closest(event.x, event.y)[0]
        color = c.itemcget(line_id, 'fill')

        if color == '#FF1199' or color == '#11FFEE':
            return
        
        if color == '#18191A':  # Checks to see if the line is available
            if player1_turn_check == True: # Checks if it's the player 1's turn
                c.itemconfig(line_id, fill='#FF1199')
                click_sound()
                player_lines.append(line_id)
                update_player1_count()
                player1_turn_check = False
                longest_player_length = count_longest_line(player_lines)
                check_red_win_condition(longest_player_length)

            elif player1_turn_check == False: # If it is not player 1's turn do player 2
                c.itemconfig(line_id, fill='#11FFEE')
                click_sound()
                computer_lines.append(line_id) # Reuses the 'computer lines' for player 2
                update_player2_count()
                player1_turn_check = True # Switches back to player 1
                longest_computer_length = count_longest_line(computer_lines)
                check_blue_win_condition(longest_computer_length)

        if all_colored():
            if game_over == False:
                result_label.config(text='Game Over! There are no more moves.')
                game_over = True
            else:
                return


    # Function to handle computer's turn
    def computer_turn():
        global game_over, player1_turn_check
        if game_over:
            return

        white_lines = [line for line in lines if c.itemcget(line, 'fill') == '#18191A']

        if white_lines:
            if difficulty == "Easy":
                line_id = random.choice(white_lines)
                c.itemconfig(line_id, fill='#11FFEE')
                computer_lines.append(line_id)
                update_computer_count()
                return
            elif difficulty == "Hard":
                for player_line in player_lines:
                    adjacent_white_lines = get_touching_white_lines(player_line)
                    valid_white_lines = [line for line in adjacent_white_lines if line in white_lines]
                    if valid_white_lines:
                        line_id = random.choice(valid_white_lines)
                        c.itemconfig(line_id, fill='#11FFEE')
                        computer_lines.append(line_id)
                        update_computer_count()
                        break
                else:
                    # If there are no adjacent white lines, choose a random white line.
                    line_id = random.choice(white_lines)
                    c.itemconfig(line_id, fill='#11FFEE')
                    computer_lines.append(line_id)
                    update_computer_count()
        else:
            return


    # Function to count the longest line length for a given color (player/computer)
    def count_longest_line(lines):
        longest_length = 0
        visited = set()
        if lines == player_lines:
            color1 = '#FF1199'
        elif lines == computer_lines:
            color1 = '#11FFEE'
        for line_id in lines:
            if line_id not in visited:
                touching_line_length = 0
                stack = [(line_id, line_id)]
                while stack: # Creates a stack to add and keep track of line id's
                    current_line, prev_line = stack.pop()
                    if current_line not in visited:
                        visited.add(current_line)
                        touching_line_length += 1
                        touching_lines = get_touching_lines(current_line, color1)
                        valid_touching_lines = [line for line in touching_lines if line != prev_line]
                        stack.extend([(line, current_line) for line in valid_touching_lines])

                longest_length = max(longest_length, touching_line_length)

        return longest_length # Function returning the longest length line of that colour


    # Functions to check lines that are touching a given line and having a specific color
    def get_touching_lines(line_id, color1):
        touching_lines = []
        x1, y1, x2, y2 = c.coords(line_id)
        nearby_lines = c.find_overlapping(x1 - 5, y1 - 5, x2 + 5, y2 + 5)
        for nearby_line in nearby_lines:
            if nearby_line != line_id:
                color = c.itemcget(nearby_line, 'fill')
                if color == color1:
                    touching_lines.append(nearby_line)
        return touching_lines
    

    # Function to check for blank lines that are next to player lines
    def get_touching_white_lines(line_id):
        x1, y1, x2, y2 = c.coords(line_id)
        nearby_lines = c.find_overlapping(x1 - 5, y1 - 5, x2 + 5, y2 + 5)
        white_touching_lines = [line for line in nearby_lines if c.itemcget(line, 'fill') == '#18191A']
        return white_touching_lines


    # Function to check if there are no more moves left
    def all_colored():
        for line in lines:
            color = c.itemcget(line, 'fill')
            if color == '#18191A':
                return False
        return True


    # Function to check if the player has won
    def check_red_win_condition(player_count):
        if player_count >= win_condition:
            if player_vs_player == False:
                player_wins()
            else:
                player1_wins()
            return True
        return False
    

    # Function to check if player 2 or the computer has won
    def check_blue_win_condition(computer_count):
        if computer_count >= win_condition:
            if player_vs_player == False:
                computer_wins()
            else:
                player2_wins()
            return True
        return False


    # Updates the player's count display
    def update_player_count():
        player_count = count_longest_line(player_lines)
        player_count_label.config(text="Player count: " + str(player_count))


    # Updates the computer's count display
    def update_computer_count():
        computer_count = count_longest_line(computer_lines)
        computer_count_label.config(text="Computer count: " + str(computer_count))


    # Updates the player 1's count display
    def update_player1_count():
        player_count = count_longest_line(player_lines)
        player_count_label.config(text="Player 1 count: " + str(player_count))


    # Updates the player 2's count display
    def update_player2_count():
        computer_count = count_longest_line(computer_lines)
        computer_count_label.config(text="Player 2 count: " + str(computer_count))


    # Function to return to the main menu and close the game window
    def main_menu():
        game_window.destroy()
        main_window.deiconify()

    # Creates the lists of lines and dots
    lines = []
    dots = []

    # Resets and starts the new game
    def start_new_game():
        global game_over
        game_over = False
        result_label.config(text='')
        if player_vs_player == False:   # Changes labels depending on single player mode
            player_count_label.config(text="Player count: 0") 
            computer_count_label.config(text="Computer count: 0")
        else:
            player_count_label.config(text="Player 1 count: 0")
            computer_count_label.config(text="Player 2 count: 0")
        
        c.delete('all')
        lines.clear()
        dots.clear()
        player_lines.clear()
        computer_lines.clear()
        
        for row in range(num_col): # Creates the rows and dots
            for col in range(num_row):
                x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
                y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
                line = c.create_line(x, y, x + dot_spacing + dot_size, y, fill="#18191A", width=line_thickness)
                lines.append(line)
                if player_vs_player == False:
                    c.tag_bind(line, '<Button-1>', player_turn) # Binds the lines to left click and runs player turn
                else:
                    c.tag_bind(line, '<Button-1>', player_vs_player_turn)

        for row in range(num_row):
            for col in range(num_col):
                x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
                y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
                line = c.create_line(x, y, x, y + dot_spacing + dot_size, fill="#18191A", width=line_thickness)
                lines.append(line)
                if player_vs_player == False:
                    c.tag_bind(line, '<Button-1>', player_turn)
                else:
                    c.tag_bind(line, '<Button-1>', player_vs_player_turn)

        for row in range(num_col):
            for col in range(num_col):
                x = start_x + col * (dot_size + dot_spacing)
                y = start_y + row * (dot_size + dot_spacing)
                c.create_oval(x, y, x + dot_size, y + dot_size, fill="black")

        if not player_first:
            computer_turn()

    start_new_game()

    

    restart_button = tk.Button(game_window, text="Restart", font=('Arial', 16, 'bold'), bg='goldenrod', command=start_new_game)
    restart_button.place(relx=0.66, rely=0.95, anchor=tk.SE)

    menu_button = tk.Button(game_window, text="Main Menu", font=('Arial', 16, 'bold'), bg='mediumseagreen', command=main_menu)
    menu_button.place(relx=0.49, rely=0.95, anchor=tk.SE)

    game_window.mainloop()

# Main menu window

main_window = tk.Tk()
main_window.title("Main Menu")
main_window.geometry("600x600")
main_window.resizable(False, False)

canvas_width = 600
canvas_height = 600

# Background Video
videoplayer = TkinterVideo(master=main_window, scaled=True)
videoplayer.load(r"Background Video.mp4")
videoplayer.pack(expand=True, fill='both')
videoplayer.play()



def video_loop():
    videoplayer.play()
    main_window.after(1, video_loop)
main_window.after(1, video_loop)


# Function for the quit button
def menu_quit():
    main_window.destroy()
    background_music.stop()
    quit()


# Collects the information from the drop down menus
def start_with_options():
    grid_size = int(grid_size_var.get())
    player_vs_player = player_vs_player_var.get()
    difficulty = difficulty_var.get()
    
    try:
        win_condition = int(win_condition_entry.get())  # Get the win condition from the entry widget
        if win_condition <= 0:
            raise ValueError("Win condition must be a positive integer.")
    except ValueError: 
        # Handle invalid input (non-integer or negative value)
        messagebox.showerror("Invalid Win Condition", "Please enter a positive integer for the win condition.")
        return

    start_game(grid_size, player_vs_player, difficulty, win_condition)


# Error handling for the win condition
def validate_win_condition_input(value):
    if not value:
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False
    

# Opens the rules window
def show_rules():
    rule_window = tk.Toplevel(main_window)
    rule_window.title("Rules and Instructions")
    rule_window.geometry("700x400")
    rule_window.resizable(False, False)

    # Create labels to display the rules and instructions
    rule_label = ttk.Label(rule_window, text="Rules and Instructions", font=('Arial', 20, 'bold'), foreground='red')
    rule_label.pack(pady=10)

    rules_text = """
    The objective of the game is to place lines on the grid to form the longest connected line.
    
    - Each player takes turns creating lines by clicking on the available lines on the grid.
    - Players can only draw on the blank lines.
    - Any lines touching that are the same colour will count as one line
    - The game ends when someone reaches the win condition or there are no more available moves.
    - The player with a line equal to or longer than the win condition wins!
    - In single-player mode, the player competes against the computer.
    - In player-vs-player mode, two players take turns.
    - The difficulty of the computer can be changed in the options menu.
    - Increasing the win condition will also make it more difficult to win.
    """
    rules_label = ttk.Label(rule_window, text=rules_text, font=('Arial', 12))
    rules_label.pack(pady=10)

    # Create a back button to go back to the main menu
    back_button = ttk.Button(rule_window, text="Back to Main Menu", style="PlayButton.TButton", command=rule_window.destroy)
    back_button.pack(pady=20)
    

# Style configuration for the buttons
style = ttk.Style()
style.configure("PlayButton.TButton", font=('Arial', 20), foreground='black', background='#FFD700')
style.configure("RuleButton.TButton", font=('Arial', 15), foreground='black', background='#800080')
style.configure("QuitButton.TButton", font=('Arial', 20), foreground='black', background='#FF4500')
style.configure("Main.TLabel", font=('Roboto', 35, 'bold'), foreground='#11FFEE', background='#18191A')
style.configure("Subtitle.TLabel", font=('Arial', 16), foreground='white', background='#18191A')
style.configure("Entry.TEntry", font=('Arial', 14))
style.configure("Option.TMenubutton", font=('Arial', 14), foreground='black', background='white')


# Create title label with improved styling
title_label = ttk.Label(main_window, text="HyperLine Showdown", style="Main.TLabel")
title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

# Create grid size selection with improved styling
grid_size_label = ttk.Label(main_window, text="Grid Size:", style="Subtitle.TLabel")
grid_size_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

grid_size_var = tk.StringVar(main_window)
grid_size_var.set("4")  # Default value

grid_size_options = ["3", "4", "5"]  # Customize available grid sizes if needed

grid_size_menu = tk.OptionMenu(main_window, grid_size_var, *grid_size_options)
grid_size_menu.config(font=('Arial', 14), bg='white', activebackground='white', fg='black', activeforeground='black', relief='flat')
grid_size_menu.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

# Create player vs player checkbox with improved styling
player_vs_player_label = ttk.Label(main_window, text="Player vs Player", style="Subtitle.TLabel")
player_vs_player_label.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

player_vs_player_var = tk.BooleanVar(main_window)
player_vs_player_check = ttk.Checkbutton(main_window, variable=player_vs_player_var, style="Option.TCheckbutton")
player_vs_player_check.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

# Create difficulty selection with improved styling
difficulty_label = ttk.Label(main_window, text="Difficulty:", style="Subtitle.TLabel")
difficulty_label.place(relx=0.35, rely=0.8, anchor=tk.CENTER)

difficulty_var = tk.StringVar(main_window)
difficulty_var.set("Easy")  # Default value

difficulty_options = ["Easy", "Hard"]  # Customize available difficulty levels if needed

difficulty_menu = tk.OptionMenu(main_window, difficulty_var, *difficulty_options)
difficulty_menu.config(font=('Arial', 14), bg='white', activebackground='white', fg='black', activeforeground='black', relief='flat')
difficulty_menu.place(relx=0.6, rely=0.8, anchor=tk.CENTER)

# Create win condition entry with improved styling
win_condition_label = ttk.Label(main_window, text="Win Condition:", style="Subtitle.TLabel")
win_condition_label.place(relx=0.4, rely=0.9, anchor=tk.CENTER)

validate_win_condition = main_window.register(validate_win_condition_input)
win_condition_entry = ttk.Entry(main_window, font=('Arial', 14), width=5, validate="key", validatecommand=(validate_win_condition, "%P"), style="Entry.TEntry")
win_condition_entry.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

rules_button = ttk.Button(main_window, text="Rules", style="RuleButton.TButton", command=show_rules)
rules_button.place(relx=0.15, rely=0.05, anchor=tk.CENTER)

# Create play button with improved styling
play_button = ttk.Button(main_window, text="Play", style="PlayButton.TButton", command=start_with_options)
play_button.place(relx=0.325, rely=0.45, anchor=tk.CENTER)

# Create quit button with improved styling
quit_button = ttk.Button(main_window, text="Quit", style="QuitButton.TButton", command=menu_quit)
quit_button.place(relx=0.675, rely=0.45, anchor=tk.CENTER)
 

main_window.mainloop()