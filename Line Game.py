import tkinter as tk
import random

window = tk.Tk()
window.title("Line Game")
window.geometry('700x700')

canvas_width = 700
canvas_height = 700

c = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
c.pack()

dot_size = 16
dot_spacing = 100
line_thickness = 12

player_first = True
win_condition = 12
game_over = False

result_label = tk.Label(window, text='', font=('Arial', 20, 'bold'), bg='white')
result_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

player_count_label = tk.Label(window, text="Player's count: 0", font=('Arial', 16, 'bold'), bg='white', fg='crimson')
player_count_label.place(relx=0.1, rely=0.95, anchor=tk.SW)

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

    if color == 'crimson':
        return

    if color == 'lightseagreen':
        return

    if color == 'white':
        c.itemconfig(line_id, fill='crimson')
        update_player_count()
        computer_turn()

    longest_line_length = count_longest_line()
    print("Longest line length:", longest_line_length)

    if all_colored():
        print('There are no more moves.')

    if not check_win_condition(longest_line_length):
        return


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


def count_longest_line():
    longest_line_length = 0
    visited = set()
    visited_branch = set()

    for line_id in lines:
        if c.itemcget(line_id, 'fill') == 'crimson' and line_id not in visited:
            touching_line_length = 0
            branch_length = 0  # Added branch_length variable
            stack = [(line_id, line_id)]  # Tuple: (current_line, prev_line)
            branch_detected = False
            while stack:
                current_line, prev_line = stack.pop()
                if current_line not in visited:
                    visited.add(current_line)
                    touching_line_length += 1
                    touching_lines = get_touching_red_lines(current_line)
                    valid_touching_lines = [line for line in touching_lines if line != prev_line]
                    stack.extend([(line, current_line) for line in valid_touching_lines])

                    current_branch = (current_line, prev_line)
                    if len(valid_touching_lines) >= 2 and not branch_detected and current_branch not in visited_branch:  # Check for T-shape
                        print("Branch detected!")
                        visited_branch.add(current_branch)
                        branch_detected = True

            longest_line_length = max(longest_line_length, touching_line_length)
            if branch_detected:
                branch_counts.append(1)  # Add 1 to branch_counts for each detected branch
                print_branch_counts()  # Print branch counts

    return longest_line_length




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

    if all_colored():
        print("There are no more moves.")
        game_over = True

    return False


def update_player_count():
    player_count = count_longest_line()
    player_count_label.config(text="Player's count: " + str(player_count))


def print_branch_counts():
    print("Branch Counts:")
    for i, count in enumerate(branch_counts):
        print("Branch {}: {}".format(i + 1, count))



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

restart_button = tk.Button(window, text="Restart", font=('Arial', 16, 'bold'), bg='goldenrod', command=start_new_game)
restart_button.place(relx=0.9, rely=0.95, anchor=tk.SE)

window.mainloop()
