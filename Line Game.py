import tkinter as tk
import random

window = tk.Tk()
window.title("Line Game")
window.geometry('600x600')

canvas_width = 600
canvas_height = 600

c = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
c.pack()

dot_size = 16
dot_spacing = 100
line_thickness = 12

player_first = True
win_condition = 8
game_over = False

result_label = tk.Label(window, text='', font=('Arial', 20, 'bold'), bg='white')
result_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

player_count_label = tk.Label(window, text="Player's count: 0", font=('Arial', 16), bg='white')
player_count_label.place(relx=0.1, rely=0.95, anchor=tk.SW)



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
    lengths = {}
    for line_id in lines:
        if c.itemcget(line_id, 'fill') == 'crimson':
            visited = set()
            length = counting_function(line_id, visited, 1, lengths)
            lengths[line_id] = length

    longest_line_length = max(lengths.values(), default=0)
    return longest_line_length


def counting_function(line_id, visited, current_length, lengths, prev_line_id=None):
    visited.add(line_id)

    if line_id not in lengths or current_length > lengths[line_id]:
        lengths[line_id] = current_length

    touching_lines = get_touching_red_lines(line_id)
    valid_touching_lines = []

    for neighbor_id in touching_lines:
        if neighbor_id not in visited and neighbor_id != prev_line_id:
            valid_touching_lines.append(neighbor_id)

    if not valid_touching_lines:
        return current_length

    max_length = current_length

    for neighbor_id in valid_touching_lines:
        new_visited = visited.copy()
        new_length = counting_function(neighbor_id, new_visited, current_length + 1, lengths, line_id)
        if new_length > max_length:
            max_length = new_length

    return max_length


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


start_x = (canvas_width - (3 * dot_spacing + 4 * dot_size)) // 2
start_y = (canvas_height - (3 * dot_spacing + 4 * dot_size)) // 2

lines = []
for row in range(4):
    for col in range(3):
        x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
        y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
        line = c.create_line(x, y, x + dot_spacing + dot_size, y, fill="white", width=line_thickness)
        lines.append(line)
        c.tag_bind(line, '<Button-1>', player_turn)

for row in range(3):
    for col in range(4):
        x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
        y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
        line = c.create_line(x, y, x, y + dot_spacing + dot_size, fill="white", width=line_thickness)
        lines.append(line)
        c.tag_bind(line, '<Button-1>', player_turn)

dots = []
for row in range(4):
    for col in range(4):
        x = start_x + col * (dot_size + dot_spacing)
        y = start_y + row * (dot_size + dot_spacing)
        c.create_oval(x, y, x + dot_size, y + dot_size, fill="black")

if not player_first:
    computer_turn()

window.mainloop()
