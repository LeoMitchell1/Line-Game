import tkinter as tk
import random
from pygame import mixer
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageDraw, ImageFilter


def click_sound():
    mixer.init()
    click_sound = mixer.Sound("Click sound.mp3")
    click_sound.play()


mixer.init()
background_music = mixer.Sound("Background Music.mp3")
background_music.play(loops=-1)

def menu_close():
    main_window.withdraw()

def start_game(grid_size, player_vs_player, difficulty, win_condition):
    menu_close()

    global player1_turn_check

    game_window = tk.Tk()
    game_window.title("Line Game")
    game_window.geometry('700x800')
    game_window.resizable(False, False)

    canvas_width = 700
    canvas_height = 800

    c = tk.Canvas(game_window, width=canvas_width, height=canvas_height, bg='#18191A')
    c.pack()

    dot_size = 16
    dot_spacing = 100
    line_thickness = 12

    player1_turn_check = True
    player_first = True
    num_row = grid_size - 1
    num_col = grid_size

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
    start_x = (canvas_width - grid_width) // 1
    start_y = (canvas_height - grid_height) // 2

    computer_lines = []
    player_lines = []


    def player_wins():
        global game_over
        game_over = True
        result_label.config(text='Congratulations! Player Wins.')

    def computer_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Computer Wins.')

    def player1_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Player 1 Wins.')
    
    def player2_wins():
        global game_over
        game_over = True
        result_label.config(text='Game Over! Player 2 Wins.')

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
            
    def player_vs_player_turn(event):
        global game_over, player1_turn_check

        if game_over:
            return
        line_id = event.widget.find_closest(event.x, event.y)[0]
        color = c.itemcget(line_id, 'fill')

        if color == '#FF1199' or color == '#11FFEE':
            return
        
        if color == '#18191A':
            if player1_turn_check == True:
                c.itemconfig(line_id, fill='#FF1199')
                click_sound()
                player_lines.append(line_id)
                update_player1_count()
                player1_turn_check = False
                longest_player_length = count_longest_line(player_lines)
                check_red_win_condition(longest_player_length)

            elif player1_turn_check == False:
                c.itemconfig(line_id, fill='#11FFEE')
                click_sound()
                computer_lines.append(line_id)
                update_player2_count()
                player1_turn_check = True
                longest_computer_length = count_longest_line(computer_lines)
                check_blue_win_condition(longest_computer_length)

        if all_colored():
            if game_over == False:
                result_label.config(text='Game Over! There are no more moves.')
                game_over = True
            else:
                return
        
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
                while stack:
                    current_line, prev_line = stack.pop()
                    if current_line not in visited:
                        visited.add(current_line)
                        touching_line_length += 1
                        touching_lines = get_touching_lines(current_line, color1)
                        valid_touching_lines = [line for line in touching_lines if line != prev_line]
                        stack.extend([(line, current_line) for line in valid_touching_lines])

                longest_length = max(longest_length, touching_line_length)

        return longest_length

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
    
    def get_touching_white_lines(line_id):
        x1, y1, x2, y2 = c.coords(line_id)
        nearby_lines = c.find_overlapping(x1 - 5, y1 - 5, x2 + 5, y2 + 5)
        white_touching_lines = [line for line in nearby_lines if c.itemcget(line, 'fill') == '#18191A']
        return white_touching_lines

    def all_colored():
        for line in lines:
            color = c.itemcget(line, 'fill')
            if color == '#18191A':
                return False
        return True

    def check_red_win_condition(player_count):
        if player_count >= win_condition:
            if player_vs_player == False:
                player_wins()
            else:
                player1_wins()
            return True
        return False
    
    def check_blue_win_condition(computer_count):
        if computer_count >= win_condition:
            if player_vs_player == False:
                computer_wins()
            else:
                player2_wins()
            return True
        return False

    def update_player_count():
        player_count = count_longest_line(player_lines)
        player_count_label.config(text="Player count: " + str(player_count))

    def update_computer_count():
        computer_count = count_longest_line(computer_lines)
        computer_count_label.config(text="Computer count: " + str(computer_count))

    def update_player1_count():
        player_count = count_longest_line(player_lines)
        player_count_label.config(text="Player 1 count: " + str(player_count))

    def update_player2_count():
        computer_count = count_longest_line(computer_lines)
        computer_count_label.config(text="Player 2 count: " + str(computer_count))

    def main_menu():
        game_window.destroy()
        main_window.deiconify()

    lines = []
    dots = []

    def start_new_game():
        global game_over
        game_over = False
        result_label.config(text='')
        if player_vs_player == False:
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
        
        for row in range(num_col):
            for col in range(num_row):
                x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
                y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
                line = c.create_line(x, y, x + dot_spacing + dot_size, y, fill="#18191A", width=line_thickness)
                lines.append(line)
                if player_vs_player == False:
                    c.tag_bind(line, '<Button-1>', player_turn)
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


videoplayer = TkinterVideo(master=main_window, scaled=True)
videoplayer.load(r"Background Video.mp4")
videoplayer.pack(expand=True, fill='both')
videoplayer.play()

def video_loop():
    videoplayer.play()
    main_window.after(1, video_loop)
main_window.after(1, video_loop)

def menu_quit():
    main_window.destroy()
    background_music.stop()
    quit()


title_label = tk.Label(main_window, text="HyperLine Showdown", font=('Roboto', 35, 'bold'), fg='#11FFEE', bg='#18191A')
title_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)


def start_with_options():
    grid_size = int(grid_size_var.get())
    player_vs_player = player_vs_player_var.get()
    difficulty = difficulty_var.get()
    win_condition = int(win_condition_entry.get())  # Get the win condition from the entry widget
    start_game(grid_size, player_vs_player, difficulty, win_condition)


    # Create grid size selection
grid_size_label = tk.Label(main_window, text="Grid Size:", font=('Arial', 16), bg='#18191A', fg='white')
grid_size_label.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

grid_size_var = tk.StringVar(main_window)
grid_size_var.set("5")  # Default value

grid_size_options = ["3", "4", "5"]  # Customize available grid sizes if needed

grid_size_menu = tk.OptionMenu(main_window, grid_size_var, *grid_size_options)
grid_size_menu.config(font=('Arial', 14), bg='white', activebackground='white', fg='black', activeforeground='black', relief='flat')
grid_size_menu.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

# Create player vs player checkbox
player_vs_player_label = tk.Label(main_window, text="Player vs Player", font=('Arial', 16), bg='#18191A', fg='white')
player_vs_player_label.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

player_vs_player_var = tk.BooleanVar(main_window)
player_vs_player_check = tk.Checkbutton(main_window, variable=player_vs_player_var, bg='#18191A', activebackground='#18191A')
player_vs_player_check.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

# Create difficulty selection
difficulty_label = tk.Label(main_window, text="Difficulty:", font=('Arial', 16), bg='#18191A', fg='white')
difficulty_label.place(relx=0.35, rely=0.8, anchor=tk.CENTER)

difficulty_var = tk.StringVar(main_window)
difficulty_var.set("Easy")  # Default value

difficulty_options = ["Easy", "Hard"]  # Customize available difficulty levels if needed

difficulty_menu = tk.OptionMenu(main_window, difficulty_var, *difficulty_options)
difficulty_menu.config(font=('Arial', 14), bg='white', activebackground='white', fg='black', activeforeground='black', relief='flat')
difficulty_menu.place(relx=0.6, rely=0.8, anchor=tk.CENTER)

win_condition_label = tk.Label(main_window, text="Win Condition:", font=('Arial', 16), bg='#18191A', fg='white')
win_condition_label.place(relx=0.4, rely=0.9, anchor=tk.CENTER)

win_condition_entry = tk.Entry(main_window, font=('Arial', 14), width=5)
win_condition_entry.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

# Create play button
play_button = tk.Button(main_window, text="Play", font=('Arial', 20), bg='white', command=start_with_options)
play_button.place(relx=0.42, rely=0.5, anchor=tk.CENTER)

quit_button = tk.Button(main_window, text="Quit", font=('Arial', 20), bg='white', command=menu_quit)
quit_button.place(relx=0.58, rely=0.5, anchor=tk.CENTER)


main_window.mainloop()