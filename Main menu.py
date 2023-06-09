import tkinter as tk
import random

def menu_close():
    main_window.withdraw()

def start_game():
    menu_close()

    game_window = tk.Tk()
    game_window.title("Line Game")
    game_window.geometry('700x800')
    game_window.resizable(False, False)

    canvas_width = 700
    canvas_height = 800

    c = tk.Canvas(game_window, width=canvas_width, height=canvas_height, bg='white')
    c.pack()

    dot_size = 16
    dot_spacing = 100
    line_thickness = 12

    player_first = True
    win_condition = 20

    result_label = tk.Label(game_window, text='', font=('Arial', 20, 'bold'), bg='white')
    result_label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

    player_count_label = tk.Label(game_window, text="Player's count: 0", font=('Arial', 16, 'bold'), bg='white', fg='crimson')
    player_count_label.place(relx=0.1, rely=0.18, anchor=tk.SW)

    computer_count_label = tk.Label(game_window, text="Computer's count: 0", font=('Arial', 16, 'bold'), bg='white', fg='lightseagreen')
    computer_count_label.place(relx=0.61, rely=0.18, anchor=tk.SW)

    branch_counts = []  # Store branch counts

    start_x = (canvas_width - (4 * dot_spacing + 4 * dot_size)) // 2
    start_y = (canvas_height - (4 * dot_spacing + 4 * dot_size)) // 2


    def player_wins():
        global game_over
        print('Player wins!')
        game_over = True
        result_label.config(text='Game Over! Player Wins.')


    def computer_wins():
        global game_over
        print('Game Over. You lose.')
        game_over = True


    def player_turn(event):
        global game_over
        if game_over:
            return
        line_id = event.widget.find_closest(event.x, event.y)[0]
        color = c.itemcget(line_id, 'fill')

        if color == 'crimson' or color == 'lightseagreen':
            return

        if color == 'white':
            c.itemconfig(line_id, fill='crimson')
            update_player_count()
            computer_turn()

        longest_line_length = count_longest_line()

        if all_colored():
            result_label.config(text='Game Over! There are no more moves.')

        if not check_win_condition(longest_line_length):
            return

        # Update the player count starting from the clicked line
        player_count = count_longest_line(start_line=line_id)
        player_count_label.config(text="Player's count: " + str(player_count))



    def computer_turn():
        global game_over
        if game_over:
            return

        white_lines = [line for line in lines if c.itemcget(line, 'fill') == 'white']
        if white_lines:
            line_id = random.choice(white_lines)
            c.itemconfig(line_id, fill='lightseagreen')
        else:
            return


    def count_longest_line(start_line=None):
        longest_line_length = 0
        visited = set()

        for line_id in lines:
            if c.itemcget(line_id, 'fill') == 'crimson' and line_id not in visited:
                if start_line and line_id != start_line:
                    continue

                touching_line_length = 0
                stack = [(line_id, line_id)]  # Tuple: (current_line, prev_line)
                while stack:
                    current_line, prev_line = stack.pop()
                    if current_line not in visited:
                        visited.add(current_line)
                        touching_line_length += 1
                        touching_lines = get_touching_red_lines(current_line)
                        valid_touching_lines = [line for line in touching_lines if line != prev_line]
                        stack.extend([(line, current_line) for line in valid_touching_lines])

                longest_line_length = max(longest_line_length, touching_line_length)

        return longest_line_length



    def is_only_touching_one_side(line1, line2):
        x1, y1, x2, y2 = c.coords(line1)
        x3, y3, x4, y4 = c.coords(line2)

        # Determine the orientation of the lines based on their coordinates
        line1_horizontal = y1 == y2
        line1_vertical = x1 == x2
        line2_horizontal = y3 == y4
        line2_vertical = x3 == x4

        if line1_horizontal and line2_horizontal:
            return (y1 == y3 or y1 == y4) and (y2 == y3 or y2 == y4)
        elif line1_vertical and line2_vertical:
            return (x1 == x3 or x1 == x4) and (x2 == x3 or x2 == x4)

        return False


    def get_touching_red_lines(line_id):
        touching_lines = []
        x1, y1, x2, y2 = c.coords(line_id)
        nearby_lines = c.find_overlapping(x1 - 5, y1 - 5, x2 + 5, y2 + 5)
        for nearby_line in nearby_lines:
            if nearby_line != line_id:
                color = c.itemcget(nearby_line, 'fill')
                if color == 'crimson':
                    touching_lines.append(nearby_line)
        return touching_lines


    def all_colored():
        for line in lines:
            color = c.itemcget(line, 'fill')
            if color == 'white':
                return False
        return True
    


    def check_win_condition(player_count):
        if player_count >= win_condition:
            player_wins()
            return True

        computer_count = count_longest_line()
        if computer_count >= win_condition:
            computer_wins()
            return True

        return False


    def update_player_count():
        player_count = count_longest_line()
        player_count_label.config(text="Player's count: " + str(player_count))


    def main_menu():
        game_window.destroy()
        main_window.deiconify()



    lines = []
    dots = []

    def start_new_game():

        global game_over
        game_over = False
        branch_counts.clear()  # Clear branch_counts list
        result_label.config(text='')
        player_count_label.config(text="Player's count: 0")
        c.delete('all')
        lines.clear()
        dots.clear()

        for row in range(5):
            for col in range(4):
                x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
                y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
                line = c.create_line(x, y, x + dot_spacing + dot_size, y, fill="white", width=line_thickness)
                lines.append(line)
                c.tag_bind(line, '<Button-1>', player_turn)

        for row in range(4):
            for col in range(5):
                x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
                y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
                line = c.create_line(x, y, x, y + dot_spacing + dot_size, fill="white", width=line_thickness)
                lines.append(line)
                c.tag_bind(line, '<Button-1>', player_turn)

        for row in range(5):
            for col in range(5):
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


def menu_quit():
    main_window.destroy()
    quit()


player_count_label = tk.Label(main_window, text="Longest Line Game", font=('Arial', 16, 'bold'), fg='black')
player_count_label.place(relx=0.35, rely=0.25, anchor=tk.SW)

play_button = tk.Button(main_window, text="Play", font=('Arial', 16, 'bold'), bg='goldenrod', command=start_game)
play_button.place(relx=0.45, rely=0.5, anchor=tk.SE)

quit_button = tk.Button(main_window, text="Quit", font=('Arial', 16, 'bold'), bg='mediumseagreen', command=menu_quit)
quit_button.place(relx=0.7, rely=0.5, anchor=tk.SE)


main_window.mainloop()

